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

import subprocess
import os

# =============================================================
# NUEVO MÓDULO PQC: SELLADO SOBERANO (ML-DSA-44)
# =============================================================
# Estas funciones usan el motor OpenSSL configurado con Lazarus
# No alteran la generación de API Keys estándar.

def sellar_documento_pqc(ruta_documento, ruta_llave_privada="llave_privada_zord.pem", ruta_salida_firma="firma_zord.sig"):
    """
    Genera el Sello Digital Lazarus (Firma Post-Cuántica) para un documento.
    """
    # Si estás en WSL y configuraste OPENSSL_MODULES, esto correrá nativo.
    comando = [
        "openssl", "dgst",
        "-provider", "oqsprovider",
        "-provider", "default",
        "-sign", ruta_llave_privada,
        "-out", ruta_salida_firma,
        ruta_documento
    ]
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"[ZORD PQC] ✅ Sello generado exitosamente: {ruta_salida_firma}")
            return True
        else:
            print(f"[ZORD PQC] ❌ Error al sellar: {resultado.stderr}")
            return False
    except Exception as e:
        print(f"[ZORD PQC] ❌ Error de sistema: {e}")
        return False

def verificar_documento_pqc(ruta_documento, ruta_firma, ruta_llave_publica="llave_publica_zord.pem"):
    """
    Valida la integridad de un documento contra un Sello ZORD.
    """
    comando = [
        "openssl", "dgst",
        "-provider", "oqsprovider",
        "-provider", "default",
        "-verify", ruta_llave_publica,
        "-signature", ruta_firma,
        ruta_documento
    ]
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if "Verified OK" in resultado.stdout:
            print(f"[ZORD PQC] ✅ VERIFIED OK: El documento '{ruta_documento}' mantiene integridad absoluta.")
            return True
        else:
            print(f"[ZORD PQC] ❌ FALLO DE VERIFICACIÓN: Documento alterado o sello inválido.")
            return False
    except Exception as e:
        print(f"[ZORD PQC] ❌ Error de sistema: {e}")
        return False
