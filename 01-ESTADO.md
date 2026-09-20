# Estado

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
- [ ] `git push origin main` en este repo sigue sin completarse: el classifier ya deja pasar el intento, pero GitHub rechaza la deploy key de este repo por permiso de solo lectura (`salvabayonapascual/avs-zammad.git`) -- hay que darle permiso de escritura en GitHub, no es algo resoluble desde aqui. 2 commits locales listos esperando.
- [x] Creada skill `.skills/ninjaone-alertas-duplicadas/SKILL.md` (flujo completo: identificar en Zammad, investigar en SentinelOne, confirmar con el usuario, marcar y borrar) para repetir este proceso con otros equipos (empezando por TX2550M4).
- [x] `git push` resuelto (2026-09-14): la clave por defecto del equipo ya era deploy key de otro repo. Generada clave dedicada `id_ed25519_zammad`, alias `github.com-zammad-avs` en `~/.ssh/config`, remote actualizado y deploy key con permiso de escritura anadida en GitHub. Repo sincronizado con `origin/main`.
- [x] TX2550M4 (2026-09-14): borrados los 36 tickets Zammad del patron NinjaOne duplicado, a peticion expresa del usuario tras confirmar que queria borrarlos sin distincion. **Importante:** a diferencia de AVSP166, la investigacion en SentinelOne encontro que parte de este ruido corresponde a malware real sin remediar (`Formulario.exe`, `v2.1.6.zip`, veredicto `true_positive`, sigue detectandose hoy en un recurso compartido de red) -- no se marco nada como falso positivo en SentinelOne, el malware sigue activo en origen. Ver `15-MEMORIA-IA.md` 2026-09-14 15:40 CEST para el detalle y la proxima accion real (borrar el archivo del recurso compartido).

Detalle completo en `15-MEMORIA-IA.md` (entradas 2026-09-13 y 2026-09-14).

## Próxima acción recomendada

- [x] Generado token de acceso personal en Zammad (`api-avs-zammad-claude`, permisos admin+ticket.agent) para dejar de usar la contraseña en llamadas API. Ver `15-MEMORIA-IA.md` 2026-09-20.
- [ ] Decidir sobre los 36 tickets Zammad restantes y las detecciones SentinelOne de TX2550M4 (mismo patron que AVSP166, sin confirmar todavia).
- [ ] Corregir `Documentacion/Conexion/RCLONE.cmd`: referencia `id_rsa`, que no existe en este equipo (el acceso real usa `id_ed25519`).
- [ ] Completar `04-INVENTARIO.md` con el resto de datos técnicos del LXC (recursos, versión de Zammad, etc.).
