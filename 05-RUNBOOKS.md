# Runbooks




## Gestion de @autorizaciones

1. Enviar al correo habitual de soporte con @autorizaciones al principio del asunto.
2. Diego recibe la propiedad inicial; ambos siguen el ticket por suscripcion.
3. Para que intervenga Salva, cambiar propietario a Salvador Bayona Pascual; las respuestas no deben restablecer a Diego.
4. Para revisar avisos: comprobar miembros del grupo 6, mentions de ambos usuarios y preferencias email/online de propios/suscritos. Verificar entrega en buzones, no confundir suscripcion con entrega SMTP.
5. Rollback de esta configuracion: desactivar triggers 11-14 y filtro 6; retirar solo el permiso del grupo 6 de los usuarios 5/8 y desactivar el grupo cuando no tenga tickets activos. No borrar tickets ni otros permisos. Las suscripciones ya creadas son persistentes.

Referencia de mecanismo: https://admin-docs.zammad.org/en/latest/manage/trigger.html (suscripcion mediante triggers).
