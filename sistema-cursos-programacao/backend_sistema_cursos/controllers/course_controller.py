from flask import Blueprint, request, jsonify
from services.course_service import list_all_courses, add_course, get_course_by_id, update_course, delete_course
#Importar o decorator de autenticação
from utils.auth import token_required

course_bp = Blueprint("course_bp", __name__, url_prefix="/cursos")

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
@token_required  #Adiciona o decorator para exigir token
def post_course(current_user):  #A função agora recebe o usuário logado
    
    # Verificação de autorização (permissão)
    if current_user['user_type'] not in ['admin', 'instrutor']:
        return jsonify({"mensagem": "Acesso negado. Permissão de instrutor ou admin necessária."}), 403

    dados = request.get_json()
    if not dados:
        return jsonify({"mensagem": "Dados inválidos"}), 400

    # O 'instructor_id' não é mais enviado pelo cliente, usamos o do usuário logado.
    required_fields = ["title", "language", "description", "level", "duration", "price"]
    if not all(field in dados for field in required_fields):
        return jsonify({"mensagem": "Campos obrigatórios ausentes"}), 400

    # Atribui o ID do usuário logado como o instrutor do curso.
    dados['instructor_id'] = current_user['id']

    new_course = add_course(dados)
    return jsonify(new_course.to_dict()), 201

@course_bp.route("/<string:course_id>", methods=["PUT"])
@token_required 
def put_course(current_user, course_id):  
    
    #Verificação de autorização
    if current_user['user_type'] not in ['admin', 'instrutor']:
        return jsonify({"mensagem": "Acesso negado. Permissão de instrutor ou admin necessária."}), 403

    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"mensagem": "Curso não encontrado"}), 404

    #Apenas um admin ou o instrutor dono do curso pode editá-lo.
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
    
    #Verificação de autorização
    if current_user['user_type'] not in ['admin', 'instrutor']:
        return jsonify({"mensagem": "Acesso negado. Permissão de instrutor ou admin necessária."}), 403

    course = get_course_by_id(course_id)
    if not course:
        return jsonify({"mensagem": "Curso não encontrado"}), 404
        
    #Apenas um admin ou o instrutor dono do curso pode deletá-lo.
    if current_user['user_type'] != 'admin' and course.instructor_id != current_user['id']:
        return jsonify({"mensagem": "Acesso negado. Você não é o instrutor deste curso."}), 403

    if delete_course(course_id):
        return jsonify({"mensagem": "Curso deletado com sucesso"}), 200
    return jsonify({"mensagem": "Curso não encontrado"}), 404