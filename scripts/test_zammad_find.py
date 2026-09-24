"""Pruebas de `find_tickets` contra la instancia real de Zammad (solo lectura).

Ejecutar antes de subir cualquier cambio de `zammad_api.py`:

    python scripts/test_zammad_find.py

Usa tickets historicos cerrados como referencia fija (ver 15-MEMORIA-IA.md,
2026-09-24): los recuentos se comprueban como "contiene al menos estos",
no como numero exacto, porque la categoria sigue creciendo.
Cada caso cubre un fallo real que la primera version de `find` tenia.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zammad_api as z  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
token = z.get_token()
failures = []


def check(name, cond, detail=""):
    print(("OK   " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)


def numbers(results):
    return {r["number"] for r in results}


# 1. Texto que solo aparece en el cuerpo de los mensajes, no en el titulo
r = z.find_tickets(token, "ProBook", categoria="Compra material")
check("cuerpo de mensajes: ProBook en Compra material",
      {"11744", "11865", "11887", "11779"} <= numbers(r), sorted(numbers(r)))

# 2. Consulta con OR y comodines (antes se envolvia como frase exacta -> 0)
r = z.find_tickets(token, "portatil* OR laptop*", limit=200)
check("OR + comodines devuelve resultados", len(r) > 0 and "111158" in numbers(r), len(r))

# 3. Filtro de fechas (antes usaba [fecha TO *] -> 0)
r = z.find_tickets(token, "portatil*", since="2025-06-01", limit=200)
check("--since devuelve resultados", len(r) > 0, len(r))
check("--since excluye lo anterior", all(x["created_at"] >= "2025-06-01" for x in r))
r = z.find_tickets(token, "portatil*", since="2026-03-01", until="2026-03-31", limit=200)
check("--since/--until acotan a marzo 2026",
      len(r) > 0 and all("2026-03-01" <= x["created_at"] <= "2026-03-31" for x in r), len(r))

# 4. Solo filtros, sin texto (antes '(*)' -> 0)
r = z.find_tickets(token, "", categoria="Compra material", since="2026-07-01")
check("sin texto, solo filtros", {"111158", "111165"} <= numbers(r), sorted(numbers(r)))
try:
    z.find_tickets(token, "")
    check("sin texto ni filtros se rechaza", False)
except SystemExit:
    check("sin texto ni filtros se rechaza", True)

# 5. Snippets: cada termino por separado y marca literal
r = z.find_tickets(token, "probook OR elitebook", categoria="Compra material", snippets=True)
t11744 = next((x for x in r if x["number"] == "11744"), None)
check("snippets con OR: 11744 literal", bool(t11744 and t11744["literal"] and t11744["matches"]))

# 6. Frase exacta de varias palabras
r = z.find_tickets(token, "llega mañana", categoria="Compra material", snippets=True)
check("frase exacta con acento", len(r) > 0 and any(x["literal"] for x in r), len(r))

print()
print(f"{len(failures)} fallos" if failures else "Todas las pruebas OK")
sys.exit(1 if failures else 0)
