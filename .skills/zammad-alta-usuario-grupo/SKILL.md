---
name: zammad-alta-usuario-grupo
description: Crear o completar usuarios de Zammad con rol y grupo independiente, evitando duplicados y validando el alcance real de permisos.
---

# Alta de usuario y grupo en Zammad

Usar al solicitar una cuenta de Zammad o acceso separado a tickets.

## Flujo

1. Confirmar nombre, correo, rol, nombre exacto del grupo y si el acceso será `full`, `read` o `change`.
2. Consultar `/users/search` por correo/login y `/groups` por nombre exacto. No crear duplicados.
3. Si el usuario existe, modificar solo los campos necesarios; conservar sus roles y grupos no relacionados.
4. Crear el grupo únicamente si no existe. Para un grupo privado de una persona, usar un nombre inequívoco como `@Nombre Apellidos`.
5. Para trabajar tickets, asignar el rol de agente (`Agent`) además del rol cliente solo si está autorizado. Nunca conceder `admin` por comodidad.
6. Asignar al usuario únicamente al grupo solicitado con el permiso indicado; no añadirlo a `@it` ni a otros grupos por similitud.
7. Validar con lecturas independientes de `/users/:id` y `/groups/:id`: usuario activo, roles, `group_ids`, grupo activo y `user_ids`.
8. Indicar al usuario que acceda a la URL normal de Zammad y use recuperación de contraseña si no tiene una. Confirmar funcionalmente el primer acceso cuando sea posible.

## Seguridad y cierre

- Usar `.skills/zammad-api/SKILL.md` y `scripts/zammad_api.py`; el token nunca aparece en salida ni documentación.
- No guardar contraseñas, enlaces de recuperación ni tokens.
- Registrar en `10-VALIDACIONES.md` el usuario, grupo, rol y alcance, sin secretos; actualizar memoria según el límite de cinco entradas.
- Cerrar con el procedimiento de guarda, revisión de diff, commit y push.
