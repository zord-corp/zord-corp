from flask import Flask, request
import launcher # Importa el archivo del Paso 2

app = Flask(__name__)

@app.route('/webhook-flow', methods=['POST'])
def webhook_flow():
    # 1. Flow envía un 'token' por cada transacción
    token_pago = request.form.get('token')
    
    # [IMPORTANTE] Aquí deberías usar la librería oficial de Flow 
    # para confirmar que el pago realmente entró a tu BCI.
    
    # 2. Simulación de datos tras pago aprobado (esto vendría de Flow)
    pago_confirmado = True 
    plan = "PRO" # Supongamos que pagó el plan corporativo
    email = "comprador@empresa.cl"
    creditos = 5000 if plan == "PRO" else 1000

    if pago_confirmado:
        # 3. Generar la llave con prefijo (ZORD-PRO-...)
        nueva_key = launcher.generar_nueva_api_key(plan)
        
        # 4. Inyectar en la base de datos de Render
        exito = launcher.registrar_en_render(nueva_key, creditos, email)
        
        if exito:
            # 5. Aquí podrías disparar un correo automático al cliente
            print(f"ÉXITO: Cliente {email} activado con llave {nueva_key}")
            return "Pago Procesado", 200
            
    return "Error", 400
