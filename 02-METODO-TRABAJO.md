# Método de trabajo

## Calidad de contexto GEN-017

**Aplicación local confirmada:** 2026-10-12 13:42. [[Clientes/AVS/general/ESTANDAR-ARQUITECTURA-CONTEXTO|Estándar GEN-017]] prevalece sobre instrucciones de carga/archivo anteriores; los límites y autorizaciones operativas específicas siguen vigentes.

### Carga selectiva

Entrada: AGENTS, [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/01-ESTADO|01-ESTADO.md]] y [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/07b-PREFERENCIAS-IA|preferencias]]; memoria reciente si se retoma o falta contexto. Consulta: inventario y fuente técnica del propietario. Diagnóstico: sección pertinente de runbook/validaciones. Cambio: decisiones, autorización y procedimiento concreto. Cruce: propietarios indicados por mando. Histórico solo por tema/fecha, sin leerlo entero al iniciar. Una evidencia documental no es estado vivo.

### Autorizaciones y precedencia

- Una lectura/diagnóstico no autoriza cambiar producción. Para cambios sin autorización concreta, explicar consecuencias, afectados, duración, respaldo y rollback antes de confirmar.
- Publicar tickets/correos/mensajes exige aprobar el texto completo, salvo una excepción permanente explícita que cubra exactamente esa publicación. Consultar las decisiones vigentes y el procedimiento propietario; no importar permisos de otros sistemas.
- Las excepciones conservan condiciones, comprobaciones y límites. Ante ambigüedad, detener la acción dependiente y continuar las lecturas útiles. Las instrucciones explícitas posteriores del usuario prevalecen.
- GEN-017 cambia la arquitectura documental, no accesos, servicios ni autorizaciones técnicas. El guarda automático cubre solo cambios propios revisados; operaciones destructivas y diffs inesperados requieren confirmación.

### Memoria breve y conservación

[[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/15-MEMORIA-IA|15-MEMORIA-IA.md]] conserva continuidad y hasta cinco entradas completas, objetivo máximo 120 líneas. Al exceder el presupuesto, trasladar íntegros texto y fechas a [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/08-HISTORICO|08-HISTORICO.md]]; comprobar conservación y dejar referencias a siguientes acciones aún relevantes. Si una entrada sola excede el límite, archivarla y dejar resumen/ref. Preferencias estables en su fuente, decisiones en [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/03-DECISIONES|03-DECISIONES.md]], pendientes en [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/01-ESTADO|01-ESTADO.md]], pruebas en [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/10-VALIDACIONES|10-VALIDACIONES.md]]. No duplicar entradas ni usar pendientes históricos como vigentes sin verificar.

### Fuentes y evaluación

Alcance propio en inventario; registro de repos/remotos en mando. [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/07-CONTEXTO|07-CONTEXTO.md]] e índice enlazan fuentes, sin copiar listas/recuentos actuales. Conservar inventarios técnicos legítimos, hechos históricos y evidencias originales. Si falla la fuente viva, indicar dato no disponible; no sustituirlo por memoria ni cero.

Aplicar los casos locales de [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/10-VALIDACIONES|10-VALIDACIONES.md]]: consulta, fallo de fuente, cruce, autorización/publicación, ambigüedad, gobierno, memoria/navegación y cierre. Separar revisión estática, simulación y prueba real; no actuar en producción para probar autorizaciones.

### Guarda y controles

Ejecutar [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/PROCEDIMIENTO-GUARDA|guarda local]] al terminar cambios propios: revisar diff, memoria/estado del alcance y controles locales de enlaces, texto, secretos y pruebas pertinentes. Conservar identidad, rama, remoto, testigo y trailers exigidos. Commit y push normal, contrastando HEAD remoto; sin remoto, commit local y limitación explícita. Un commit, lanzamiento o componente instalado no acredita éxito operativo.



1. Consultar estado e inventario antes de actuar.
2. Registrar decisiones antes de cambios de criterio.
3. Ejecutar o actualizar un runbook cuando aplique.
4. Registrar la validación real y el cierre de sesión.


## Reglas locales conservadas desde la entrada

Cargar la sección pertinente antes de operar; las decisiones actuales prevalecen sobre ejemplos o referencias históricas.

### Reglas

- No registrar ni exponer secretos, contraseñas, tokens o claves privadas.
- Separar hechos, decisiones, pendientes y recomendaciones.
- No mover ni borrar contenido sin confirmación explícita.
- Registrar pruebas reales en [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/10-VALIDACIONES|10-VALIDACIONES]].
- Al cerrar una sesión, actualizar [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/15-MEMORIA-IA|15-MEMORIA-IA]].

### Navegación

[[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/00-INDICE|Índice]] · [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/01-ESTADO|Estado]] · [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/PROCEDIMIENTO-GUARDA|Guarda]]

Publicación: mostrar el texto completo y obtener aprobación antes de enviar respuestas o correos. La excepción de cierre de triage interno sin firma procede solo de la autorización vigente en SentinelOne y mando, con asociación del threat/ticket comprobada. Respetar además el criterio vigente de @autorizaciones sobre titularidad y reasignación; no enviar por una mera consulta.

## Proceso reproducible GEN-018

Aplicar [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/CALIDAD-CONTEXTO|CALIDAD-CONTEXTO.md]] y [[Clientes/AVS/general/PROCESO-CALIDAD-CONTEXTO|proceso común]] antes de cerrar cambios. Validación versionada, evaluación con cobertura/hash, reglas locales verificadas y tandas piloto reanudables. GEN-018 introduce cierre sin escrituras redundantes: sin cambios ni continuidad nuevos, comprobar sincronización y conservar memoria/testigo existentes. No amplía permisos operativos ni permite omitir controles en cambios reales. Las reglas específicas anteriores permanecen vigentes.


## Integración y evidencias GEN-019

Aplicar [[Clientes/AVS/general/PROCESO-EVALUACION-AGENTES|proceso GEN-019]]: hook obligatorio sobre el índice Git, evidencia JSON estructurada con hash y revisión, y versión normativa GEN-019.1 separada del mantenimiento del validador. No omitir controles locales. Campañas aisladas = simulación; no equivalen a cumplimiento observado en producción.

Un diagnóstico técnico combinado se documenta en los propietarios afectados. En mando solo se guardan doctrina, seguimiento de gobierno y referencias; pedir «guarda» no autoriza copiar allí ese diagnóstico, estado ni inventarios.
