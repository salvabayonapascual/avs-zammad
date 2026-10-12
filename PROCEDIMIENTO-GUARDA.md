# Procedimiento `guarda`

## Calidad de cierre GEN-017

Este flujo se activa también al terminar cambios documentales autorizados, conforme al guarda automático de mando. Aplicar memoria breve/conservación y evaluación de [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/02-METODO-TRABAJO|02-METODO-TRABAJO.md]]. Preservar la identidad, rama y origin actuales; publicar solo el alcance revisado, sin force/reset/amend. Si no existe remoto, guardar commit local y comunicar que no está publicado, sin crear un remoto por inferencia.


1. Revisar el estado del repositorio.
2. Confirmar que no se incluyen secretos ni material privado.
3. Validar el alcance de los cambios.
4. Actualizar `15-MEMORIA-IA.md` al cerrar una sesión.
5. Crear commits por unidad lógica y publicar solo cuando corresponda.
