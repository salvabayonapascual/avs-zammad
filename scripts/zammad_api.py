"""Cliente API reutilizable para Zammad (lectura de token desde credenciales cifradas).

Uso desde linea de comandos:
    python scripts/zammad_api.py search <query> [--state new|open|closed|all]
    python scripts/zammad_api.py get <id>
    python scripts/zammad_api.py reply <id> <body> [--internal]
    python scripts/zammad_api.py close <id> [--body <body>] [--internal]
    python scripts/zammad_api.py delete <id> [<id> ...]

No expone el token en la salida. `search` usa el endpoint de busqueda con
`expand=true` y devuelve una lista compacta (id, number, title, state,
created_at). `delete` opera sobre el `id` interno, no sobre el `number`
visible -- resolver primero con `search` o `get` si solo se tiene el
number.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENCIALES_REL = os.path.join("Documentacion", "Privado", "credenciales-zammad.md")
CREDENCIALES_PATH = os.path.join(ROOT, CREDENCIALES_REL)
SECRETS_TOOL = os.path.join(os.path.expanduser("~"), ".config", "obsidian-vault", "secrets_tool.py")
BASE_URL = "https://zammad.avsconsulting.es/api/v1"


def get_token():
    """Lee el token de acceso API desde credenciales-zammad.md. Si solo existe
    la version cifrada (.enc), se desbloquea con secrets_tool.py el tiempo
    justo para leer el token y se vuelve a cifrar de inmediato (nunca queda
    una copia en claro tirada)."""
    if os.path.exists(CREDENCIALES_PATH):
        with open(CREDENCIALES_PATH, encoding="utf-8") as f:
            content = f.read()
    else:
        unlock = subprocess.run(
            [sys.executable, SECRETS_TOOL, "unlock", "--file", CREDENCIALES_REL, "--ttl", "60"],
            cwd=ROOT, capture_output=True, text=True,
        )
        if unlock.returncode != 0:
            raise SystemExit(f"No se pudo desbloquear {CREDENCIALES_REL}: {unlock.stderr.strip()}")
        temp_path = unlock.stdout.strip().splitlines()[-1]
        try:
            with open(temp_path, encoding="utf-8") as f:
                content = f.read()
        finally:
            subprocess.run(
                [sys.executable, SECRETS_TOOL, "lock", "--file", CREDENCIALES_REL],
                cwd=ROOT, capture_output=True, text=True,
            )
    m = re.search(r"^- Token:\s*(\S+)", content, re.MULTILINE)
    if not m:
        raise SystemExit("No se encontro el token de acceso API en credenciales-zammad.md")
    return m.group(1)


def _request(method, path, token, params=None, body=None):
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Token token={token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, raw.decode(errors="replace")


def search_tickets(token, query, state=None):
    q = f'title:"{query}"'
    if state and state != "all":
        q += f" AND state.name:{state}"
    status, data = _request("GET", "/tickets/search", token, params={"query": q, "limit": 200, "expand": "true"})
    if status != 200:
        raise RuntimeError(f"Error {status}: {data}")
    results = []
    for t in data:
        results.append({
            "id": t.get("id"),
            "number": t.get("number"),
            "title": t.get("title"),
            "state": t.get("state"),
            "created_at": t.get("created_at"),
        })
    return results


def get_ticket(token, ticket_id):
    status, data = _request("GET", f"/tickets/{ticket_id}", token)
    if status != 200:
        raise RuntimeError(f"Error {status}: {data}")
    return data


def delete_ticket(token, ticket_id):
    status, data = _request("DELETE", f"/tickets/{ticket_id}", token)
    return status


def ticket_states(token):
    status, data = _request("GET", "/ticket_states", token, params={"active": "true"})
    if status != 200:
        raise RuntimeError(f"Error {status}: {data}")
    return data


def state_id_by_name(token, name):
    for state in ticket_states(token):
        if str(state.get("name", "")).lower() == name.lower():
            return state["id"]
    raise RuntimeError(f"No se encontro el estado Zammad: {name}")


def update_ticket(token, ticket_id, state_id=None, body=None, internal=False):
    payload = {}
    if state_id is not None:
        payload["state_id"] = state_id
    if body is not None:
        payload["article"] = {
            "subject": "Actualizacion de ticket",
            "body": body,
            "type": "note",
            "internal": internal,
        }
    status, data = _request("PUT", f"/tickets/{ticket_id}", token, body=payload)
    if status != 200:
        raise RuntimeError(f"Error {status}: {data}")
    return data


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(1)
    cmd = sys.argv[1]
    token = get_token()

    if cmd == "search":
        args = [a for a in sys.argv[2:] if not a.startswith("--state")]
        state = None
        for a in sys.argv[2:]:
            if a.startswith("--state="):
                state = a.split("=", 1)[1]
        query = " ".join(args)
        print(json.dumps(search_tickets(token, query, state), ensure_ascii=False, indent=2))
    elif cmd == "get":
        print(json.dumps(get_ticket(token, sys.argv[2]), ensure_ascii=False, indent=2))
    elif cmd == "reply":
        ticket_id = sys.argv[2]
        internal = "--internal" in sys.argv[3:]
        body = " ".join(arg for arg in sys.argv[3:] if arg != "--internal")
        update_ticket(token, ticket_id, body=body, internal=internal)
        print(f"id={ticket_id} replied=True internal={internal}")
    elif cmd == "close":
        ticket_id = sys.argv[2]
        internal = "--internal" in sys.argv[3:]
        body_index = next((i for i, arg in enumerate(sys.argv[3:], start=3) if arg == "--body"), None)
        body = sys.argv[body_index + 1] if body_index is not None and body_index + 1 < len(sys.argv) else None
        closed_id = state_id_by_name(token, "closed")
        update_ticket(token, ticket_id, state_id=closed_id, body=body, internal=internal)
        print(f"id={ticket_id} closed=True")
    elif cmd == "delete":
        for tid in sys.argv[2:]:
            status = delete_ticket(token, tid)
            print(f"id={tid} status={status}")
    else:
        print(__doc__)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
