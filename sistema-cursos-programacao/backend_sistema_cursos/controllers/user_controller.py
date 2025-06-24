# ======================================================
# 📁 user_controller.py
# Controlador para gerenciamento de usuários e autenticação
# ======================================================

# -------------------- IMPORTAÇÕES --------------------
from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from services.user_service import (
    list_all_users, 
    add_user, 
    get_user_by_id, 
    update_user, 
    delete_user,
    find_user_by_email
)
from utils.auth import token_required

# -------------------- CRIAÇÃO DO BLUEPRINT --------------------
user_bp = Blueprint("user_bp", __name__, url_prefix="/usuarios")

# ======================================================
# ➕ CADASTRO DE NOVO USUÁRIO (ROTA PÚBLICA)
# ======================================================
@user_bp.route("/", methods=["POST"])
def post_usuario():
    # Rota pública para permitir o cadastro de novos usuários
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    required_fields = ["name", "email", "password", "user_type"]
    if not all(field in dados and dados[field] for field in required_fields):
        return jsonify({"mensagem": "Todos os campos são obrigatórios (name, email, password, user_type)."}), 400
    
    # --- Validações de Conteúdo e Formato ---
    
    # Valida o nome do usuário
    if len(dados["name"].strip()) < 2:
        return jsonify({"mensagem": "O nome deve ter pelo menos 2 caracteres."}), 400

    # Valida o formato do e-mail
    if "@" not in dados["email"] or "." not in dados["email"] or len(dados["email"]) < 5:
        return jsonify({"mensagem": "Formato de e-mail inválido."}), 400
        
    # Valida o comprimento da senha
    if len(dados["password"]) < 6:
        return jsonify({"mensagem": "A senha deve ter no mínimo 6 caracteres."}), 400

    # Valida o tipo de usuário para garantir que seja um dos valores permitidos
    if dados["user_type"] not in ["aluno", "instrutor", "admin"]:
        return jsonify({"mensagem": "Tipo de usuário inválido. Use 'aluno', 'instrutor' ou 'admin'."}), 400

    try:
        new_user = add_user(dados)
        # Usamos to_dict() que é seguro e não expõe a senha na resposta
        return jsonify(new_user.to_dict()), 201
    except ValueError as e:
        # Captura o erro de e-mail duplicado do service
        return jsonify({"mensagem": str(e)}), 409


# ======================================================
# 🔑 AUTENTICAÇÃO DE USUÁRIO (LOGIN - ROTA PÚBLICA)
# ======================================================
@user_bp.route("/login", methods=["POST"])
def login():
    # Rota pública para permitir a autenticação e obtenção de token
    dados = request.get_json()
    if not dados or not dados.get("email") or not dados.get("password"):
        return jsonify({"mensagem": "Email e senha são obrigatórios"}), 400

    email = dados["email"]
    password = dados["password"]
    user = find_user_by_email(email)

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"mensagem": "Credenciais inválidas"}), 401

    payload = {
        'sub': user.id,
        'tipo': user.user_type,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({
        "token": token,
        "user": user.to_dict() # Resposta segura sem a senha
    })


# ======================================================
# 🔍 CONSULTA DE USUÁRIOS (ROTAS PROTEGIDAS)
# ======================================================
@user_bp.route("/", methods=["GET"])
@token_required
def get_usuarios(current_user):
    # Apenas administradores podem listar todos os usuários
    if current_user['user_type'] != 'admin':
        return jsonify({"mensagem": "Acesso negado. Apenas administradores."}), 403
    
    usuarios = list_all_users()
    # A senha não deve ser exposta, o to_dict() do modelo já cuida disso
    return jsonify([user.to_dict() for user in usuarios]), 200


@user_bp.route("/<string:user_id>", methods=["GET"])
@token_required
def get_usuario_by_id(current_user, user_id):
    # Um usuário pode ver seu próprio perfil, ou um admin pode ver qualquer perfil
    if current_user['user_type'] != 'admin' and current_user['id'] != user_id:
        return jsonify({"mensagem": "Acesso negado."}), 403

    usuario = get_user_by_id(user_id)
    if usuario:
        return jsonify(usuario.to_dict()), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404


# ======================================================
# ✏️ EDIÇÃO DE USUÁRIO (ROTA PROTEGIDA)
# ======================================================
@user_bp.route("/<string:user_id>", methods=["PUT"])
@token_required
def put_usuario(current_user, user_id):
    # Um usuário pode atualizar seu próprio perfil, ou um admin pode atualizar qualquer perfil
    if current_user['user_type'] != 'admin' and current_user['id'] != user_id:
        return jsonify({"mensagem": "Acesso negado."}), 403

    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400
    
    # Impede que um usuário comum (não-admin) altere seu próprio tipo de usuário
    if 'user_type' in dados and current_user['user_type'] != 'admin':
        return jsonify({"mensagem": "Você não tem permissão para alterar o tipo de usuário."}), 403

    usuario_atualizado = update_user(user_id, dados)
    if usuario_atualizado:
        # A resposta da atualização também usa o to_dict() seguro
        return jsonify({"mensagem": "Usuário atualizado com sucesso", "usuario": usuario_atualizado.to_dict()}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404


# ======================================================
# 🗑️ REMOÇÃO DE USUÁRIO (ROTA PROTEGIDA)
# ======================================================
@user_bp.route("/<string:user_id>", methods=["DELETE"])
@token_required
def delete_usuario(current_user, user_id):
    # Apenas administradores podem deletar usuários
    if current_user['user_type'] != 'admin':
        return jsonify({"mensagem": "Acesso negado. Apenas administradores."}), 403

    if delete_user(user_id):
        return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404