---
name: ninjaone-alertas-duplicadas
description: Resolver el patron de tickets Zammad duplicados "alerta ninjaone <equipo> / <persona>" para un equipo concreto -- investigar en SentinelOne, decidir con el usuario si son falso positivo, y limpiar Zammad + SentinelOne. Usar cuando se pida limpiar, resolver o eliminar tickets/alertas NinjaOne duplicadas de un equipo especifico (p. ej. "limpia los duplicados de AVSP166", "resuelve las alertas de TX2550M4").
---

# Alertas NinjaOne duplicadas (Zammad + SentinelOne)

Complementa a `.skills/zammad-tickets-pendientes/SKILL.md` (que lista/ordena, pero no
decide ni actua) y a `SentinelOne/.github/skills/sentinelone-eliminar-amenazas/SKILL.md`
(que es para amenazas CONFIRMADAS maliciosas, no para esto). Este skill es el flujo
validado de principio a fin, ejecutado por primera vez el 2026-09-13 para `AVSP166`
(ver `15-MEMORIA-IA.md` de esa fecha).

## Por que existe este patron

El LXC `correos-ninjaone` (192.168.150.240, ver `C:\Datos\Clientes\AVS\NinjaOne\07-CONTEXTO.md`)
traduce actividades de NinjaOne a correos a `soporte@avsconsulting.es`, que Zammad convierte
en tickets con asunto literal `@it alerta ninjaone <equipo> / <persona>` o
`@incidencias alerta ninjaone <equipo> / <persona>`. Si el equipo tiene amenazas SentinelOne
activas sin resolver, el LXC sigue generando alertas nuevas indefinidamente -- limpiar solo
Zammad sin tocar SentinelOne no soluciona nada, vuelve a llenarse.

## Flujo

### 1. Identificar candidatos en Zammad (equipo concreto, no todos)

Reusar la query de `.skills/zammad-tickets-pendientes/SKILL.md` (estados no cerrados:
`state_id:1 OR state_id:2 OR state_id:3 OR state_id:6`, `expand=true`) y filtrar por
`alerta ninjaone <EQUIPO>` en el titulo. No mezclar equipos distintos en la misma
confirmacion/borrado.

### 2. Investigar en SentinelOne (solo lectura)

```
cd C:\Datos\Clientes\AVS\SentinelOne
python scripts\sentinelone_api.py threats <EQUIPO>
```

Agrupar resultados por `sha1`/`filePath` (no por threatId suelto -- el mismo archivo genera
IDs de amenaza distintos cada vez, ver aprendizaje critico en `NinjaOne/07-CONTEXTO.md`).
Para cada grupo, anotar: `classification`, `confidenceLevel`, `incidentStatus`,
`analystVerdict`, si ya tiene `mitigationStatus` (kill/quarantine/remediate) con exito.

### 3. Clasificar cada grupo -- nunca asumir falso positivo sin evidencia

- Si ya existe un informe o decision registrada (buscar el nombre del archivo/hash en
  `SentinelOne/01-ESTADO.md`, `SentinelOne/Documentos/PDF/*`, o entradas ya
  `analystVerdict: false_positive` para el mismo hash): tratar igual, es continuidad de un
  patron ya decidido.
- Si es una herramienta interna de AVS sin firmar (ruta tipica bajo
  `...\PROGRAMAS\...\dist\*.exe`, developer conocido) y coincide con el patron ya descrito
  en `SentinelOne/01-ESTADO.md` ("AVS Toolbox sin resolver" / propuesta de firma de codigo
  interna): es candidato razonable a falso positivo, pero **presentar el desglose completo
  al usuario y pedir confirmacion explicita antes de marcar nada** -- no decidir solo.
- Señalar aparte, con mas cautela, cualquier grupo con `confidenceLevel: malicious` (no solo
  `suspicious`) o que ya tenga acciones de mitigacion reales ejecutadas (kill/quarantine) --
  es una senal mas fuerte de que el propio SentinelOne lo trato como amenaza real, no ruido.
- Si no hay patron previo ni evidencia clara: no asumir nada, decir al usuario que hace
  falta investigar (hash, ruta, comportamiento) antes de decidir.

### 4. Marcar en SentinelOne (solo los grupos confirmados por el usuario)

```
python scripts\sentinelone_api.py resolve-false-positive <id1> <id2> ...
```

Solo los `threatId` que sigan `incidentStatus: unresolved` (los ya `resolved`/`false_positive`
de sesiones previas no hace falta tocarlos). Guardar la lista de IDs usados en la nota de
cierre de sesion, por si el bloqueo de escritura obliga a reintentar mas tarde.

### 5. Borrar los tickets Zammad correspondientes

Los tickets se identifican por `number` (el visible, p. ej. `111247`) pero la API de
borrado necesita el `id` interno -- **nunca borrar usando el `number` directamente**
(`DELETE /api/v1/tickets/<number>` da 404 silencioso-ish, no es el mismo recurso). Resolver
primero:

```
GET /api/v1/tickets/search?query=number:111247 OR number:111248 ...
```

Verificar que `id`->`number`->`title` coincide con la lista confirmada por el usuario antes
de borrar (dejar esa tabla de verificacion visible en la conversacion, no solo en memoria),
y despues:

```
DELETE /api/v1/tickets/<id>
```
para cada uno. Credenciales via `secrets_tool.py unlock --ttl 300` / `lock` inmediatamente
despues, nunca imprimir usuario/contraseña (ver `.skills/zammad-api/SKILL.md`).

### 6. Registrar

Actualizar `01-ESTADO.md` y `15-MEMORIA-IA.md` de este repo (que, equipo, cuantos tickets,
cuantas amenazas, IDs usados). Si la decision cierra un pendiente listado en
`SentinelOne/01-ESTADO.md` (como la fila "Alta | Pendiente | AVS Toolbox sin resolver"),
señalarlo explicitamente para que se pueda marcar como resuelto alli tambien.

## Reglas duras

- Nunca mezclar equipos en una misma tanda de confirmacion: cada equipo (`TX2550M4`,
  `AVSP166`, etc.) es una decision separada, aunque el patron de ticket sea identico.
- Nunca decidir "es falso positivo" sin mostrar el desglose completo (hash, clasificacion,
  confianza, mitigaciones ya ejecutadas) y obtener confirmacion explicita del usuario.
- Nunca borrar un ticket Zammad usando su `number` como si fuera el `id` de la API.
- Nunca imprimir usuario/contraseña/token de Zammad ni de SentinelOne en la respuesta.
- Si una llamada de escritura (SentinelOne o Zammad) es bloqueada por el classifier de
  auto-mode del entorno, reintentar una vez (a veces es transitorio) antes de darla por
  bloqueada de verdad y pedir al usuario que ajuste permisos.
