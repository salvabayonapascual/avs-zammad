"""SSH administrativo con clave del propietario Proxmox, solo en memoria."""
import importlib.util
import io
import re
import shlex
from pathlib import Path

import paramiko
from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[1]
HOST = "192.168.150.186"
CONTAINER = "zammad-docker-compose-zammad-railsserver-1"


def vault():
    path = Path.home() / ".config/obsidian-vault/secrets_tool.py"
    spec = importlib.util.spec_from_file_location("zammad_vault", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def connect():
    target = ROOT.parents[3] / "Servidor Proxmox/secretos.md"
    if target.exists():
        raise RuntimeError("El almacen administrativo debe estar cifrado.")
    v = vault()
    data = Fernet(v.load_project_key(target)).decrypt(v.enc_path(target).read_bytes()).decode()
    keys = re.findall(r"-----BEGIN (?:RSA |OPENSSH |EC |)PRIVATE KEY-----.*?"
                      r"-----END (?:RSA |OPENSSH |EC |)PRIVATE KEY-----", data, re.S)
    if len(keys) != 1:
        raise RuntimeError("Clave administrativa ambigua.")
    key = None
    for cls in (paramiko.Ed25519Key, paramiko.RSAKey, paramiko.ECDSAKey):
        try:
            key = cls.from_private_key(io.StringIO(keys[0]))
            break
        except paramiko.SSHException:
            continue
    if key is None:
        raise RuntimeError("Formato de clave desconocido.")
    client = paramiko.SSHClient()
    for line in (Path.home() / ".ssh/known_hosts").read_text().splitlines():
        try:
            entry = paramiko.hostkeys.HostKeyEntry.from_line(line)
        except Exception:
            continue
        if entry:
            for host in entry.hostnames:
                client.get_host_keys().add(host, entry.key.get_name(), entry.key)
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(HOST, username="root", pkey=key, allow_agent=False,
                   look_for_keys=False, timeout=15)
    return client


def rails(client, code, payload=None):
    # El entrypoint construye DATABASE_URL desde el entorno sin exportarla aqui.
    command = (f"docker exec {'-i ' if payload is not None else ''}{CONTAINER} "
               "/docker-entrypoint.sh bundle exec rails runner " + shlex.quote(code))
    stdin, stdout, stderr = client.exec_command(command, timeout=90)
    if payload is not None:
        stdin.write(payload)
        stdin.flush()
    stdin.channel.shutdown_write()
    output = stdout.read().decode(errors="replace")
    errors = stderr.read()  # Nunca exponer excepciones que puedan incluir el payload.
    if stdout.channel.recv_exit_status() != 0:
        raise RuntimeError("Consulta Rails fallida; salida sensible suprimida.")
    return output
