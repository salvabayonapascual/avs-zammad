# Decisiones

## 2026-08-30 — Eliminar tickets duplicados de alerta TX2550M4

Se eliminaron (borrado permanente, no cierre) los tickets #111253, #111251 y #111254, correspondientes a la misma alerta de NinjaOne/SentinelOne (cmd.exe marcado como Ransomware, Device ID 2837) generada por triplicado el 2026-08-30 en los grupos `@it` e `@incidencias`.

- **Motivo:** confirmado por el usuario que eran tickets a eliminar tras verificar por contenido (Threat ID, Device ID, fecha) que correspondían exactamente a las capturas mostradas.
- **Pendiente:** existen más tickets históricos con el mismo patrón para TX2550M4 (usuarios sbayona, KGOMEZ, 5S, JUANMA) en fechas previas, no eliminados. Evaluar si la detección es un falso positivo recurrente y ajustar la regla de origen (NinjaOne/SentinelOne) en vez de seguir borrando tickets manualmente.
