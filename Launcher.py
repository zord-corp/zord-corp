import requests

def notificar_pago_exitoso(api_key_cliente, cantidad_comprada, nombre_cliente):
    # Esta es la URL de tu motor en Render
    url_render = "https://zsusy-zsecure-engine.onrender.com/admin/add_credits"
    
    # Este es el Token que definiste en tu archivo zord_api.py
    # ¡CÁMBIALO ALLÁ Y PON EL MISMO AQUÍ!
    admin_token = "ZORD_SECRET_2026" 

    headers = {
        "ZORD-ADMIN-TOKEN": admin_token,
        "Content-Type": "application/json"
    }

    payload = {
        "api_key": api_key_cliente,
        "cantidad": cantidad_comprada,
        "nombre": nombre_cliente
    }

    try:
        response = requests.post(url_render, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Éxito: Créditos cargados a {nombre_cliente}")
        else:
            print(f"Error: El motor respondió {response.status_code}")
    except Exception as e:
        print(f"Error de conexión: {e}")
