from flask import Blueprint, request, jsonify
from services.course_service import list_all_courses, add_course, get_course_by_id, update_course, delete_course

course_bp = Blueprint("course_bp", __name__, url_prefix="/cursos")

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

@course_bp.route("/", methods=["POST"])
def post_course():
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    required_fields = ["title", "language", "description", "level", "duration", "price", "instructor_id"]
    if not all(field in dados for field in required_fields):
        return jsonify({"mensagem": "Campos obrigatórios ausentes"}), 400

    new_course = add_course(dados)
    return jsonify(new_course.to_dict()), 201

@course_bp.route("/<string:course_id>", methods=["PUT"])
def put_course(course_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    updated_course = update_course(course_id, dados)
    if updated_course:
        return jsonify({"mensagem": "Curso atualizado com sucesso", "course": updated_course.to_dict()}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

@course_bp.route("/<string:course_id>", methods=["DELETE"])
def delete_course_route(course_id):
    if delete_course(course_id):
        return jsonify({"mensagem": "Curso deletado com sucesso"}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404
