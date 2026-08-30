# Memoria IA

## 2026-08-30 12:30 CEST
**Tema:** Accesos, verificación de API Zammad y limpieza de tickets duplicados
**Tipo:** Sesion
**Estado:** Aplicado

**Ultimo contexto:**
- Registrados accesos web (FQDN público, FQDN alternativo, IP directa) y SSH del LXC en `04-INVENTARIO.md`.
- Guardadas credenciales del usuario `sat@nexo.net` en `Documentacion/Privado/credenciales-zammad.md` (excluido de Git).
- Verificado por Selenium el login web y, en `Admin > Sistema > API`, que están habilitados Token Access y HTTP Basic Auth (no hay apps OAuth configuradas).
- Probada la API REST con Basic Auth (`GET /api/v1/users/me` → 200 OK).
- Creada skill `.skills/zammad-api/SKILL.md` con la forma de autenticarse y endpoints útiles.
- A petición del usuario, localizados por contenido (Threat ID/Device ID/fecha) y eliminados permanentemente vía API 3 tickets duplicados de una misma alerta de ransomware (falso positivo probable) en TX2550M4: #111253, #111251, #111254.
- Detectado que existen más tickets históricos con el mismo patrón (TX2550M4, distintos usuarios) sin limpiar — ver `03-DECISIONES.md`.

**Archivos tocados:**
- `04-INVENTARIO.md`, `01-ESTADO.md`, `03-DECISIONES.md`, `10-VALIDACIONES.md`, `.skills/zammad-api/SKILL.md`, `Documentacion/Privado/credenciales-zammad.md` (no versionado).

**Siguiente acción sugerida:**
- Generar token de acceso personal en Zammad y sustituir el uso de la contraseña en la API.
- Revisar la regla de origen (NinjaOne/SentinelOne) del falso positivo recurrente en TX2550M4.

## 2026-08-30 10:46 CEST
**Tema:** Creación de arquitectura documental
**Tipo:** Estructural
**Estado:** Aplicado

**Ultimo contexto:**
- Creado únicamente el esqueleto documental; no se incorporó información operativa ni técnica.
- La carpeta `Documentacion/` se integra expresamente en la arquitectura mediante su guía local.
- Inicializado un repositorio Git independiente, sin remoto ni commit inicial.
- Configurado el remoto `origin`; se verificó el acceso y no hay ramas remotas todavía.

**Archivos tocados:**
- Archivos de arquitectura en la raíz del proyecto.

**Siguiente acción sugerida:**
- Incorporar contenido verificado solo cuando sea necesario.

## Formato de entrada

```md
## AAAA-MM-DD HH:MM TZ
**Tema:**
**Tipo:** Sesion / Estructural / Decision / Documentacion
**Estado:**

**Ultimo contexto:**
-

**Archivos tocados:**
-

**Siguiente acción sugerida:**
-
```
