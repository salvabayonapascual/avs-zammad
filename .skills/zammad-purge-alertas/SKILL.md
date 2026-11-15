# Skill: zammad-purge-alertas

Borrado masivo de tickets de Zammad que comparten un patron en el cuerpo
(p. ej. alertas NinjaOne repetitivas de un mismo ejecutable o amenaza).

## Cuando usarla

El usuario pide eliminar todas las alertas de Zammad que contengan un texto
concreto (nombre de ejecutable, ruta, threat ID, etc.), incluyendo historico.

## Procedimiento

1. **Dry-run** — ejecutar desde el repo Zammad:

   ```
   python scripts/zammad_api.py purge <consulta_indice> --body-contains "<texto_literal>" --state all --dry-run
   ```

   - `<consulta_indice>`: termino que el indice de Zammad SI indexa y que
     prefiltra candidatos (p. ej. `Persistence`, `Keep Access`, nombre de
     equipo). Usar `*` con un filtro (`--state`, `--group`, `--since`) si
     no hay un buen termino indexable.
   - `--body-contains`: texto literal que DEBE aparecer en el cuerpo del
     ticket (post-filtro local, insensible a mayusculas/acentos). Aqui va
     el valor que el indice no tokeniza (p. ej. `InstaladorFirma_AVS`).

2. **Revisar la salida** — confirmar que los tickets listados son correctos.

3. **Ejecutar sin dry-run**:

   ```
   python scripts/zammad_api.py purge <consulta_indice> --body-contains "<texto_literal>" --state all
   ```

4. **Verificar** — repetir el dry-run; debe devolver 0 tickets.

## Filtros opcionales

- `--state new|open|closed|pending|all` (por defecto: todos los estados)
- `--group <grupo>` (p. ej. `@it`, `@incidencias`)
- `--since YYYY-MM-DD` / `--until YYYY-MM-DD`
- `--limit N` (por defecto 200)

## Ejemplo real

Eliminar todas las alertas de InstaladorFirma:

```
python scripts/zammad_api.py purge Persistence --body-contains InstaladorFirma --state all --dry-run
python scripts/zammad_api.py purge Persistence --body-contains InstaladorFirma --state all
```

## Notas

- `purge` usa `find` internamente con `--body-contains` para post-filtrar.
- El indice de Zammad no tokeniza bien palabras con underscores ni rutas
  Windows; por eso el filtro local es imprescindible.
- `delete` en la API de Zammad es permanente e incluye el historico.
