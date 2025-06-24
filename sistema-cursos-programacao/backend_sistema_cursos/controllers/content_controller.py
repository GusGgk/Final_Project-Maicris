# ======================================================
# 📁 content_controller.py
# Controlador para gerenciamento de módulos e aulas
# ======================================================


# -------------------- IMPORTAÇÕES --------------------

from flask import Blueprint, request, jsonify
from services import content_service
from services.enrollment_service import is_user_enrolled
from utils.auth import token_required

# O app principal cuidará do contexto de importação.

# -------------------- CRIAÇÃO DO BLUEPRINT --------------------
# Cria o Blueprint para este controlador
content_bp = Blueprint('content_controller', __name__)

# -------------------- ROTAS DE CURSO --------------------

# ======================================================
# 🔍 CONSULTA DE CONTEÚDO
# ======================================================
@content_bp.route('/courses/<int:course_id>/contents', methods=['GET'])
@token_required
def get_course_contents(current_user, course_id):
    # Aluno só pode acessar se estiver matriculado
    if current_user['user_type'] == 'aluno':
        if not is_user_enrolled(current_user['id'], course_id):
            return jsonify({"message": "Você não está matriculado neste curso."}), 403
    
    content = content_service.get_content_by_course_id(course_id)
    
    if content:
        return jsonify(content), 200
    return jsonify({"message": "Conteúdo não encontrado para este curso."}), 404

# ======================================================
# ➕ CRIAÇÃO DE MÓDULO E AULA
# ======================================================

@content_bp.route('/courses/<int:course_id>/modules', methods=['POST'])
def add_module(course_id):
    data = request.get_json()
    if not data or 'titulo' not in data:
        return jsonify({"message": "O título do módulo é obrigatório."}), 400
    
    try:
        new_module = content_service.add_module_to_course(course_id, data['titulo'])
        return jsonify(new_module), 201  # 201 Created
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@content_bp.route('/courses/<int:course_id>/modules/<int:module_id>/lessons', methods=['POST'])
def add_lesson(course_id, module_id):
    data = request.get_json()
    # Validação simples dos dados recebidos
    if not data or not all(k in data for k in ['titulo', 'tipo', 'url_conteudo']):
        return jsonify({"message": "Dados da aula incompletos."}), 400
        
    try:
        new_lesson = content_service.add_lesson_to_module(course_id, module_id, data)
        return jsonify(new_lesson), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 404  # Not Found (se o curso/módulo não existir)
    except Exception as e:
        return jsonify({"message": f"Erro interno: {e}"}), 500
    
# ======================================================
# ✏️ EDIÇÃO DE MÓDULO E AULA
# ======================================================

@content_bp.route('/courses/<int:course_id>/modules/<int:module_id>', methods=['PUT'])
def editar_modulo(course_id, module_id):
    data = request.get_json()
    if not data or "titulo" not in data:
        return jsonify({"message": "Título do módulo obrigatório."}), 400
    try:
        atualizado = content_service.update_module_title(course_id, module_id, data["titulo"])
        return jsonify(atualizado), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404

@content_bp.route('/courses/<int:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>', methods=['PUT'])
def editar_aula(course_id, module_id, lesson_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados obrigatórios não fornecidos."}), 400
    try:
        atualizado = content_service.update_lesson(course_id, module_id, lesson_id, data)
        return jsonify(atualizado), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
