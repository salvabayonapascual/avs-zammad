"""Redaccion reversible y acotada de la licencia en #111121; --apply para aplicar.

Originales cifrados en Backups (excluido de Git). No borra articulos ni adjuntos,
no envia mensajes y no modifica la factura. Solo almacenamiento DB no compartido.
"""
import argparse
import base64
import email
import email.policy
import hashlib
import io
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

from pypdf import PdfReader
from cryptography.fernet import Fernet

import zammad_api as api
from zammad_ssh import ROOT, connect, rails, vault

TICKET, ARTICLE = 1123, 4032
MARKER = "[LICENCIA RETIRADA: original en custodia cifrada AVS]"


def download(path, token):
    request = urllib.request.Request(api.BASE_URL + path)
    request.add_header("Authorization", f"Token token={token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def redact_mail(raw, key):
    message = email.message_from_bytes(raw, policy=email.policy.default)
    hits = 0
    for part in message.walk():
        if part.is_multipart():
            continue
        content = part.get_payload(decode=True)
        if content is None or key.encode() not in content:
            continue
        if part.get_content_maintype() != "text":
            raise RuntimeError("Licencia en adjunto binario: revision necesaria.")
        hits += content.count(key.encode())
        encoding = part.get_content_charset() or "utf-8"
        text = content.decode(encoding).replace(key, MARKER)
        if part.get("Content-Transfer-Encoding"):
            del part["Content-Transfer-Encoding"]
        part.set_payload(text, charset=encoding)
    if not hits:
        raise RuntimeError("No se reconoce la licencia en el MIME original.")
    return message.as_bytes(policy=email.policy.SMTP), hits


RUBY = r'''
Rails.logger.level = Logger::ERROR
stage = 'parse'
begin
p = JSON.parse(STDIN.read)
a = Ticket::Article.find(4032)
raise 'Ticket inesperado' unless a.ticket_id == 1123 && a.ticket.number == '111121'
result = {}
ActiveRecord::Base.transaction do
  a.lock!
  raise 'Articulo cambiado' unless Digest::SHA256.hexdigest(a.body) == p.fetch('body_sha')
  p.fetch('stores').each do |change|
    stage = 'store_' + change.fetch('id').to_s
    s = Store.find(change.fetch('id')); s.lock!
    raise 'Adjunto inesperado' unless s.o_id.to_i == a.id && [10663,10664].include?(s.id)
    f = s.store_file; f.lock!
    raise 'Almacen compartido o no DB' unless f.provider == 'DB' && Store.where(store_file_id:f.id).count == 1
    raise 'Contenido cambiado' unless Digest::SHA256.hexdigest(s.content) == change.fetch('sha')
    replacement = Base64.strict_decode64(change.fetch('data'))
    new_sha = Digest::SHA256.hexdigest(replacement)
    raise 'Colision de contenido' if Store::File.where(sha:new_sha).where.not(id:f.id).exists?
    provider = Store::Provider::DB.find_by!(sha:f.sha); provider.lock!
    stage = 'provider_' + s.id.to_s
    provider.update!(data:replacement,sha:new_sha)
    f.update!(sha:new_sha)
    s.update!(size:replacement.bytesize)
    raise 'Escritura invalida' unless s.reload.content == replacement
  end
  # Sin callbacks: no registrar la clave anterior en historial ni enviar avisos.
  stage = 'article'
  a.update_columns(body:p.fetch('body'),updated_at:Time.current,updated_by_id:8)
  result = {article:a.id,ticket:a.ticket.number,stores:p.fetch('stores').map{|x|x['id']},ticket_state:a.ticket.state.name}
end
stage = 'index'
a.ticket.reload.search_index_update_backend
SearchIndexBackend.refresh
puts 'AVS_RESULT=' + result.to_json
rescue => error
  puts 'AVS_ERROR=' + {class:error.class.name,stage:stage}.to_json
end
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    token = api.get_token()
    status, article = api._request("GET", f"/ticket_articles/{ARTICLE}", token)
    if status != 200 or article["ticket_id"] != TICKET:
        raise RuntimeError("Articulo inesperado.")
    if MARKER in article["body"]:
        print("Articulo ya saneado; no se repite la operacion.")
        return
    text = api._html_to_text(article["body"])
    match = re.search(r"License Key:\s*([A-Z0-9]+(?:-[A-Z0-9]+){2,})", text)
    if not match:
        raise RuntimeError("Formato de licencia no reconocido.")
    key = match.group(1)
    client = connect()
    try:
        output = rails(client, "Rails.logger.level=Logger::ERROR; "
                       "puts 'AVS_BODY=' + Base64.strict_encode64(Ticket::Article.find(4032).body)")
        encoded = next(line[9:] for line in output.splitlines() if line.startswith("AVS_BODY="))
        database_body = base64.b64decode(encoded).decode()
    finally:
        client.close()
    if database_body.count(key) != 1:
        raise RuntimeError("Cuerpo original inesperado.")
    raw = download(f"/ticket_article_plain/{ARTICLE}", token)
    originals = {"article": article, "database_body": database_body,
                 "raw": base64.b64encode(raw).decode(), "attachments": {}}
    changes = []
    for attachment in article["attachments"]:
        data = download(f"/ticket_attachment/{TICKET}/{ARTICLE}/{attachment['id']}", token)
        originals["attachments"][str(attachment["id"])] = base64.b64encode(data).decode()
        if attachment["filename"].lower().endswith(".pdf"):
            pdf = PdfReader(io.BytesIO(data))
            if key in "\n".join(page.extract_text() or "" for page in pdf.pages):
                raise RuntimeError("La factura tambien contiene la clave: revisar antes de aplicar.")
        if key.encode() in data:
            if attachment["id"] != 10664:
                raise RuntimeError("Licencia en adjunto inesperado.")
            changes.append({"id": attachment["id"], "sha": hashlib.sha256(data).hexdigest(),
                            "data": base64.b64encode(data.replace(key.encode(), MARKER.encode())).decode()})
    redacted_raw, mime_hits = redact_mail(raw, key)
    changes.append({"id": 10663, "sha": hashlib.sha256(raw).hexdigest(),
                    "data": base64.b64encode(redacted_raw).decode()})
    if {x["id"] for x in changes} != {10663, 10664}:
        raise RuntimeError("No se reconocen todas las copias esperadas.")
    payload = {"body_sha": hashlib.sha256(database_body.encode()).hexdigest(),
               "body": database_body.replace(key, MARKER), "stores": changes}
    print(json.dumps({"ticket": "111121", "body_occurrences": article["body"].count(key),
                      "mime_occurrences": mime_hits, "stores": [x["id"] for x in changes],
                      "invoice_contains_license": False, "apply": args.apply}))
    if not args.apply:
        return
    v = vault()
    target = ROOT / "Documentacion/Privado/credenciales-zammad.md"
    cipher = Fernet(v.load_project_key(target))
    backup = ROOT / "Backups" / (datetime.now().strftime("%Y%m%d-%H%M%S") + "-111121-original.json.enc")
    backup.parent.mkdir(exist_ok=True)
    encrypted = cipher.encrypt(json.dumps(originals).encode())
    backup.write_bytes(encrypted)
    if json.loads(cipher.decrypt(backup.read_bytes())) != originals:
        raise RuntimeError("Copia cifrada no verificada.")
    client = connect()
    try:
        output = rails(client, RUBY, json.dumps(payload))
        for line in output.splitlines():
            if line.startswith('AVS_ERROR='):
                print(line)
                raise RuntimeError('Transaccion fallida; revisar etapa indicada.')
        result = next(line for line in output.splitlines() if line.startswith("AVS_RESULT="))
        print(result)
    finally:
        client.close()
    status, fresh = api._request("GET", f"/ticket_articles/{ARTICLE}", token)
    if status != 200 or key in fresh["body"] or MARKER not in fresh["body"]:
        raise RuntimeError("Verificacion del cuerpo fallida.")
    for change in changes:
        path = (f"/ticket_article_plain/{ARTICLE}" if change["id"] == 10663 else
                f"/ticket_attachment/{TICKET}/{ARTICLE}/{change['id']}")
        current = download(path, token)
        if current != base64.b64decode(change["data"]):
            raise RuntimeError("Verificacion del adjunto fallida.")
    status, matches = api._request("GET", "/tickets/search", token,
                                  params={"query": '"' + key + '"', "limit": 10})
    if status != 200 or any(t["id"] == TICKET for t in matches):
        raise RuntimeError("La licencia sigue en el indice; revisar.")
    print("Verificado: cuerpo, HTML original, MIME y busqueda sin licencia; factura y ticket conservados.")
    print("Copia cifrada local: " + backup.name)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Operacion interrumpida ({type(error).__name__}); detalles sensibles suprimidos.", file=sys.stderr)
        sys.exit(2)
