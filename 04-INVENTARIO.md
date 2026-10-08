# Inventario

## Accesos

- Web (FQDN público): https://zammad.avsconsulting.es
- Web (FQDN alternativo, ver `Documentacion/Conexion/HTTPS - FQDN.bat`): https://zammadavs.salbapas.work:8443
- Web (IP directa, ver `Documentacion/Conexion/HTTPS - IP.bat`): http://192.168.150.186:8080
- SSH: `ssh root@192.168.150.186` (ver `Documentacion/Conexion/SSH - local.bat`); credenciales no registradas en notas versionables (`13-SEGURIDAD-Y-PRIVADO.md`)


## Grupo @autorizaciones

- Alta 2026-10-02, ticket #111373. Grupo id 6; propietario inicial Diego Liosi (5), Salva (8) como seguimiento y receptor del traspaso. Ambos miembros full y suscritos automaticamente.
- Correo de entrada: soporte existente, asunto @autorizaciones; no se creo un buzon nuevo. Filtro 6; triggers 11-14. Evidencia en [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Cluster Proxmox/pve8.avs.local/VM/Zammad/10-VALIDACIONES|10-VALIDACIONES]].

## Plataforma verificada el 2026-10-08

- VM QEMU 110 `Zammad` en pve8, activa; 4 vCPU, memoria configurada 8000 MiB, disco virtual 30 GiB. Fuente: consulta viva Proxmox `/cluster/resources`.
- Servicio desplegado con Docker Compose: imagen Zammad `6.5.0-15`, PostgreSQL `17.4-alpine`, Redis `7.4.2-alpine`, Elasticsearch `8.17.4`, nginx proxy `1.27-alpine`. No se realizó actualización de versiones.
- Acceso administrativo para mantenimiento: `scripts/zammad_ssh.py` carga solo en memoria la clave cifrada cuyo propietario es [[Clientes/AVS/Valencia/Usuarios y equipos/Servidores/Servidor Proxmox/13-SEGURIDAD-Y-PRIVADO|Servidor Proxmox]]. Las identidades locales antiguas no autenticaron; no asumir que `SSH - local.bat` funciona con la clave por defecto.
- Acceso RCLONE: `%LOCALAPPDATA%\AVS\Tools\rclone\rclone.exe` v1.75.1; identidad local `%USERPROFILE%\.ssh\id_ed25519_zammad_sftp`, autorizada con `restrict,command="internal-sftp"` (sin shell), host verificado en `known_hosts_zammad_sftp`. Datos privados fuera del repo.
- `Documentacion/Conexion/RCLONE.cmd -CheckOnly` comprueba SFTP. El montaje opcional Z: necesita WinFsp, ausente al verificar; no hay montaje creado.
