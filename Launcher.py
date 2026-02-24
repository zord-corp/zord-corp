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
