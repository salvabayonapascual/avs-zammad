# Validaciones reales

| Fecha | Prueba | Estado | Evidencia | Siguiente paso |
|---|---|---|---|---|
| 2026-09-22 | Eliminación de `AVS_Toolbox.exe` y cierre del ticket #111334 | Aplicado | Verificado por SSH en TX2550M4: el archivo no estaba firmado y fue eliminado; `Test-Path` devolvió `False`. Ticket Zammad ID interno `1336`: anotación interna añadida y estado final `closed`; categoría sin categoría. La instancia mantuvo `priority_id=2` porque no ofrece prioridad baja configurable. | Aplicar en futuras alertas de AVS_Toolbox sin firmar: eliminar tras confirmación, anotar y preguntar antes del cierre por respuesta, prioridad, criticidad y categoría. |
| 2026-08-30 | Login web Zammad (Selenium) con `sat@nexo.net` | OK | Dashboard cargado tras login | — |
| 2026-08-30 | Acceso API REST vía HTTP Basic Auth (`GET /api/v1/users/me`) | OK (HTTP 200) | Respuesta 200 con `curl -u` | Preferir token personal en vez de contraseña para uso continuado |
| 2026-08-30 | Eliminación de tickets duplicados de alerta ransomware (falso positivo) TX2550M4 vía API (`DELETE /api/v1/tickets/:id`) | OK | Tickets #111253, #111251, #111254 verificados con HTTP 404 tras borrado | Revisar regla NinjaOne/SentinelOne para TX2550M4; hay más duplicados históricos sin limpiar |
