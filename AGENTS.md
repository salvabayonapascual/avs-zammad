# AGENTS.md — Zammad — AVS

Entrada canónica de este propietario. Aplicar [[Clientes/AVS/general/ESTANDAR-ARQUITECTURA-CONTEXTO|Estándar GEN-017]] y la doctrina GEN vigente de mando; este repo conserva solo su dominio y consulta otros propietarios al cruzar sistemas.

## Reglas esenciales

- Separar hechos comprobados, decisiones, pendientes y recomendaciones; citar fuente y fecha. No responder estado actual desde memoria o snapshots. Una fuente inaccesible produce dato no disponible, no cifras inventadas.
- Secretos sueltos solo cifrados y fuera de respuestas/logs; controles GEN-003/010. Excepciones expresas de backups según doctrina, nunca inferidas por ser un remoto privado.
- Una consulta no autoriza cambios, reinicios, borrados ni publicaciones. Respetar autorización concreta y excepciones permanentes verificadas del propietario; no ampliarlas. Ante ambigüedad, no ejecutar la acción dependiente.
- Antes de operar, leer [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/02-METODO-TRABAJO|método y reglas locales]] y [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/03-DECISIONES|decisiones vigentes]], y la skill/runbook específica. Conservar límites propios de seguridad, respaldo, ventana, identidad y host key.
- La autoridad GEN es de gobierno. Confirmar alineación aquí; no declarar aplicados criterios en otros repos por inferencia. Inventario/estado de otros dominios permanecen en sus propietarios.

## Inicio y carga selectiva

1. Fetch/status; si origin existe y está limpio y solo detrás, pull --ff-only. Preservar cambios ajenos y detener divergencias; sin remoto, no simular sincronización.
2. Leer [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/01-ESTADO|01-ESTADO.md]] y [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/07b-PREFERENCIAS-IA|preferencias]]; [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/15-MEMORIA-IA|15-MEMORIA-IA.md]] al retomar o si falta contexto reciente.
3. Cargar solo las fuentes de la intención según el router. No leer histórico completo ni activar tareas operativas por abrir el repo.

## Router

| Intención | Fuentes |
|---|---|
| Consulta/diagnóstico | Estado → inventario y sección de runbook/validación; consultar servicio vivo cuando corresponda |
| Cambio operativo | Método/reglas locales → decisiones → autorización y skill/runbook → evidencia comprobada |
| Cruce de sistemas | Registro/mapa del mando → fuentes de cada propietario |
| Arquitectura/documentación | Método → estándar GEN-017 → evaluación local y revisión del diff |
| Cierre | Guarda local → memoria breve → controles → commit/push o fallo explícito |

## Cierre y navegación

- Cuando haya trabajo o continuidad nuevos, actualizar memoria con fecha/hora, Tipo, tema, último contexto y siguiente acción; hasta cinco entradas, objetivo 120 líneas. Archivar íntegro en histórico local y conservar referencias a pendientes.
- Registrar pruebas en validaciones y actualizar estado si cambia, manteniendo fechas de hechos técnicos. No confundir revisión documental con comprobación viva.
- Ejecutar [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/PROCEDIMIENTO-GUARDA|guarda local]] al terminar cambios: diff revisado, controles locales, testigo/trailer si se exige, commit/push con identidad/remoto propios. No force/reset/amend ni cambios ajenos; fallos explícitos.
- Navegación interna con wikilinks completos desde C:/Datos; comprobar destinos y encabezados. Índice: [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/00-INDICE|00-INDICE.md]]; método: [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/02-METODO-TRABAJO|02-METODO-TRABAJO.md]]; evaluación: [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/10-VALIDACIONES|10-VALIDACIONES.md]].

## Calidad del proceso GEN-018

Seguir [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/CALIDAD-CONTEXTO|CALIDAD-CONTEXTO.md]]: validador versionado, controles locales, evaluación de agentes y cierre sin commits redundantes. Sin cambios ni continuidad nuevos, verificar sincronización; no editar memoria/testigo por un «guarda» repetido.

GEN-019: el hook comprueba staging; evidencias estructuradas y versión de reglas según [[Clientes/AVS/general/PROCESO-EVALUACION-AGENTES|proceso GEN-019]]. Mantener simulación y observación real diferenciadas.

Un diagnóstico técnico combinado se documenta en los propietarios afectados. En mando solo se guardan doctrina, seguimiento de gobierno y referencias; pedir «guarda» no autoriza copiar allí ese diagnóstico, estado ni inventarios.
