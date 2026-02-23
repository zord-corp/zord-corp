from flask import Flask, request, jsonify
import launcher  # Importamos tu lógica del Paso 2

app = Flask(__name__)

# Llave de seguridad para que solo Flow pueda enviarte datos
# Puedes encontrarla en tu panel de Flow como "Secret Key"
FLOW_SECRET = "TU_SECRET_KEY_DE_FLOW" 

@app.route('/webhook-flow', methods=['POST'])
def webhook_flow():
    """
    Este es el punto de entrada que Flow llama automáticamente
    cuando el BCI confirma el pago.
    """
    # 1. Recibir el token del pago desde Flow
    token_pago = request.form.get('token')
    
    if not token_pago:
        return "Token no encontrado", 400

    # 2. Lógica de Negocio: Determinar el Plan
    # En una integración real, aquí consultarías a la API de Flow 
    # usando el token para saber qué compró exactamente el cliente.
    
    # --- SIMULACIÓN DE RESULTADO DE PAGO ---
    pago_exitoso = True 
    email_cliente = request.form.get('email', 'cliente_nuevo@zord.cl')
    
    # Determinamos el plan (esto suele venir en un campo 'status' o 'amount')
    # Por ahora, simularemos que si el pago es exitoso, le damos el plan PRO
    plan_comprado = "PRO" 
    creditos = 5000 if plan_comprado == "PRO" else 1000

    if pago_exitoso:
        # 3. Generar la API-KEY única (ZORD-PRO-XXXX...)
        nueva_api_key = launcher.generar_nueva_api_key(plan_comprado)
        
        # 4. Registrar en el motor ZSusy (Render / PostgreSQL Oregon)
        print(f"[*] Procesando compra de {email_cliente}. Generando llave...")
        
        exito_registro = launcher.registrar_en_render(
            api_key=nueva_api_key,
            cantidad=creditos,
            nombre_cliente=email_cliente
        )

        if exito_registro:
            # 5. Aquí es donde el sistema "se paga solo"
            print(f"[EXITO] Cliente {email_cliente} activado. Key: {nueva_api_key}")
            
            # TODO: Aquí podrías añadir una función para enviar la llave por email
            return jsonify({"status": "success", "key_generada": nueva_api_key}), 200
        else:
            return "Error al registrar en motor Render", 500

    return "Pago no aprobado", 402

if __name__ == '__main__':
    # Tu servidor web debe correr este proceso en el puerto 5000 o el que use tu hosting
    app.run(port=5000)
