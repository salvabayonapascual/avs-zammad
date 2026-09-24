---
name: zammad-buscar-texto
description: Buscar una cadena de texto en los tickets de Zammad (titulo y cuerpo de los mensajes), con filtros por estado, grupo, categoria y fechas, y fragmento de contexto donde aparece. Usar cuando se pida "busca en Zammad...", "que tickets hablan de...", "cuando se compro/pidio...", o localizar un ticket por algo que se dijo dentro de el y no por su asunto.
---

# Buscar cadenas de texto en Zammad

Complementa a `.skills/zammad-api/SKILL.md` (auth y endpoints). El token se lee solo
desde las credenciales cifradas; no hace falta desbloquear nada a mano.

## Cuando usar `find` y no `search`

- `zammad_api.py search <texto>` busca **solo en el titulo** del ticket.
- `zammad_api.py find <texto>` busca en el **titulo y en el cuerpo de todos los
  mensajes** (indice de busqueda de Zammad). Es la opcion por defecto para "busca X":
  muchos datos (modelos, enlaces, nombres) solo aparecen dentro de los mensajes.
  Ejemplo real (2026-09-24): "ProBook" no esta en ningun titulo de la categoria
  "Compra material", pero `find` lo encuentra en 4 tickets.

## Uso

Desde la raiz de este repo:

```
python scripts/zammad_api.py find <texto> [--state new|open|closed|pending|all]
    [--group <grupo>] [--categoria <categoria>] [--since YYYY-MM-DD]
    [--until YYYY-MM-DD] [--limit N] [--snippets]
```

- `<texto>`: una palabra, varias palabras sueltas (se busca la frase exacta) o sintaxis de
  busqueda de Zammad: comodines (`portatil*`), `OR`/`AND`/`NOT`, frases entre comillas
  (`probook OR "galaxy book"`). Si lleva sintaxis se pasa tal cual y, con `--snippets`,
  cada termino se comprueba por separado.
  Sin texto (o `"*"`) se lista todo lo que cumpla los filtros, p. ej.
  `find --categoria "Compra material" --since 2026-07-01` (hace falta al menos un filtro).
- `--state pending`: new + open + pending reminder + pending close (lo no cerrado).
- `--group`: nombre exacto del grupo, con la arroba (`@it`, `@altasybajas`, `@calidad`,
  `@innovacion`, `@incidencias`).
- `--categoria`: campo personalizado "Categoria" (`Alta personal`, `Baja personal`,
  `Cambio de equipo`, `Compra material`, `Instalación - actualización`). **"Compra
  material" es una categoria, no un grupo.**
- `--since/--until`: por fecha de creacion del ticket, ambos incluidos (se traducen a
  `created_at:>=` / `<=`; Zammad devuelve 0 con rangos abiertos `[fecha TO *]`).
- `--snippets`: lee los mensajes de cada resultado y devuelve hasta 3 fragmentos
  (±100 caracteres) donde aparece la cadena, sin distinguir mayusculas ni acentos.
  Mas lento (una llamada por ticket): usarlo cuando haya que explicar *que* dice el
  ticket, no para un simple recuento.

Resultado: JSON ordenado del mas reciente al mas antiguo, con `id`, `number`, `title`,
`state`, `group`, `categoria`, `customer`, `created_at` y, con `--snippets`,
`literal` + `matches`.

## Antes de cambiar `find`

Ejecutar `python scripts/test_zammad_find.py` (solo lectura, contra tickets historicos
conocidos) antes y despues de tocar `find_tickets` o `_request`, y no subir el cambio si
falla algo. Cubre los fallos reales de la primera version: texto solo en el cuerpo,
`OR`/comodines, filtros de fecha, busqueda solo por filtros, snippets por termino y frase
con acento. Si se corrige un fallo nuevo, anadir su caso a ese script.

## Interpretar los resultados

- El indice de Zammad busca por palabras y con cierta tolerancia: puede devolver
  tickets donde la cadena exacta no esta. Con `--snippets`, `literal: false` marca esos
  casos; descartarlos o mencionarlos aparte, no presentarlos como coincidencias.
- No limitar a una categoria salvo que se pida: compras reales pueden estar sin categoria
  (p. ej. reenvios de pedidos de HP Store de 2025-11, sin `categoria`). Buscar en todo y
  despues agrupar.
- Una busqueda por titulo no basta para "listar las compras de X": revisar tambien los
  tickets de la categoria cuyo titulo no lo dice (p. ej. "ORDENADOR VMORALES" era un
  portatil). Combinar `find` con `--categoria` y leer los fragmentos.
- Presentar como tabla: numero, fecha, asunto y el dato buscado (del fragmento), del mas
  reciente al mas antiguo. Distinguir el objeto buscado de sus accesorios (un "cargador
  para portatil" no es una compra de portatil).
- `number` es el numero visible en Zammad; `id` es el interno que usan `get`, `reply`,
  `close` y `delete`.

## Seguridad

- Solo lectura: `find` no modifica ningun ticket.
- Los tickets contienen datos personales (telefonos, firmas de correo): en la respuesta,
  resumir y citar solo lo necesario; no volcar cuerpos enteros.
- No guardar los resultados en el repo; si se vuelcan a un fichero temporal, borrarlo al
  terminar.
