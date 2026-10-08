# Validaciones reales

| Fecha | Prueba | Estado | Evidencia | Siguiente paso |
|---|---|---|---|---|
| 2026-09-22 | Eliminación de `AVS_Toolbox.exe` y cierre del ticket #111334 | Aplicado | Verificado por SSH en TX2550M4: el archivo no estaba firmado y fue eliminado; `Test-Path` devolvió `False`. Ticket Zammad ID interno `1336`: anotación interna añadida y estado final `closed`; categoría sin categoría. La instancia mantuvo `priority_id=2` porque no ofrece prioridad baja configurable. | Aplicar en futuras alertas de AVS_Toolbox sin firmar: eliminar tras confirmación, anotar y preguntar antes del cierre por respuesta, prioridad, criticidad y categoría. |
| 2026-08-30 | Login web Zammad (Selenium) con `sat@nexo.net` | OK | Dashboard cargado tras login | — |
| 2026-08-30 | Acceso API REST vía HTTP Basic Auth (`GET /api/v1/users/me`) | OK (HTTP 200) | Respuesta 200 con `curl -u` | Preferir token personal en vez de contraseña para uso continuado |
| 2026-08-30 | Eliminación de tickets duplicados de alerta ransomware (falso positivo) TX2550M4 vía API (`DELETE /api/v1/tickets/:id`) | OK | Tickets #111253, #111251, #111254 verificados con HTTP 404 tras borrado | Revisar regla NinjaOne/SentinelOne para TX2550M4; hay más duplicados históricos sin limpiar |


## 2026-10-02 11:40 - Grupo @autorizaciones (ticket #111373)

**Tipo:** Sesion / configuracion
**Estado:** Aplicado; recepcion final en buzones pendiente de comprobar con una entrada real.

- Grupo 6 `@autorizaciones`, activo; direccion/sig de soporte existentes (email_address_id=1, signature_id=1), miembros Diego Liosi (5) y Salvador Bayona Pascual (8), ambos full. Se conservaron los permisos de los demas grupos.
- Trigger 11 `Asunto @autorizaciones`: en creacion con asunto que contiene @autorizaciones, enruta al grupo 6 y asigna Diego. Trigger 12: alta directa en grupo 6 sin propietario tambien asigna Diego.
- Triggers 13 y 14: suscriben respectivamente Diego y Salva a los tickets del grupo. Preferencias existentes verificadas: ambos tienen email y online para create/update en propios y suscritos. No se cambiaron las preferencias globales.
- Filtro de correo 6: asunto que empieza por @autorizaciones, grupo 6. No fuerza propietario en seguimientos: respeta el traspaso manual a Salva.
- Prueba real #111376 (id 1378), nota interna: creado inicialmente en @it con asunto @autorizaciones; resultado grupo 6, owner 5. GET mentions confirma usuarios 5 y 8. PUT owner 8 y posterior nota conservan owner 8. Cerrado state_id=4 tras la prueba.
- No se envio una respuesta a Diego ni se cerro #111373. La configuracion de avisos y las suscripciones estan verificadas; no se afirma entrega final a ambos buzones. No fue posible consultar logs por SSH: autenticacion rechazada con la clave disponible.
- Cambio local previo en scripts/zammad_api.py preservado y excluido de este guarda.

**Siguiente accion:** comprobar la recepcion de un correo real con asunto @autorizaciones en dliosi@avsconsulting.es y sat@nexo.net. Diego atiende inicialmente; Salva interviene al recibir la reasignacion.

## 2026-10-08 18:05 CEST — Reducción de avisos repetidos

- **RCLONE:** ejecutado `powershell -NoProfile -ExecutionPolicy Bypass -File Documentacion/Conexion/montar-zammad.ps1 -CheckOnly`; salida 0, SFTP verificado con identidad dedicada y claves de host fijadas desde SSH autenticado. rclone v1.75.1 descargado de la fuente oficial, SHA256 del ZIP contrastado con SHA256SUMS. No se montó Z: porque WinFsp no está instalado; no se desmontaron unidades ni se reescribieron remotes.
- **SyncBack #111121 (1123), artículo 4032:** simulación y aplicación de `scripts/sanear_licencia_syncback.py --apply`. Copia cifrada recuperable verificada antes del cambio; transacción de cuerpo y Store 10663/10664, sin borrados. Lectura posterior independiente: licencia ausente del cuerpo, HTML y partes MIME; búsqueda de la clave sin este ticket. IDs de adjuntos y hashes de imágenes/factura conservados, checksums de almacenamiento correctos. Ticket sigue cerrado.
- **@autorizaciones:** consulta viva de grupo 6, usuarios 5/8, suscripciones e historial de #111384 (1386) y #111389 (1391). Ambos destinatarios constan en avisos de creación online/email: 2026-10-06 08:36:58/08:37:00 UTC y 2026-10-07 10:56:46/10:56:48 UTC. También consta seguimiento. Canal Email::Notification 1 activo, SMTP, status_out=ok, sin error; cola Delayed::Job vacía. Ejecuciones reales completadas sin avisos de error en las ventanas consultadas. No se cambió configuración ni se enviaron correos de prueba.
- **Límite de evidencia:** comprobación de avisos en servidor, no acceso a los buzones finales de Diego/Salva. No se eleva como incidencia una recepción no confirmada sin indicios de fallo; si el usuario informa de ausencia, investigar entonces correo destino/spam.
- Evidencia saneada: `Documentacion/Validaciones/2026-10-08-saneamiento.json`. Original cifrado local: referencia en `13-SEGURIDAD-Y-PRIVADO.md`; ninguna licencia/token/clave privada versionada.
- Inventario básico contrastado con recursos Proxmox y `docker ps`; corregida la identificación LXC por VM.
- #111328 (1330): búsqueda API en vivo confirma `closed`; retirada su marca de pendiente documental sin modificar el ticket ni afirmar resolución técnica en NinjaOne.
