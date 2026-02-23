import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify
import launcher  # Importa generar_nueva_api_key y registrar_en_render

app = Flask(__name__)

# =============================================================
# CONFIGURACIÓN DE CREDENCIALES
# =============================================================
# Flow (Obtenlas en Datos de Integración)
FLOW_SECRET = "TU_SECRET_KEY_DE_FLOW" 

# Gmail / Google Workspace (zord.spa@zord.cl)
USUARIO_ZORD = "zord.spa@zord.cl"
PASS_APP_GOOGLE = "xxxx xxxx xxxx xxxx" # Las 16 letras que generaste

# =============================================================
# FUNCIÓN DE ENVÍO DE EMAIL
# =============================================================
def enviar_llave_cliente(email_destino, api_key_generada, plan_nombre):
    """
    Envía la credencial técnica automáticamente tras el pago.
    """
    msg = EmailMessage()
    
    contenido = f"""
    PROTOCOLO DE ENTREGA - ZORD SpA
    -------------------------------------------
    Estimado Cliente,
    
    Confirmamos la recepción de su pago para el plan {plan_nombre}. 
    Su acceso al motor de entropía ZSusy ha sido habilitado exitosamente.
    
    DETALLES DE LA CREDENCIAL:
    > X-API-KEY: {api_key_generada}
    > Estatus: ACTIVA / SALDO CARGADO
    
    INSTRUCCIONES:
    1. Valide su saldo en tiempo real en: https://zord.cl
    2. Documentación de API disponible en el portal.
    
    Soberanía Tecnológica y Estabilidad Molecular.
    ZORD SpA - Villa Alemana, Chile.
    -------------------------------------------
    Este es un mensaje automático generado por Z-Core Engine.
    """
    msg.set_content(contenido)

    msg['Subject'] = f'🔑 Su API-KEY ZORD está lista ({plan_nombre})'
    msg['From'] = USUARIO_ZORD
    msg['To'] = email_destino

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(USUARIO_ZORD, PASS_APP_GOOGLE)
            smtp.send_message(msg)
            print(f"[MAIL] Protocolo enviado exitosamente a {email_destino}")
            return True
    except Exception as e:
        print(f"[MAIL ERROR] No se pudo enviar el correo: {e}")
        return False

# =============================================================
# RUTA WEBHOOK (ENTRADA DE FLOW)
# =============================================================
@app.route('/webhook-flow', methods=['POST'])
def webhook_flow():
    # 1. Recibir token de Flow
    token_pago = request.form.get('token')
    if not token_pago:
        return "Token no encontrado", 400

    # --- SIMULACIÓN DE VALIDACIÓN DE PAGO ---
    # En producción, aquí usarías el SDK de Flow para confirmar monto y estado
    pago_exitoso = True 
    email_cliente = request.form.get('email', 'soporte@zord.cl') # Fallback por si no viene email
    plan_comprado = "PRO" # Deberías obtenerlo según el monto pagado
    creditos = 5000 if plan_comprado == "PRO" else 1000

    if pago_exitoso:
        # 2. Generar la Key única (ZORD-PRO-...)
        nueva_api_key = launcher.generar_nueva_api_key(plan_comprado)
        
        # 3. Registrar en Render (PostgreSQL Oregon)
        print(f"[*] Inyectando {creditos} créditos para {email_cliente}...")
        exito_registro = launcher.registrar_en_render(
            api_key=nueva_api_key,
            cantidad=creditos,
            nombre_cliente=email_cliente
        )

        if exito_registro:
            # 4. Enviar el correo automático
            enviar_llave_cliente(email_cliente, nueva_api_key, plan_comprado)
            
            # 5. Respuesta final exitosa
            print(f"[EXITO] Proceso completado para {email_cliente}")
            return jsonify({
                "status": "success", 
                "message": "Credenciales enviadas",
                "key": nueva_api_key # Solo para registro interno
            }), 200
        else:
            return "Error en registro de motor", 500

    return "Pago fallido", 402

if __name__ == '__main__':
    app.run(port=5000)
