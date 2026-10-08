# Seguridad y privado

- Los secretos no se registran en notas versionables.
- `Documentacion/Privado/` y `Backups/` se reservan para material local o sensible.
- Documentar solo referencias saneadas y verificables.
- #111121: originales recuperables en `Backups/20261008-175618-111121-original.json.enc`, cifrados con la clave de proyecto del almacén privado; excluidos de Git. Incluyen el cuerpo exacto de base de datos, MIME y adjuntos. No copiar la licencia a notas ni al historial.
- `scripts/sanear_licencia_syncback.py` sustituye únicamente la licencia reconocida, con transacción y comprobaciones de identidad, hashes y referencias no compartidas. Mantiene los IDs y la factura; actualiza el índice sin callbacks que registren el secreto anterior o generen avisos. No purga copias históricas externas ni backups de plataforma.
- La identidad SFTP dedicada permanece en el perfil local con ACL de lectura del usuario; no se reutiliza la clave GitHub ni se exporta la clave administrativa de Proxmox.
