import json
import os
from models.course import Course

# -------------------------
# Configuração de caminho
# -------------------------

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')

# -------------------------
# Utilitários de leitura/escrita
# -------------------------

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

# -------------------------
# Operações de CRUD
# -------------------------

def list_all_courses():
    """Retorna uma lista de todos os cursos."""
    return _read_courses_data()

def get_course_by_id(course_id):
    """Retorna um curso pelo seu ID."""
    courses = _read_courses_data()
    for course in courses:
        if str(course.id) == str(course_id):
            return course
    return None

def add_course(course_data):
    """
    Adiciona um novo curso com ID numérico incremental.
    Garante que o ID seja único e armazenado como string.
    """
    courses = _read_courses_data()

    # Geração de novo ID
    if not courses:
        new_id = 1
    else:
        existing_ids = []
        for course in courses:
            try:
                existing_ids.append(int(course.id))
            except ValueError:
                pass
        new_id = max(existing_ids, default=0) + 1

    new_id_str = str(new_id)
    new_course = Course(
    id=new_id_str,
    title=course_data['title'],
    language=course_data['language'],
    description=course_data['description'],
    level=course_data['level'],
    duration=course_data['duration'],
    price=course_data['price'],
    instructor_id=course_data['instructor_id']
    )

    courses.append(new_course)
    _write_courses_data(courses)
    return new_course

def update_course(course_id, new_course_data):
    """Atualiza os dados de um curso existente."""
    courses = _read_courses_data()
    for i, course in enumerate(courses):
        if str(course.id) == str(course_id):
            courses[i].setTitle(new_course_data.get('title', course.title))
            courses[i].setLanguage(new_course_data.get('language', course.language))
            courses[i].description = new_course_data.get('description', course.description)
            courses[i].setLevel(new_course_data.get('level', course.level))
            courses[i].duration = new_course_data.get('duration', course.duration)
            courses[i].price = new_course_data.get('price', course.price)
            courses[i].setInstructorId(new_course_data.get('instructor_id', course.instructor_id))

            _write_courses_data(courses)
            return courses[i]
    return None

def delete_course(course_id): 
    """Remove um curso com base no ID."""
    courses = _read_courses_data()
    updated_courses = [course for course in courses if str(course.id) != str(course_id)]
    if len(updated_courses) < len(courses):
        _write_courses_data(updated_courses)
        return True
    return False
