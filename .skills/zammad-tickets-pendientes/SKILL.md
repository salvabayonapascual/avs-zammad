---
name: zammad-tickets-pendientes
description: Listar y ordenar los tickets pendientes (no cerrados) de Zammad (https://zammad.avsconsulting.es). Usar cuando se pida ver, listar u ordenar los tickets pendientes/abiertos, o hacer triage de la cola de soporte.
---

# Listar tickets pendientes (Zammad)

Complementa a `.skills/zammad-api/SKILL.md` (auth y endpoints generales). Este skill es
el proceso concreto, ya validado, para obtener los tickets pendientes ordenados.

## Qué es "pendiente"

Estados de Zammad (`GET /api/v1/ticket_states`): `1=new`, `2=open`, `3=pending reminder`,
`4=closed`, `5=merged`, `6=pending close`. "Pendiente" = no cerrado ni fusionado:
`state_id` en `{1, 2, 3, 6}`.

## Credenciales

Están cifradas en `Documentacion/Privado/credenciales-zammad.md.enc` (+ `.key.enc`).
Desbloquear con TTL corto y volver a bloquear en cuanto termines de usarlas:

```
python "%USERPROFILE%\.config\obsidian-vault\secrets_tool.py" unlock --file "Documentacion/Privado/credenciales-zammad.md" --ttl 300
```

Esto imprime la ruta de un archivo temporal (fuera del repo). **Nunca leas ese archivo
con una herramienta que muestre su contenido en la respuesta** (ver reglas duras del
prompt de cifrado). Extrae usuario/contraseña con regex a variables de PowerShell y
constrúyelas el header `Authorization: Basic <base64(usuario:contraseña)>` sin imprimirlo:

```powershell
$temp = "<ruta impresa por unlock>"
$content = Get-Content -Raw -LiteralPath $temp
$user = [regex]::Match($content, 'Usuario:\s*(\S+)').Groups[1].Value
$pass = [regex]::Match($content, 'Contrase\S*:\s*(.+)').Groups[1].Value.Trim()
$b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes("$($user):$($pass)"))
$headers = @{ Authorization = "Basic $b64" }
```

Al terminar, vuelve a bloquear (aunque el TTL lo haría solo):

```
python "%USERPROFILE%\.config\obsidian-vault\secrets_tool.py" lock --file "Documentacion/Privado/credenciales-zammad.md"
```

Si ya existe un token de acceso personal generado (ver `.skills/zammad-api/SKILL.md`),
úsalo en vez de usuario/contraseña: `Authorization: Token token=<TOKEN>`.

## Query

Usar el endpoint de búsqueda, no `/api/v1/tickets` (ese solo pagina de 100 en 100 sin
filtro y hay que recorrer todas las páginas). `tickets/search` permite filtrar y ordenar
en el servidor, y `expand=true` devuelve nombres legibles (`state`, `priority`, `group`,
`customer`) en vez de solo ids:

```powershell
$query = 'state_id:1 OR state_id:2 OR state_id:3 OR state_id:6'
$uri = "https://zammad.avsconsulting.es/api/v1/tickets/search?query=$([uri]::EscapeDataString($query))&limit=300&sort_by=priority_id&order_by=desc&expand=true"
$result = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
```

`limit=300` cubre con margen el volumen visto hasta ahora (69 pendientes en 2026-09-13);
si algún día se acerca a ese límite, subirlo.

## Orden y presentación

Ordenar por prioridad (`3 high` > `2 normal` > `1 low`) y, dentro de la misma prioridad,
por `created_at` ascendente (el más antiguo primero, para priorizar lo que lleva más
tiempo sin atender):

```python
prio_rank = {"3 high": 0, "2 normal": 1, "1 low": 2}
data.sort(key=lambda t: (prio_rank.get(t["priority"], 9), t["created_at"]))
```

Presentar como tabla: número, fecha, grupo, asunto. Si hay muchas alertas automáticas
repetidas (patrón conocido: "alerta ninjaone TX2550M4 / <persona>", ver `01-ESTADO.md`
sobre el posible falso positivo recurrente de NinjaOne/SentinelOne para TX2550M4),
agruparlas/resumirlas en vez de listarlas una a una, y destacar aparte los tickets
distintos que sí requieren acción humana.

## Seguridad

- Nunca imprimir usuario/contraseña/token en la respuesta ni en la salida de un comando
  que se vaya a mostrar (ver `.skills/zammad-api/SKILL.md` → Seguridad).
- Borrar los archivos temporales con los resultados de la API al terminar
  (`$env:TEMP\zammad-*.json`), no dejarlos acumulándose entre sesiones.
