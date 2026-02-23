import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- NUEVO: Para permitir peticiones desde zord.cl
import launcher 

app = Flask(__name__)
CORS(app)  # <--- ACTIVACIÓN DE CORS

# =============================================================
# CONFIGURACIÓN DE CREDENCIALES
# =============================================================
FLOW_SECRET = "a027e1791c1f3919654120ebb688410360b3d72c" 
USUARIO_ZORD = "zord.spa@zord.cl"
PASS_APP_GOOGLE = "jqgj fmzv qtya kdiw" 

# =============================================================
# FUNCIÓN DE ENVÍO DE EMAIL
# =============================================================
def enviar_llave_cliente(email_destino, api_key_generada, plan_nombre):
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
    2. Utilice esta llave en sus integraciones técnicas.
    
    Soberanía Tecnológica y Estabilidad Molecular.
    ZORD SpA - Villa Alemana, Chile.
    -------------------------------------------
    """
    msg.set_content(contenido)
    msg['Subject'] = f'🔑 Su API-KEY ZORD está lista ({plan_nombre})'
    msg['From'] = USUARIO_ZORD
    msg['To'] = email_destino

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(USUARIO_ZORD, PASS_APP_GOOGLE)
            smtp.send_message(msg)
            print(f"[MAIL] Protocolo enviado a {email_destino}")
            return True
    except Exception as e:
        print(f"[MAIL ERROR] {e}")
        return False

# =============================================================
# RUTA WEBHOOK (PUENTE DESDE /EXITO O FLOW)
# =============================================================
@app.route('/webhook-flow', methods=['POST'])
def webhook_flow():
    # Detectar si viene como JSON o como Formulario
    if request.is_json:
        data = request.get_json()
        token_pago = data.get('token')
    else:
        token_pago = request.form.get('token')

    if not token_pago:
        return jsonify({"error": "Token no encontrado"}), 400

    # LÓGICA DE ACTIVACIÓN
    # Nota: Aquí simulamos éxito. En producción validarías con el token contra Flow.
    pago_exitoso = True 
    email_cliente = "soporte@zord.cl" # En un flujo real, obtienes esto de Flow vía API
    plan_comprado = "PRO" 
    creditos = 5000 if plan_comprado == "PRO" else 1000

    if pago_exitoso:
        nueva_api_key = launcher.generar_nueva_api_key(plan_comprado)
        
        print(f"[*] Registrando {creditos} créditos para {email_cliente}...")
        exito_registro = launcher.registrar_en_render(
            api_key=nueva_api_key,
            cantidad=creditos,
            nombre_cliente=email_cliente
        )

        if exito_registro:
            enviar_llave_cliente(email_cliente, nueva_api_key, plan_comprado)
            return jsonify({
                "status": "success", 
                "key": nueva_api_key
            }), 200
        else:
            return jsonify({"error": "Error en motor Render"}), 500

    return jsonify({"error": "Pago no aprobado"}), 402

if __name__ == '__main__':
    # Puerto estándar para Render
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
