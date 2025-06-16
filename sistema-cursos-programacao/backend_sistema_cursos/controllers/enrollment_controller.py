from flask import Blueprint, request, jsonify
from services.enrollment_service import list_all_enrollments, add_enrollment, get_enrollments_by_user_id, get_enrollments_by_course_id, delete_enrollment

enrollment_bp = Blueprint("enrollment_bp", __name__, url_prefix="/enrollments")

@enrollment_bp.route("/", methods=["GET"])
def get_enrollments():
    enrollments = list_all_enrollments()
    return jsonify([e.to_dict() for e in enrollments]), 200

@enrollment_bp.route("/", methods=["POST"])
def post_enrollment():
    dados = request.get_json()
    if not dados or "user_id" not in dados or "course_id" not in dados:
        return jsonify({"mensagem": "Dados inválidos. Requer 'user_id' e 'course_id'."}), 400

    resultado = add_enrollment(dados["user_id"], dados["course_id"])
    if "Erro" in resultado["mensagem"]:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

@enrollment_bp.route("/user/<string:user_id>", methods=["GET"])
def get_enrollments_by_user(user_id):
    enrollments = get_enrollments_by_user_id(user_id)
    return jsonify([e.to_dict() for e in enrollments]), 200

@enrollment_bp.route("/course/<string:course_id>", methods=["GET"])
def get_enrollments_by_course(course_id):
    enrollments = get_enrollments_by_course_id(course_id)
    return jsonify([e.to_dict() for e in enrollments]), 200

@enrollment_bp.route("/<string:enrollment_id>", methods=["DELETE"])
def delete_enrollment_route(enrollment_id):
    if delete_enrollment(enrollment_id):
        return jsonify({"mensagem": "Matrícula deletada com sucesso"}), 200
    return jsonify({"mensagem": "Matrícula não encontrada"}), 404