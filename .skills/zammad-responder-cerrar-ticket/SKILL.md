---
name: zammad-responder-cerrar-ticket
description: "Use when the user asks to read, answer, update or close a Zammad ticket. Read it with `show` (accepts the visible number), draft the reply, SHOW THE EXACT TEXT AND WAIT FOR APPROVAL, send it by email with `email` (not `reply`, which only creates a note), verify, and optionally close only that ticket."
---

# Leer, responder y cerrar tickets Zammad

## Leer y responder a un usuario (flujo habitual)

**Regla (preferencia del usuario, `general/07b-PREFERENCIAS-IA.md`, 2026-10-02):** "contesta al ticket" autoriza a **preparar** la respuesta, no a enviarla. Siempre se muestra el texto completo y se espera la aprobación explícita antes de enviar.

1. **Leer** (acepta el número visible, p. ej. `111370`, o el id interno):
   ```
   python scripts/zammad_api.py show <numero> [--max-chars 1500]
   ```
   Muestra título, estado, grupo, cliente y la conversación limpia (sin el acuse automático).
2. **Redactar** el borrador en el tono del usuario: breve, cercano, en castellano, saludo con el nombre ("Hola Sergio:"), cierre corto ("Gracias.", "Un abrazo."). Sin firma: Zammad añade la del agente. No inventar datos ni compromisos que el usuario no haya dicho; si se añade algo propio (p. ej. el correo de otra persona sacado de otro ticket), decirlo al presentar el borrador.
3. **Mostrar y esperar aprobación.** Presentar en el chat: destinatario (correo), número y título del ticket, y el **texto exacto** tal cual se enviará. Preguntar también si después se deja abierto o se cierra. No enviar nada sin un "sí"/"envíalo" explícito; si el usuario corrige el texto, volver a mostrar la versión final antes de enviarla.
4. **Comprobar en seco** con el texto aprobado guardado en un fichero UTF-8 (así no se rompen acentos ni comillas):
   ```
   python scripts/zammad_api.py email <numero> --file <borrador.txt> --dry-run
   ```
   Cada línea en blanco del fichero separa un párrafo. Debe salir el mismo texto aprobado y el destinatario correcto.
5. **Enviar** el mismo fichero sin `--dry-run`. El comando crea un artículo de tipo `email`, visible, al cliente del ticket (o a `--to`), y verifica después que ha quedado como correo visible:
   ```
   python scripts/zammad_api.py email <numero> --file <borrador.txt>
   ```
6. **Informar** al usuario de lo enviado y del estado en que queda el ticket (al responder, Zammad suele pasarlo de `new` a `open`). Cerrar solo si lo pide (paso 7 del flujo de abajo). Borrar el fichero del borrador.

**Por qué `email` y no `reply`:** `reply` crea un artículo de tipo **nota**; aunque no sea interna, **no se envía por correo** al usuario. Detectado el 2026-09-30 al contestar los tickets #111357 y #111370, que hubo que enviar construyendo el correo a mano. `reply` queda para notas internas (`--internal`).

---

# Detalle: responder, anotar y cerrar

## Regla principal

El número visible del ticket (`number`, por ejemplo `111335`) no es el ID que
usan las operaciones de la API. Siempre hay que buscar primero y usar después
el `id` interno devuelto por Zammad.

## Excepción: herramientas internas AVS sin firma (no preguntar, decisión permanente 2026-09-23)

Para este caso concreto y acotado, el flujo de confirmación de más abajo **no aplica** — es la única excepción del skill. Antes de mostrar tickets pendientes, si el ticket corresponde a una herramienta interna AVS conocida (`Calculadora_CAEs`, `GeneradorContable`, `ConversorPDF`, `AVS_Toolbox`, `ProcesarNominas`, `EspacioGPT` u otra del mismo patrón — lista y criterio canónicos en `SentinelOne/03-DECISIONES.md`, no duplicar aquí):

