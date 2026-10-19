---
name: registrar-compra
description: Preparar y enviar solicitudes de compra de material por Zammad. Usar cuando haya que pedir a Silvia Densow un producto para un usuario o equipo.
---

# Registrar una compra en Zammad

Usa esta skill cuando el usuario pida solicitar material o un dispositivo para una persona o equipo.

## Flujo

1. Localiza el ticket relacionado en Zammad y léelo antes de redactar. Si no existe, prepara la solicitud en el canal indicado por el usuario; no inventes un número de ticket.
2. Identifica el producto, el enlace, el usuario beneficiario y el motivo de la compra. No inventes modelo, precio, plazo ni proveedor.
3. El destinatario de las compras es siempre Silvia Densow: `sdensow@avsconsulting.es`. El ticket original puede pertenecer al usuario beneficiario; eso no cambia el destinatario.
4. Redacta un correo breve en castellano, dirigido a Silvia, indicando el producto, el enlace y por qué se necesita. Mantén el ticket abierto salvo que el usuario pida cerrarlo.
5. Muestra el destinatario, número de ticket y texto exacto y espera aprobación explícita antes de enviar.
6. Tras la aprobación, ejecuta primero una comprobación en seco:

   ```powershell
   python scripts/zammad_api.py email <numero> --to sdensow@avsconsulting.es --file <borrador.txt> --dry-run
   ```

7. Envía el mismo borrador como correo visible, no como nota interna:

   ```powershell
   python scripts/zammad_api.py email <numero> --to sdensow@avsconsulting.es --file <borrador.txt>
   ```

8. Verifica que Zammad registra el artículo como `email`, con `internal: false`, y elimina el borrador temporal. No cierres el ticket sin instrucciones.

## Límites

- No compres directamente ni confirmes un pedido; esta skill solo solicita la compra.
- No guardes credenciales ni datos de pago.
- Si falta el destinatario, el producto, el enlace o el ticket, detente y pide solo el dato necesario.
- Si Silvia responde con disponibilidad, precio o plazo, regístralo en el ticket y consulta al usuario antes de aceptar cambios o confirmar la compra.
