from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import os

# Inicializa Firebase
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "base-de-datos-asm",
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": "firebase-adminsdk@base-de-datos-asm.iam.gserviceaccount.com",
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("CLIENT_CERT_URL")
})

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://base-de-datos-asm-default-rtdb.firebaseio.com'
})

app = Flask(__name__)

@app.route('/', methods=['GET'])
def buscar():
    consulta = request.args.get('q', '').lower()
    if not consulta:
        return jsonify({"mensaje": "No se proporcionó término de búsqueda"}), 400

    ref = db.reference('inventario')
    data = ref.get()

    resultados = []
    for id_producto, valores in data.items():
        texto_busqueda = f"{valores.get('Marca', '')} {valores.get('Modelo', '')} {valores.get('Caracteristicas clave', '')}".lower()
        if all(palabra in texto_busqueda for palabra in consulta.split()):
            resultados.append({
                "ID": id_producto,
                **valores
            })

    if resultados:
        return jsonify(resultados)
    else:
        return jsonify({"mensaje": "No se encontraron coincidencias"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
