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
