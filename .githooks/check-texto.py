"""Comprobaciones de texto antes de cada commit (GEN-010). Lo llama .githooks/pre-commit.

Bloquea el commit si un fichero de texto en staging:
  1. contiene caracteres de control (salvo tabulador, salto de linea, retorno de carro y salto de pagina);
     p. ej. un "\\a" interpretado como campana dentro de una ruta de Windows.
  2. cambia su estilo de finales de linea (CRLF <-> LF) respecto a HEAD: el texto no cambia pero Git
     muestra el fichero entero como modificado.

Motivo: ambos errores pasaron el 2026-09-26 al editar ficheros con scripts y llegaron a GitHub.
Si el cambio de finales de linea es intencionado: PERMITIR_CAMBIO_EOL=1 git commit ...

Es identico en todos los repos AVS; la copia de referencia vive en general/.githooks/check-texto.py.
"""
import os
import subprocess
import sys

TEXTO = (".md", ".py", ".ps1", ".psm1", ".txt", ".json", ".csv", ".toml", ".yml", ".yaml",
         ".sh", ".bat", ".cmd", ".html", ".css", ".js", ".ini", ".cfg", ".xml", ".rb")
PERMITIDOS = {9, 10, 12, 13}


def git(*args):
    return subprocess.run(["git", *args], capture_output=True)


def estilo(b):
    crlf = b.count(b"\r\n")
    lf = b.count(b"\n") - crlf
    if not crlf and not lf:
        return None
    return "CRLF" if crlf >= lf else "LF"


def main():
    nombres = [n for n in git("diff", "--cached", "--name-only", "--diff-filter=AM", "-z").stdout.split(b"\0") if n]
    problemas = []
    permitir_eol = os.environ.get("PERMITIR_CAMBIO_EOL") == "1"
    for n in nombres:
        nombre = n.decode("utf-8", "replace")
        if not nombre.lower().endswith(TEXTO):
            continue
        nuevo = git("show", ":" + nombre).stdout
        if b"\x00" in nuevo:          # UTF-16 u otro binario con extension de texto: no se analiza
            continue
        malos = sorted({c for c in nuevo if c < 32 and c not in PERMITIDOS})
        if malos:
            linea = next(i for i, l in enumerate(nuevo.split(b"\n"), 1) if any(c in l for c in bytes(malos)))
            problemas.append(f"{nombre}: caracter(es) de control {', '.join(hex(c) for c in malos)} (linea {linea})")
        anterior = git("show", "HEAD:" + nombre)
        if anterior.returncode == 0 and not permitir_eol:
            a, b = estilo(anterior.stdout), estilo(nuevo)
            if a and b and a != b:
                problemas.append(f"{nombre}: finales de linea {a} -> {b} (si es a proposito: PERMITIR_CAMBIO_EOL=1)")
    if problemas:
        print("Commit bloqueado por check-texto (GEN-010):", file=sys.stderr)
        for p in problemas:
            print("  - " + p, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
