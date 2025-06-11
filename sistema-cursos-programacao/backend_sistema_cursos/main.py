from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

# Importar serviços de usuário, curso e matrícula
from services.user_service import listar_usuarios, adicionar_usuario, get_user_by_id, update_user, delete_user
from services.course_service import list_all_courses, add_course, get_course_by_id, update_course, delete_course
from services.enrollment_service import list_all_enrollments, add_enrollment, get_enrollments_by_user_id, get_enrollments_by_course_id, delete_enrollment

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)  # habilita o CORS

# Caminhos para armazenamento local de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ENROLLMENTS_FILE = os.path.join(DATA_DIR, 'enrollments.json')

# -------------------- ROTAS DE TESTE --------------------
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"mensagem": "Servidor funcionando"}), 200

# -------------------- ROTAS DE USUÁRIOS --------------------
@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = listar_usuarios()
    return jsonify(usuarios), 200

@app.route("/usuarios/<string:user_id>", methods=["GET"])
def get_usuario_by_id(user_id):
    usuario = get_user_by_id(user_id)
    if usuario:
        return jsonify(usuario.to_dict()), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

@app.route("/usuarios", methods=["POST"])
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

@app.route("/usuarios/<string:user_id>", methods=["PUT"])
def put_usuario(user_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    usuario_atualizado = update_user(user_id, dados)
    if usuario_atualizado:
        return jsonify({"mensagem": "Usuário atualizado com sucesso", "usuario": usuario_atualizado.to_dict()}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

@app.route("/usuarios/<string:user_id>", methods=["DELETE"])
def delete_usuario(user_id):
    if delete_user(user_id):
        return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

# -------------------- ROTAS DE CURSOS --------------------
@app.route("/courses", methods=["GET"])
def get_courses():
    courses = list_all_courses()
    return jsonify([course.to_dict() for course in courses]), 200

@app.route("/courses/<string:course_id>", methods=["GET"])
def get_course(course_id):
    course = get_course_by_id(course_id)
    if course:
        return jsonify(course.to_dict()), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

@app.route("/courses", methods=["POST"])
def post_course():
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    required_fields = ["title", "language", "level", "instructor_id"]
    if not all(field in dados for field in required_fields):
        return jsonify({"mensagem": "Campos obrigatórios ausentes (title, language, level, instructor_id)"}), 400

    new_course = add_course(dados)
    return jsonify(new_course.to_dict()), 201

@app.route("/courses/<string:course_id>", methods=["PUT"])
def put_course(course_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    updated_course = update_course(course_id, dados)
    if updated_course:
        return jsonify({"mensagem": "Curso atualizado com sucesso", "course": updated_course.to_dict()}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

@app.route("/courses/<string:course_id>", methods=["DELETE"])
def delete_course_route(course_id):
    if delete_course(course_id):
        return jsonify({"mensagem": "Curso deletado com sucesso"}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

# -------------------- ROTAS DE MATRÍCULAS --------------------
@app.route("/enrollments", methods=["GET"])
def get_enrollments():
    enrollments = list_all_enrollments()
    return jsonify([e.to_dict() for e in enrollments]), 200

@app.route("/enrollments", methods=["POST"])
def post_enrollment():
    dados = request.get_json()
    if not dados or "user_id" not in dados or "course_id" not in dados:
        return jsonify({"mensagem": "Dados inválidos. Requer 'user_id' e 'course_id'."}), 400

    resultado = add_enrollment(dados["user_id"], dados["course_id"])
    if "Erro" in resultado["mensagem"]:
        return jsonify(resultado), 400
    return jsonify(resultado), 201

@app.route("/enrollments/user/<string:user_id>", methods=["GET"])
def get_enrollments_by_user(user_id):
    enrollments = get_enrollments_by_user_id(user_id)
    return jsonify([e.to_dict() for e in enrollments]), 200

@app.route("/enrollments/course/<string:course_id>", methods=["GET"])
def get_enrollments_by_course(course_id):
    enrollments = get_enrollments_by_course_id(course_id)
    return jsonify([e.to_dict() for e in enrollments]), 200

@app.route("/enrollments/<string:enrollment_id>", methods=["DELETE"])
def delete_enrollment_route(enrollment_id):
    if delete_enrollment(enrollment_id):
        return jsonify({"mensagem": "Matrícula deletada com sucesso"}), 200
    return jsonify({"mensagem": "Matrícula não encontrada"}), 404

# -------------------- INICIALIZAÇÃO --------------------
if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(ENROLLMENTS_FILE):
        with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    app.run(debug=True)
