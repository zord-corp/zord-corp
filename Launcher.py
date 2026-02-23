import requests
import secrets
import string

# =============================================================
# CONFIGURACIÓN SEGURA (Vínculo con Render)
# =============================================================
RENDER_URL = "https://zsusy-zsecure-engine.onrender.com/admin/add_credits"
ZORD_ADMIN_TOKEN = "Zord-Bci-Secure-99x#"  # Tu clave maestra validada

def generar_nueva_api_key(plan="STD"):
    """
    Genera una API KEY única con prefijo para el cliente.
    Ejemplo: ZORD-STD-A1B2C3D4E5F6
    """
    # Usamos secrets para una generación criptográficamente segura
    random_str = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    return f"ZORD-{plan}-{random_str}"

def registrar_en_render(api_key, cantidad, nombre_cliente):
    """
    Inyecta la nueva llave y sus créditos en la base de datos de Oregon.
    """
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
        response = requests.post(RENDER_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"[CEREBRO] Éxito: {nombre_cliente} activado con {cantidad} créditos.")
            return True
        else:
            print(f"[CEREBRO] Error Render: {response.text}")
            return False
    except Exception as e:
        print(f"[CEREBRO] Error Crítico de conexión: {e}")
        return False
