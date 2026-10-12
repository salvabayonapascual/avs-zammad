# Calidad del contexto — GEN-018

Aplicación local confirmada. Seguir [[Clientes/AVS/general/PROCESO-CALIDAD-CONTEXTO|proceso obligatorio]]; complementa GEN-017 y conserva autorizaciones/restricciones propias.

## Validación y cierre

```powershell
python "C:\Datos\Clientes\AVS\general\scripts\context_quality.py" --root "C:\Datos\Clientes\AVS\Valencia\Usuarios y equipos\Servidores\Cluster Proxmox\pve8.avs.local\VM\Zammad" --vault C:/Datos
```

Ejecutar antes del commit junto a controles locales de enlaces/texto/secretos. Fuente única del código en mando; si no está accesible, declarar control pendiente. `context-quality.json` en la raíz comprueba reglas locales mediante hashes de secciones y rutas; un cambio autorizado exige revisión explícita del manifiesto y fuente, nunca regenerarlo para ocultar fallos. Memoria: máximo cinco entradas y objetivo 120 líneas; entrada objetivo 80.

## Evaluación pendiente

`EVALUACION-AGENTES.json` en la raíz comienza vacío; no representa pruebas realizadas. Ocho casos Q-01 a Q-08 del proceso común. Para el hash vigente, deben pasar todos en al menos dos sesiones del mismo agente/modelo; usar evidencia propietaria y tipo observado/simulado. El último resultado de cada caso prevalece. Solo cobertura totalmente observada cierra cumplimiento observado; cualquier cambio de instrucciones requiere reevaluación. No ejecutar acciones de producción para probar permisos.

## Guarda sin duplicación

Si el árbol está limpio, no hay contexto nuevo y el cierre ya consta, verificar HEAD/remoto y comunicar hash existente; no editar memoria/testigo ni generar commit solo por «guarda». Con cambios o continuidad nuevos, cerrar con guarda y controles propios. Esta excepción GEN-018 prevalece sobre cierres anteriores indiscriminados.

## Navegación

- [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/00-INDICE|00-INDICE.md]]
- [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/02-METODO-TRABAJO|02-METODO-TRABAJO.md]]
- [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/10-VALIDACIONES|10-VALIDACIONES.md]]


## Integración obligatoria GEN-019

[[Clientes/AVS/general/PROCESO-EVALUACION-AGENTES|proceso GEN-019]]. `pre-commit` ejecuta `--staged`; si falta la fuente o falla calidad, bloquea sin saltarse otros controles. Manifiesto declara `policy_revision=GEN-019.1`. Evidencias: entrada, actuación/resultado real, criterio, evaluación/revisor y SHA-256; no aceptar un archivo existente sin integridad/contenido. Comentarios/docstrings del validador no cambian cobertura; cambios de lógica requieren revisión de impacto y pruebas. Evaluación aislada marcada `simulation`; seguimiento observado sigue pendiente.


GEN-020 obligatorio: [[Clientes/AVS/general/EVALUACION-ACCIONES-AGENTES|evaluación de acciones GEN-020]]. Acciones, variantes reservadas, revisión separada y carga selectiva; trazas locales en `Evaluaciones-GEN-020/`.
