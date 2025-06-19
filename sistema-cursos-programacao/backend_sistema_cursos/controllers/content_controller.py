from flask import Blueprint, request, jsonify
from services import content_service

# Não é mais necessário manipular o sys.path aqui.
# O app principal cuidará do contexto de importação.

# Cria o Blueprint para este controlador
content_bp = Blueprint('content_controller', __name__)


@content_bp.route('/courses/<int:course_id>/contents', methods=['GET'])
def get_course_contents(course_id):
    content = content_service.get_content_by_course_id(course_id)
    if content:
        return jsonify(content), 200
    return jsonify({"message": "Conteúdo não encontrado para este curso."}), 404


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
