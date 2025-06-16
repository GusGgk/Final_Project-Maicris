from flask import Blueprint, request, jsonify
from services.user_service import listar_usuarios, adicionar_usuario, get_user_by_id, update_user, delete_user

user_bp = Blueprint("user_bp", __name__, url_prefix="/usuarios")

# LISTAR USUÁRIOS
@user_bp.route("/", methods=["GET"])
@user_bp.route("", methods=["GET"])  # opcional, para aceitar sem barra
def get_usuarios():
    usuarios = listar_usuarios()
    return jsonify(usuarios), 200

# ADICIONAR USUÁRIO
@user_bp.route("/", methods=["POST"])
@user_bp.route("", methods=["POST"])  # opcional
def post_usuario():
    dados = request.get_json(force=True)
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    required_fields = ["name", "email", "password", "type"]
    if not all(field in dados for field in required_fields):
        return jsonify({"mensagem": "Campos obrigatórios ausentes (name, email, password, type)"}), 400

    resultado = adicionar_usuario(dados)
    if "Erro" in resultado["mensagem"]:
        return jsonify(resultado), 409
    return jsonify(resultado), 201

# RESTANTE DAS ROTAS
@user_bp.route("/<string:user_id>", methods=["GET"])
def get_usuario_by_id(user_id):
    usuario = get_user_by_id(user_id)
    if usuario:
        return jsonify(usuario.to_dict()), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

@user_bp.route("/<string:user_id>", methods=["PUT"])
def put_usuario(user_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    usuario_atualizado = update_user(user_id, dados)
    if usuario_atualizado:
        return jsonify({"mensagem": "Usuário atualizado com sucesso", "usuario": usuario_atualizado.to_dict()}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

@user_bp.route("/<string:user_id>", methods=["DELETE"])
def delete_usuario(user_id):
    if delete_user(user_id):
        return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404
