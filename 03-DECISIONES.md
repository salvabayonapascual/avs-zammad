# Decisiones

## 2026-08-30 — Eliminar tickets duplicados de alerta TX2550M4

Se eliminaron (borrado permanente, no cierre) los tickets #111253, #111251 y #111254, correspondientes a la misma alerta de NinjaOne/SentinelOne (cmd.exe marcado como Ransomware, Device ID 2837) generada por triplicado el 2026-08-30 en los grupos `@it` e `@incidencias`.

- **Motivo:** confirmado por el usuario que eran tickets a eliminar tras verificar por contenido (Threat ID, Device ID, fecha) que correspondían exactamente a las capturas mostradas.
- **Pendiente:** existen más tickets históricos con el mismo patrón para TX2550M4 (usuarios sbayona, KGOMEZ, 5S, JUANMA) en fechas previas, no eliminados. Evaluar si la detección es un falso positivo recurrente y ajustar la regla de origen (NinjaOne/SentinelOne) en vez de seguir borrando tickets manualmente.


## 2026-10-02 - Responsabilidad de @autorizaciones

Peticion explicita del usuario sobre #111373: Diego Liosi es propietario por defecto; Diego y Salva reciben seguimiento. Salva no responde hasta que le traspasen el ticket mediante reasignacion. Es un criterio operativo, no un bloqueo tecnico de respuesta: ambos necesitan permisos para gestionar el traspaso. No reasignar automaticamente a Diego en cada respuesta.


## GEN-017 — Calidad de arquitectura de contexto (2026-10-12 13:42)

Aplicación local expresamente confirmada del [[Clientes/AVS/general/ESTANDAR-ARQUITECTURA-CONTEXTO|Estándar GEN-017]]: entrada breve, carga selectiva, continuidad acotada/archivo íntegro, autorizaciones con precedencia, fuentes canónicas y evaluación/cierre. Reglas operativas propias conservadas en [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/02-METODO-TRABAJO|02-METODO-TRABAJO.md]]; no concede nuevas acciones sobre producción. GEN-017 prevalece sobre pautas locales antiguas de carga/archivo incompatibles. Validación documental en [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/10-VALIDACIONES|10-VALIDACIONES.md]]; comportamiento real de agentes pendiente de observar.

## GEN-018 — Proceso de calidad confirmado (2026-10-12 14:33)

Aplicadas las cinco mejoras autorizadas: validación reproducible, evaluación con ocho casos/hash y mínimo dos sesiones del mismo agente/modelo, tandas piloto con checkpoints atómicos, conservación verificable de reglas locales y guarda sin cambios redundantes. Fuente [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/CALIDAD-CONTEXTO|CALIDAD-CONTEXTO.md]]. Confirmación documental local; evaluación real de agentes sigue pendiente. No modifica hechos técnicos ni permisos del propietario.


## GEN-019 — Integración y evaluación (2026-10-12 15:06)

Confirmada aplicación local de hook sobre staging, evidencia estructurada/hash y revisión normativa GEN-019.1; fuente [[Clientes/AVS/general/PROCESO-EVALUACION-AGENTES|proceso GEN-019]]. Conservadas autorizaciones y reglas locales. La campaña aislada solo aplica a pilotos AVSP67/Passbolt/SentinelOne y mantiene el seguimiento observado pendiente. No se extrapolan resultados a este propietario sin pruebas.
