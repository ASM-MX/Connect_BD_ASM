
import os
import json
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, request, jsonify

# Leer credencial desde variable de entorno
json_str = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
cred_dict = json.loads(json_str.replace('\\n', '\n'))

# Inicializar Firebase
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://base-de-datos-asm-default-rtdb.firebaseio.com'
})

app = Flask(__name__)

@app.route("/", methods=["GET"])
def buscar():
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"mensaje": "No se proporcionó término de búsqueda"}), 400

    ref = db.reference("inventario")
    datos = ref.get()
    resultados = []

    for clave, valores in datos.items():
        campo_texto = f"{valores.get('Marca', '')} {valores.get('Modelo', '')} {valores.get('Caracteristicas clave', '')}".lower()
        if all(palabra in campo_texto for palabra in query.split()):
            resultados.append({
                "ID": clave,
                **valores
            })

    if resultados:
        return jsonify(resultados)
    else:
        return jsonify({"mensaje": "No se encontraron coincidencias"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
