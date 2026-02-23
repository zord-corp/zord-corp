import requests
import json

# ==============================================================================
# CONFIGURACIÓN DE CONEXIÓN (VINCULACIÓN CON RENDER)
# ==============================================================================
# La URL de tu motor en producción
RENDER_API_URL = "https://zsusy-zsecure-engine.onrender.com/admin/add_credits"

# El Token que definimos en las variables de entorno de Render
# Asegúrate de que coincida con el que pusiste en el panel de Render
ZORD_ADMIN_TOKEN = "ZORD_SECRET_2026" 

def cargar_creditos_cliente(api_key, cantidad, nombre_cliente="Cliente Nuevo"):
    """
    Función maestra para inyectar créditos desde zord.cl hacia el motor ZSusy.
    Se activa automáticamente tras un pago exitoso en el BCI vía Flow.cl.
    """
    
    print(f"[*] Iniciando carga de {cantidad} créditos para: {nombre_cliente}...")

    headers = {
        "ZORD-ADMIN-TOKEN": ZORD_ADMIN_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "api_key": api_key,
        "cantidad": cantidad,
        "nombre": nombre_cliente
    }

    try:
        # Enviamos la orden al servidor de Render
        response = requests.post(RENDER_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"[SUCCESS] {response.json()['message']}")
            return True
        elif response.status_code == 403:
            print("[ERROR] Token de Administración inválido. Revisa las variables de entorno en Render.")
            return False
        else:
            print(f"[ERROR] El servidor respondió con código: {response.status_code}")
            print(f"Detalle: {response.text}")
            return False

    except Exception as e:
        print(f"[CRITICAL ERROR] No se pudo contactar con el motor ZSusy: {e}")
        return False

# ==============================================================================
# ZONA DE PRUEBAS (Simulación de Venta)
# ==============================================================================
if __name__ == "__main__":
    # Supongamos que acabamos de recibir un pago por un pack de 1,000 llaves
    test_key = "ZORD-DEMO-1234"
    pack_comprado = 1000
    nombre = "Empresa_Partner_Z"

    exito = cargar_creditos_cliente(test_key, pack_comprado, nombre)
    
    if exito:
        print("[*] Sistema listo para la siguiente transacción.")
    else:
        print("[!] Revisa la conexión con la base de datos en Oregon.")
