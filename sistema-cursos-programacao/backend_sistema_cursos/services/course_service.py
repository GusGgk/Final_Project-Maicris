# backend_sistema_cursos/services/course_service.py

import json
import os
from ..models.course import Course # Importa a classe Course

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')

def _read_courses_data():
    """Lê os dados dos cursos do arquivo courses.json."""
    if not os.path.exists(COURSES_FILE) or os.stat(COURSES_FILE).st_size == 0:
        return []
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Course.from_dict(course_data) for course_data in data]

def _write_courses_data(courses):
    """Escreve os dados dos cursos no arquivo courses.json."""
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump([course.to_dict() for course in courses], f, indent=4, ensure_ascii=False)

def list_all_courses():
    """Retorna uma lista de todos os cursos."""
    return _read_courses_data()

def add_course(course_data):
    """Adiciona um novo curso."""
    courses = _read_courses_data()
    # Gera um novo ID para o curso
    new_id = 1 if not courses else max(course.id for course in courses) + 1
    new_course = Course(
        id=new_id,
        title=course_data['title'],
        language=course_data['language'],
        level=course_data['level'],
        instructor_id=course_data['instructor_id']
    )
    courses.append(new_course)
    _write_courses_data(courses)
    return new_course

def get_course_by_id(course_id):
    """Retorna um curso pelo seu ID."""
    courses = _read_courses_data()
    for course in courses:
        if course.id == course_id:
            return course
    return None

def update_course(course_id, new_course_data):
    """Atualiza um curso existente."""
    courses = _read_courses_data()
    for i, course in enumerate(courses):
        if course.id == course_id:
            courses[i].setTitle(new_course_data.get('title', course.title))
            courses[i].setLanguage(new_course_data.get('language', course.language))
            courses[i].setLevel(new_course_data.get('level', course.level))
            courses[i].setInstructorId(new_course_data.get('instructor_id', course.instructor_id))
            _write_courses_data(courses)
            return courses[i]
    return None

def delete_course(course_id):
    """Deleta um curso pelo seu ID."""
    courses = _read_courses_data()
    initial_len = len(courses)
    courses = [course for course in courses if course.id != course_id]
    if len(courses) < initial_len:
        _write_courses_data(courses)
        return True
    return False