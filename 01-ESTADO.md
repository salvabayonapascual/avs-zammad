# Estado

> **Resumen rápido** · Última actualización: 2026-10-08
> **Alta:** ninguno abierto ahora mismo.
> **Media:** ninguno de los tres avisos revisados requiere intervención operativa. Los demás tickets se consultan en vivo, sin reutilizar el listado histórico de esta nota.
> **Ultimo cambio (2026-10-08):** corregido RCLONE y validado SFTP con identidad dedicada; licencia de #111121 saneada en cuerpo, HTML, MIME e índice, con copia cifrada recuperable; avisos @autorizaciones verificados en entradas reales y canal SMTP activo/OK. No se ha comprobado la recepción final en buzones. Montar Z: sigue requiriendo instalar WinFsp en este equipo; es una dependencia de la herramienta local, no un fallo del servicio. Evidencia en `10-VALIDACIONES.md`.
> Detalle completo más abajo.

## Situación actual

- [x] Accesos web y SSH del LXC registrados en `04-INVENTARIO.md`.
- [x] Credenciales de Zammad cifradas con cifrado de sobre: `Documentacion/Privado/credenciales-zammad.md.enc` + `.key.enc` (incluye login web y la clave SSH `id_ed25519` usada para el acceso root, ver `15-MEMORIA-IA.md` 2026-09-13).
- [x] API REST de Zammad verificada y documentada en la skill `.skills/zammad-api/`; nueva skill `.skills/zammad-tickets-pendientes/`.
- [x] Eliminados 3 tickets duplicados de alerta ransomware TX2550M4 del 2026-08-30 (ver `03-DECISIONES.md`).
- [x] Analizados los 69 tickets pendientes (2026-09-13): 46 son alertas NinjaOne duplicadas (TX2550M4/AVSP166), 23 distintos. Coordinado con SentinelOne: AVSP166 = 4 herramientas internas sin firmar, 26 detecciones, 8 sin resolver confirmadas por el usuario como falso positivo.
- [x] Token de acceso personal de Zammad creado (2026-09-20): `api-avs-zammad-claude`, permisos admin+ticket.agent, guardado cifrado. Ya no depende de la contraseña para llamadas API.

## Completado al reabrir sesión (2026-09-13, tras reinicio de VSCode)

- [x] SentinelOne: 8 amenazas AVSP166 marcadas `false_positive` + `resolved` (reintento tras bloqueo transitorio del classifier).
- [x] Zammad: 10 tickets AVSP166 borrados via API (ids internos 1249,1250,1259,1260,1261,1262,1264,1265,1272,1273 -- verificados contra su `number`/`title` antes de borrar).
- [x] Incidencia histórica de `git push origin main` cerrada el 2026-09-14; ver resolución y clave dedicada más abajo.
- [x] Creada skill `.skills/ninjaone-alertas-duplicadas/SKILL.md` (flujo completo: identificar en Zammad, investigar en SentinelOne, confirmar con el usuario, marcar y borrar) para repetir este proceso con otros equipos (empezando por TX2550M4).
- [x] `git push` resuelto (2026-09-14): la clave por defecto del equipo ya era deploy key de otro repo. Generada clave dedicada `id_ed25519_zammad`, alias `github.com-zammad-avs` en `~/.ssh/config`, remote actualizado y deploy key con permiso de escritura anadida en GitHub. Repo sincronizado con `origin/main`.
- [x] TX2550M4 (2026-09-14): borrados los 36 tickets Zammad del patron NinjaOne duplicado, a peticion expresa del usuario tras confirmar que queria borrarlos sin distincion. En su momento, la investigacion en SentinelOne encontro que parte de este ruido correspondia a malware real sin remediar (`Formulario.exe`, `v2.1.6.zip`, veredicto `true_positive`) -- no se marco nada como falso positivo en SentinelOne. Ver `15-MEMORIA-IA.md` 2026-09-14 15:40 CEST para el detalle original.
- [x] **[2026-09-20] CORREGIDO -- el malware SI se remedio, esta entrada estaba desactualizada:** `Formulario.exe` y `v2.1.6.zip` fueron borrados de verdad del recurso compartido el 2026-09-15 (SSH al servidor, verificacion de SHA1 exacto contra SentinelOne antes de borrar, confirmacion posterior de que ya no existen -- ver `SentinelOne/01-ESTADO.md` y `SentinelOne/15-MEMORIA-IA.md` de esa fecha). Re-verificado de nuevo el 2026-09-20 desde el proyecto SentinelOne (API sin detecciones nuevas desde el 15-09, sin exclusion de hash, y comprobacion SSH directa: los 3 archivos ya no existen en disco). Esta informacion en este repo llevaba 5 dias desactualizada porque nunca se actualizo tras la remediacion real -- si aparece una alerta o ticket nuevo citando estos archivos como malware activo, tratarlo como reinfeccion nueva y verificar contra SentinelOne antes de asumir que es residuo de este caso.

Detalle completo en `15-MEMORIA-IA.md` (entradas 2026-09-13 y 2026-09-14).

## Próxima acción recomendada

- [x] Generado token de acceso personal en Zammad (`api-avs-zammad-claude`, permisos admin+ticket.agent) para dejar de usar la contraseña en llamadas API. Ver `15-MEMORIA-IA.md` 2026-09-20.
- [x] **[2026-09-20] Limpieza de la nueva tanda de alertas NinjaOne duplicadas:** de 25 tickets abiertos con patrón `alerta ninjaone`, se cruzaron los 4 grupos (`AVSP165`, `AVSP97`, `TX2550M4` y el ticket suelto de fallo de parches) contra SentinelOne antes de decidir nada. Borrados 22 tickets confirmados `false_positive`/`resolved` en SentinelOne: `AVSP165` (2, caso `setup.exe` cerrado 16/09), `TX2550M4 / IDELAFUENTE` (16, `AVS_Toolbox.exe` sin firmar, mismo patrón recurrente de siempre), `TX2550M4 / MIGUEL` (2, `extendtext.exe`, fangame Pokémon) y `TX2550M4 / 5. AVS` (2, `EspacioGPT.exe`). Detalle e IDs en `15-MEMORIA-IA.md`.
- [x] **`AVSP97 / wsun` resuelto [2026-09-20]:** la amenaza (`2570452559632847061`) era `AnyDesk.exe`; el usuario confirmó que sigue en uso legítimo en AVS. Creada exclusión por hash en SentinelOne y marcada `resolved`/`false_positive` (ver `SentinelOne/03-DECISIONES.md` 2026-09-20). Tickets `111324` y `111323` borrados.
- [x] Ticket `111328` sobre aprobación de parches: API consultada el 2026-10-08, estado `closed`. No se modificó el ticket; el estado técnico del parcheo sigue perteneciendo a NinjaOne.
- [x] RCLONE corregido: rclone portable verificado, clave SFTP dedicada, claves públicas del servidor fijadas y comprobación real con `-CheckOnly`. No elimina configuraciones ni desmonta otras unidades.
- [x] Inventario básico verificado: es VM QEMU 110, con Zammad en Docker; no un LXC.
- [x] #111121: licencia saneada sin borrar ticket ni factura. Originales bajo cifrado local, fuera de Git; el índice ya no devuelve este ticket al buscar la clave.
- [x] @autorizaciones: avisos de creación/seguimiento a Diego y Salva registrados para #111384 y #111389; SMTP activo/OK, sin errores ni trabajos pendientes al verificar. Sin enviar pruebas.
- Herramienta opcional: instalar WinFsp con privilegios administrativos si se necesita montar Z:. El acceso SFTP está probado; el montaje no se ha realizado.
