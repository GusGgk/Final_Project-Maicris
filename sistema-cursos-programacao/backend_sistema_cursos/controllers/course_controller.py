from flask import Blueprint, request, jsonify, current_app
from services.course_service import list_all_courses, add_course, get_course_by_id, update_course, delete_course
from utils.auth import token_required
from werkzeug.utils import secure_filename
import os
import uuid

course_bp = Blueprint("course_bp", __name__, url_prefix="/cursos")

# Diretório para armazenar imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', 'cursos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- ROTAS PÚBLICAS (NÃO EXIGEM LOGIN) ---

@course_bp.route("/", methods=["GET"])
def get_courses():
    courses = list_all_courses()
    return jsonify([course.to_dict() for course in courses]), 200

@course_bp.route("/<string:course_id>", methods=["GET"])
def get_course(course_id):
    course = get_course_by_id(course_id)
    if course:
        return jsonify(course.to_dict()), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

# --- ROTAS PROTEGIDAS (EXIGEM LOGIN E PERMISSÃO) ---

@course_bp.route("/", methods=["POST"])
@token_required
def post_course(current_user):
    if current_user['user_type'] not in ['admin', 'instrutor']:
        return jsonify({"mensagem": "Acesso negado. Apenas instrutores ou administradores."}), 403

    # Lê campos do formulário
    title = request.form.get("title")
    language = request.form.get("language")
    description = request.form.get("description")
    level = request.form.get("level")
    duration = request.form.get("duration")
    price = request.form.get("price")
    instructor_id = current_user['id']

    if not all([title, language, description, level, duration, price]):
        return jsonify({"mensagem": "Campos obrigatórios ausentes."}), 400

    # Trata upload de imagem
    image = request.files.get("image")
    image_filename = ""
    if image:
        filename = secure_filename(image.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        image.save(os.path.join(UPLOAD_FOLDER, unique_filename))
        image_filename = unique_filename

    dados = {
        "title": title,
        "language": language,
        "description": description,
        "level": level,
        "duration": duration,
        "price": price,
        "instructor_id": instructor_id,
        "image": image_filename
    }

    novo_curso = add_course(dados)
    return jsonify(novo_curso.to_dict()), 201

@course_bp.route("/<string:course_id>", methods=["PUT"])
@token_required
def put_course(current_user, course_id):
    if current_user['user_type'] not in ['admin', 'instrutor']:
        return jsonify({"mensagem": "Acesso negado."}), 403

    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"mensagem": "Curso não encontrado"}), 404

    if current_user['user_type'] != 'admin' and course.instructor_id != current_user['id']:
        return jsonify({"mensagem": "Acesso negado. Você não é o instrutor deste curso."}), 403

    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    updated_course = update_course(course_id, dados)
    if updated_course:
        return jsonify({"mensagem": "Curso atualizado com sucesso", "course": updated_course.to_dict()}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

@course_bp.route("/<string:course_id>", methods=["DELETE"])
@token_required
def delete_course_route(current_user, course_id):
    if current_user['user_type'] not in ['admin', 'instrutor']:
        return jsonify({"mensagem": "Acesso negado."}), 403

    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"mensagem": "Curso não encontrado"}), 404

    if current_user['user_type'] != 'admin' and course.instructor_id != current_user['id']:
        return jsonify({"mensagem": "Acesso negado. Você não é o instrutor deste curso."}), 403

    if delete_course(course_id):
        return jsonify({"mensagem": "Curso deletado com sucesso"}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404
