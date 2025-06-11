from flask import Flask, request, jsonify
from flask_cors import CORS  # para permitir que o frontend acesse o backend
from services.user_service import listar_usuarios, adicionar_usuario

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)  # habilita o CORS

# Rota GET - listar usuários
@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = listar_usuarios()
    return jsonify(usuarios), 200

# Rota POST - cadastrar usuário
@app.route("/usuarios", methods=["POST"])
def post_usuario():
    dados = request.get_json(force=True)  # força leitura do JSON mesmo se o header não vier perfeito
    resultado = adicionar_usuario(dados)
    return jsonify(resultado), 201

# Rota de teste (opcional)
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"mensagem": "Servidor funcionando"}), 200

# Inicializa o servidor
if __name__ == "__main__":
    app.run(debug=True)
