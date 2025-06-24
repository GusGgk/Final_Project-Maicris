# ======================================================
# 📁 enrollment_controller.py
# Controlador para gerenciamento de matrículas
# ======================================================

# -------------------- IMPORTAÇÕES --------------------
from flask import Blueprint, request, jsonify
from services.enrollment_service import (
    list_all_enrollments, 
    add_enrollment, 
    get_enrollments_by_user_id, 
    get_enrollments_by_course_id, 
    delete_enrollment,
    get_enrollment_by_id 
)
from utils.auth import token_required

# -------------------- CRIAÇÃO DO BLUEPRINT --------------------
enrollment_bp = Blueprint("enrollment_bp", __name__, url_prefix="/enrollments")

# ======================================================
# 🧾 LISTAGEM E CRIAÇÃO DE MATRÍCULAS
# ======================================================
@enrollment_bp.route("/", methods=["GET"])
@token_required
def get_enrollments(current_user):
    # Garante que apenas administradores possam listar todas as matrículas
    if current_user['user_type'] != 'admin':
        return jsonify({"mensagem": "Acesso negado. Apenas administradores."}), 403
    
    enrollments = list_all_enrollments()
    return jsonify([e.to_dict() for e in enrollments]), 200

@enrollment_bp.route("/", methods=["POST"])
@token_required
def post_enrollment(current_user):
    dados = request.get_json()
    # O user_id é extraído do token do usuário logado para segurança
    if not dados or "course_id" not in dados:
        return jsonify({"mensagem": "Dados inválidos. Requer 'course_id'."}), 400

    user_id = current_user['id']
    course_id = dados["course_id"]
    
    resultado = add_enrollment(user_id, course_id)
    
    if "Erro" in resultado.get("mensagem", ""):
        return jsonify(resultado), 400
    return jsonify(resultado), 201

# ======================================================
# 🔍 CONSULTA DE MATRÍCULAS ESPECÍFICAS
# ======================================================
@enrollment_bp.route("/user/<string:user_id>", methods=["GET"])
@token_required
def get_enrollments_by_user(current_user, user_id):
    # Um usuário só pode ver suas próprias matrículas, a menos que seja um admin
    if current_user['user_type'] != 'admin' and current_user['id'] != user_id:
        return jsonify({"mensagem": "Acesso negado."}), 403

    enrollments = get_enrollments_by_user_id(user_id)
    return jsonify([e.to_dict() for e in enrollments]), 200

@enrollment_bp.route("/course/<string:course_id>", methods=["GET"])
@token_required
def get_enrollments_by_course(current_user, course_id):
    # Regra de negócio: Apenas administradores podem ver a lista de alunos por curso
    if current_user['user_type'] != 'admin':
        return jsonify({"mensagem": "Acesso negado."}), 403

    enrollments = get_enrollments_by_course_id(course_id)
    return jsonify([e.to_dict() for e in enrollments]), 200

# ======================================================
# 🗑️ CANCELAMENTO DE MATRÍCULA
# ======================================================
@enrollment_bp.route("/<string:enrollment_id>", methods=["DELETE"])
@token_required
def delete_enrollment_route(current_user, enrollment_id):
    enrollment = get_enrollment_by_id(enrollment_id)
    if not enrollment:
        return jsonify({"mensagem": "Matrícula não encontrada"}), 404

    # Um usuário só pode deletar sua própria matrícula, a menos que seja um admin
    if current_user['user_type'] != 'admin' and current_user['id'] != enrollment.user_id:
        return jsonify({"mensagem": "Acesso negado. Você não pode cancelar esta matrícula."}), 403

    if delete_enrollment(enrollment_id):
        return jsonify({"mensagem": "Matrícula deletada com sucesso"}), 200
    return jsonify({"mensagem": "Matrícula não encontrada"}), 404