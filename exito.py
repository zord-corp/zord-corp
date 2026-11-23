<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZORD | Credencial Activada</title>
    <style>
        body {
            background-color: #05070a;
            color: #c9d1d9;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .card {
            background: #0d1117;
            padding: 40px;
            border-radius: 8px;
            max-width: 580px;
            width: 100%;
            text-align: center;
            border: 1px solid #00ffcc;
            box-shadow: 0 0 25px rgba(0, 255, 204, 0.15);
        }
        h1 { color: #00e676; font-size: 1.5rem; margin-top: 0; }
        .api-box {
            background: #04080f;
            color: #00ffcc;
            padding: 25px;
            border-radius: 6px;
            margin: 25px 0;
            border: 1px dashed rgba(0, 255, 204, 0.4);
        }
        .api-box small { color: #8b949e; display: block; margin-bottom: 10px; font-size: 0.75rem; }
        .key-text { font-size: 1.3rem; font-weight: bold; word-break: break-all; }
        .btn-return {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 28px;
            background-color: #00ffcc;
            color: #000;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>

<div class="card">
    <h1>[+] TRANSACCIÓN CONFIRMADA</h1>
    <p style="font-size: 0.9rem; color: #8b949e;">Su pago ha sido procesado por ZORD SpA.</p>

    <div class="api-box">
        <small>> SU CREDENCIAL API_KEY:</small>
        <span class="key-text" id="generatedKey">VALIDANDO PAGO...</span>
    </div>

    <p style="font-size: 0.8rem; color: #8b949e; line-height: 1.5;">
        Se ha enviado un respaldo a su correo electrónico. Conserve esta llave para operar el Sellador PQC y el Oráculo.
    </p>

    <a href="index.html" class="btn-return">Volver al Terminal</a>
</div>

<script>
    const urlParams = new URLSearchParams(window.location.search);
    const keyDirecta = urlParams.get('key');
    const tokenFlow = urlParams.get('token');
    const display = document.getElementById('generatedKey');

    if (keyDirecta) {
        display.innerText = keyDirecta;
    } else if (tokenFlow) {
        display.innerText = "ACTIVANDO CREDENCIALES...";
        fetch('https://api.zord.cl/webhook-flow', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: tokenFlow })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success" && data.key) {
                display.innerText = data.key;
            } else {
                display.innerText = "REVISE SU CORREO ELECTRÓNICO";
            }
        })
        .catch(() => {
            display.innerText = "REVISE SU CORREO ELECTRÓNICO";
        });
    } else {
        display.innerText = "REVISE SU CORREO ELECTRÓNICO";
    }
</script>
</body>
</html>
