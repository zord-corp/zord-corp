import requests

# 1. Datos de conexión
URL = "https://zsusy-zsecure-engine.onrender.com/admin/add_credits"
TOKEN = "Zord-Bci-Secure-99x#" # La clave que funcionó en PS

def ejecutar_carga():
    # 2. Configuración de Headers (Exactamente como en PS)
    headers = {
        "ZORD-ADMIN-TOKEN": TOKEN,
        "Content-Type": "application/json"
    }

    # 3. Cuerpo de la petición
    payload = {
        "api_key": "ZORD-DEMO-1234",
        "cantidad": 1000,
        "nombre": "Empresa_Partner_Z"
    }

    print(f"[*] Intentando conectar con ZSusy Engine...")

    try:
        # Usamos json=payload para que requests maneje el Content-Type automáticamente
        response = requests.post(URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("[SUCCESS] Respuesta del servidor:", response.json())
        else:
            print(f"[ERROR] Código: {response.status_code}")
            print(f"Detalle del servidor: {response.text}")
            
    except Exception as e:
        print(f"[CRITICAL] Error de conexión: {e}")

if __name__ == "__main__":
    ejecutar_carga()
