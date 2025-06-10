from flask import Flask, request, jsonify
from flask_cors import CORS
from services.user_service import listar_usuarios, adicionar_usuario

app = Flask(__name__)
CORS(app)


@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    return jsonify(listar_usuarios()), 200

@app.route("/usuarios", methods=["POST"])
def post_usuario():
    dados = request.get_json()
    resultado = adicionar_usuario(dados)
    return jsonify(resultado), 201

if __name__ == "__main__":
    app.run(debug=True)
