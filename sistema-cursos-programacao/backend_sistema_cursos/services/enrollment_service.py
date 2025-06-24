# ======================================================
# 📁 services/enrollment_service.py
# Lógica de negócio para matrículas de usuários em cursos
# ======================================================

# -------------------- IMPORTAÇÕES --------------------
import json
import os
from datetime import datetime
from models.enrollment import Enrollment
from services.user_service import get_user_by_id
from services.course_service import get_course_by_id

# -------------------- CONFIGURAÇÃO DE CAMINHO --------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ENROLLMENTS_FILE = os.path.join(DATA_DIR, 'enrollments.json')

# ======================================================
# 📂 UTILITÁRIOS DE LEITURA/ESCRITA
# ======================================================

def _read_enrollments_data():
    """Lê os dados das matrículas do arquivo e retorna uma lista de objetos Enrollment."""
    if not os.path.exists(ENROLLMENTS_FILE) or os.stat(ENROLLMENTS_FILE).st_size == 0:
        return []
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Enrollment.from_dict(enrollment_data) for enrollment_data in data]

def _write_enrollments_data(enrollments):
    """Escreve uma lista de objetos Enrollment no arquivo JSON."""
    with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump([enrollment.to_dict() for enrollment in enrollments], f, indent=4, ensure_ascii=False)

# ======================================================
# 🧩 OPERAÇÕES DE MATRÍCULA
# ======================================================

def list_all_enrollments():
    """Retorna uma lista de todas as matrículas."""
    return _read_enrollments_data()

def get_enrollments_by_user_id(user_id):
    """Retorna todas as matrículas de um usuário específico."""
    enrollments = _read_enrollments_data()
    return [e for e in enrollments if str(e.user_id) == str(user_id)]

def get_enrollments_by_course_id(course_id):
    """Retorna todas as matrículas para um curso específico."""
    enrollments = _read_enrollments_data()
    return [e for e in enrollments if str(e.course_id) == str(course_id)]

def delete_enrollment(enrollment_id):
    """Remove uma matrícula com base no ID."""
    enrollments = _read_enrollments_data()
    updated = [e for e in enrollments if str(e.id) != str(enrollment_id)]
    if len(updated) < len(enrollments):
        _write_enrollments_data(updated)
        return True
    return False

def add_enrollment(user_id, course_id):
    """Adiciona uma nova matrícula, com validações de usuário, curso e duplicidade."""
    enrollments = _read_enrollments_data()

    user = get_user_by_id(user_id)
    if not user:
        return {"mensagem": f"Erro: Usuário com ID {user_id} não encontrado."}

    course = get_course_by_id(course_id)
    if not course:
        return {"mensagem": f"Erro: Curso com ID {course_id} não encontrado."}

    if any(e.user_id == user_id and e.course_id == course_id for e in enrollments):
        return {"mensagem": f"Erro: Usuário {user.name} já está matriculado no curso {course.title}."}

    new_id = str(int(datetime.now().timestamp()))
    enrollment_date = datetime.now().isoformat()

    new_enrollment = Enrollment(
        id=new_id,
        user_id=user_id,
        course_id=course_id,
        enrollment_date=enrollment_date
    )

    enrollments.append(new_enrollment)
    _write_enrollments_data(enrollments)

    return {
        "mensagem": f"Matrícula realizada com sucesso para o usuário {user.name} no curso {course.title}.",
        "enrollment": new_enrollment.to_dict()
    }

def get_enrollment_by_id(enrollment_id):
    """Busca uma matrícula pelo seu ID e retorna um objeto Enrollment."""
    enrollments = _read_enrollments_data()
    for enrollment in enrollments:
        if str(enrollment.id) == str(enrollment_id):
            return enrollment
    return None

def is_user_enrolled(user_id, course_id):
    """Verifica se o aluno está matriculado em um curso específico."""
    enrollments = _read_enrollments_data()
    return any(
        str(e.user_id) == str(user_id) and str(e.course_id) == str(course_id)
        for e in enrollments
    )