1. Resolver el ID interno y leer el ticket; extraer threat id y ruta del cuerpo.
2. Verificar la firma en el detalle del threat de SentinelOne (no asumir del nombre) y la ruta exacta en el servidor con `Test-Path` (traducir de ruta de dispositivo NT a letra de unidad primero — ver `Servidor Primergy TX2550 M4.../_Sistema/13-COORDINACION-SYNOLOGY.md`).
3. Eliminar solo si `Test-Path` confirma que existe y la firma es inválida/ausente; nunca borrar por nombre parcial ni un archivo firmado.
4. Marcar la amenaza en SentinelOne (`true_positive`/`resolved`).
5. Añadir una nota interna indicando que estaba sin firmar y fue eliminado.
6. **Cerrar todos los tickets que compartan el mismo threat id** (puede haber varios duplicados por las reglas de enrutado `@it`/`@incidencias`), no solo el que se leyó primero — buscar el threat id en `pending` antes de dar el caso por cerrado.
7. Si hay cualquier ambigüedad (firma no verificable, ruta no confirmable, ejecutable no reconocido), no actuar sobre ese ticket y seguir con el flujo normal de confirmación de más abajo.

La prioridad/criticidad objetivo para estos tickets es baja y la categoría queda
sin categoría; si Zammad no ofrece esos valores, conservar el valor actual y
dejar constancia de la limitación.

## Flujo obligatorio, paso a paso

1. Resolver el ticket:

```powershell
python scripts\zammad_api.py search "<numero o titulo>" --state=all
```

2. Si hay más de una coincidencia, detenerse y pedir que se elija una. No
   actualizar por aproximación.

3. Leer el ticket por su ID interno:

```powershell
python scripts\zammad_api.py get <id_interno>
```

4. Confirmar objetivo, título, estado actual y contenido antes de responder.

5. Antes de cerrar, preguntar siempre al usuario:
  - ¿Quieres añadir una anotación interna?
  - ¿Quieres contestar públicamente al hilo de correo?
  - ¿Qué texto debe publicarse?
  - ¿Qué prioridad debe tener el ticket?
  - ¿Qué criticidad debe tener?
  - ¿Qué categoría debe tener?

  No cerrar ni publicar nada hasta recibir esta decisión. Si el usuario no
  quiere añadir nada, continuar sin artículo. Si prioridad, criticidad o
  categoría no se cambian, debe confirmarlo expresamente.

6. Publicar una respuesta al usuario o una nota interna, según se haya pedido.

Respuesta al usuario (correo): **siempre con el flujo de arriba** (borrador mostrado y aprobado, `email --dry-run`, `email`). No usar `reply` para esto: no envía correo.

Para nota interna:

```powershell
python scripts\zammad_api.py reply <id_interno> "<nota>" --internal
```

7. Si el usuario pide cerrar, cerrar el mismo ID después de verificar la
respuesta:

```powershell
python scripts\zammad_api.py close <id_interno>
```

Se puede añadir una nota de cierre:

```powershell
python scripts\zammad_api.py close <id_interno> --body "<resumen del cierre>" --internal
```

8. Volver a consultar el ticket y comprobar que su estado es `closed`.

## Reglas de seguridad

- Una acción por paso y esperar el resultado antes de seguir.
- No usar el número visible como si fuera el ID interno.
- No cerrar ni borrar un ticket distinto del confirmado.
- No inventar valores de prioridad, criticidad o categoría: consultar los
  valores disponibles en Zammad o conservar los actuales si el usuario lo
  confirma.
- Responder externamente solo cuando el usuario lo pida o el procedimiento lo
  determine; usar `--internal` para notas operativas.
- No imprimir, guardar ni pegar tokens o credenciales.
- El cliente API desbloquea temporalmente las credenciales cifradas y las
  vuelve a bloquear; no ejecutar `secrets_tool.py` manualmente salvo que el
  cliente falle.
- `delete` no forma parte del flujo normal de cierre y requiere una petición
  separada y explícita.

## Resultado esperado

Registrar el ID interno, número visible, respuesta publicada y estado final del
mismo ticket. Si la búsqueda, respuesta o cierre falla, detenerse y devolver el
error exacto sin intentar otra operación destructiva.
