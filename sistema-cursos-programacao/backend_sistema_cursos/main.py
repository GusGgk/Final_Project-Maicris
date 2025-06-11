from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Importar serviços de usuário e curso
# Estas importações já estão corretas para o cenário de execução a partir de backend_sistema_cursos
from services.user_service import listar_usuarios, adicionar_usuario, get_user_by_id, update_user, delete_user
from services.course_service import list_all_courses, add_course, get_course_by_id, update_course, delete_course

app = Flask(__name__)
CORS(app)

# --- Rotas para Usuários ---

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    """Retorna uma lista de todos os usuários."""
    usuarios = listar_usuarios()
    return jsonify(usuarios), 200

@app.route("/usuarios/<string:user_id>", methods=["GET"])
def get_usuario_by_id(user_id):
    """Retorna um usuário específico pelo ID."""
    usuario = get_user_by_id(user_id)
    if usuario:
        return jsonify(usuario.to_dict()), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

@app.route("/usuarios", methods=["POST"])
def post_usuario():
    """Adiciona um novo usuário."""
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400
    
    # Validar campos obrigatórios
    required_fields = ["name", "email", "password", "type"]
    if not all(field in dados for field in required_fields):
        return jsonify({"mensagem": "Campos obrigatórios ausentes (name, email, password, type)"}), 400

    resultado = adicionar_usuario(dados)
    if "Erro" in resultado["mensagem"]:
        return jsonify(resultado), 409 # Conflict
    return jsonify(resultado), 201

@app.route("/usuarios/<string:user_id>", methods=["PUT"])
def put_usuario(user_id):
    """Atualiza um usuário existente."""
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400
    
    usuario_atualizado = update_user(user_id, dados)
    if usuario_atualizado:
        return jsonify({"mensagem": "Usuário atualizado com sucesso", "usuario": usuario_atualizado.to_dict()}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

@app.route("/usuarios/<string:user_id>", methods=["DELETE"])
def delete_usuario(user_id):
    """Deleta um usuário."""
    if delete_user(user_id):
        return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
    return jsonify({"mensagem": "Usuário não encontrado"}), 404

# --- Rotas para Cursos ---

@app.route("/courses", methods=["GET"])
def get_courses():
    """Retorna uma lista de todos os cursos."""
    courses = list_all_courses()
    return jsonify([course.to_dict() for course in courses]), 200

@app.route("/courses/<string:course_id>", methods=["GET"])
def get_course(course_id):
    """Retorna um curso específico pelo ID."""
    course = get_course_by_id(course_id)
    if course:
        return jsonify(course.to_dict()), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

@app.route("/courses", methods=["POST"])
def post_course():
    """Adiciona um novo curso."""
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400
    
    # Validar campos obrigatórios
    required_fields = ["title", "language", "level", "instructor_id"]
    if not all(field in dados for field in required_fields):
        return jsonify({"mensagem": "Campos obrigatórios ausentes (title, language, level, instructor_id)"}), 400

    new_course = add_course(dados)
    return jsonify(new_course.to_dict()), 201

@app.route("/courses/<string:course_id>", methods=["PUT"])
def put_course(course_id):
    """Atualiza um curso existente."""
    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400
    
    updated_course = update_course(course_id, dados)
    if updated_course:
        return jsonify({"mensagem": "Curso atualizado com sucesso", "course": updated_course.to_dict()}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

@app.route("/courses/<string:course_id>", methods=["DELETE"])
def delete_course_route(course_id):
    """Deleta um curso."""
    if delete_course(course_id):
        return jsonify({"mensagem": "Curso deletado com sucesso"}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)