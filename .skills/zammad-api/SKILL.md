---
name: zammad-api
description: Acceder a la API REST de Zammad (https://zammad.avsconsulting.es) para consultar o gestionar tickets, usuarios, grupos, organizaciones, etc. Usar cuando se pida interactuar con Zammad sin usar la interfaz web (listar tickets, crear/actualizar tickets, consultar usuarios, automatizar tareas).
---

# API de Zammad (AVS Valencia)

## Datos del servicio

- Base URL API: `https://zammad.avsconsulting.es/api/v1`
- Documentación oficial: https://docs.zammad.org/en/latest/api/intro.html
- Instancia gestionada en el LXC de `pve8.avs.local` (ver [[04-INVENTARIO]]).

## Credenciales

Las credenciales NO están en este archivo (versionado). Están en:

`Documentacion/Privado/credenciales-zammad.md` (excluido de Git por `.gitignore`)

Verificado el 2026-08-30: ambos métodos de autenticación están habilitados en `Admin > Ajustes > Sistema > API`:
- **Token de acceso (recomendado)** — HTTP Token Authentication.
- **Password (Basic Auth)** — usuario/email + contraseña.

## Método preferido: Token de acceso

Usar token en vez de la contraseña siempre que sea posible (evita transmitir la contraseña real en cada llamada y se puede revocar sin cambiar la contraseña de la cuenta).

1. Si no existe token aún, generarlo en la web: `Perfil > Token de acceso > Crear un Token de acceso personal` (elegir permisos mínimos necesarios).
2. Guardar el token generado en `Documentacion/Privado/credenciales-zammad.md`, nunca en notas versionadas.
3. Llamar a la API:

```bash
curl -H "Authorization: Token token=<TOKEN>" https://zammad.avsconsulting.es/api/v1/groups
```

## Alternativa: Basic Auth (usuario/contraseña)

Solo si no hay token disponible y no se puede generar en el momento:

```bash
curl -u 'usuario@dominio:contraseña' https://zammad.avsconsulting.es/api/v1/users/me
```

## Endpoints útiles

| Recurso | Endpoint |
|---|---|
| Usuario actual | `GET /api/v1/users/me` |
| Listar tickets | `GET /api/v1/tickets` |
| Ver ticket | `GET /api/v1/tickets/:id` |
| Crear ticket | `POST /api/v1/tickets` |
| Listar usuarios | `GET /api/v1/users` |
| Listar grupos | `GET /api/v1/groups` |
| Listar organizaciones | `GET /api/v1/organizations` |

Ejemplo — crear ticket:

```bash
curl -X POST https://zammad.avsconsulting.es/api/v1/tickets \
  -H "Authorization: Token token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Asunto del ticket",
    "group": "Users",
    "customer": "cliente@dominio.com",
    "article": {
      "subject": "Asunto del ticket",
      "body": "Contenido del mensaje",
      "type": "note",
      "internal": false
    }
  }'
```

## Seguridad

- No imprimir ni registrar el token o la contraseña en salidas, commits, issues o notas versionadas.
- Preferir tokens con el permiso mínimo necesario (no usar tokens/roles de administrador para tareas de solo lectura).
- Si un token se filtra, revocarlo inmediatamente desde `Perfil > Token de acceso`.
- Registrar cualquier cambio de configuración de la API (activar/desactivar métodos) en [[03-DECISIONES]].
