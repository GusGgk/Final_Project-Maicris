

import json
import os
from ..models.course import Course

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
    
    # Gerar um novo ID numérico e depois convertê-lo para string
    # Certifica-se que os IDs existentes são convertidos para int antes de encontrar o máximo
    if not courses:
        new_id = 1
    else:
        # Pega todos os IDs, converte para int, encontra o máximo e adiciona 1
        # Usa um bloco try-except para lidar com IDs que não são números (embora não deva acontecer se os IDs forem numéricos)
        existing_ids = []
        for course in courses:
            try:
                existing_ids.append(int(course.id))
            except ValueError:
                # Se um ID não for um número, podemos ignorá-lo ou gerar um erro,
                # para este caso, vamos supor que os IDs são sempre numéricos em string
                pass 
        
        if existing_ids:
            new_id = max(existing_ids) + 1
        else:
            new_id = 1
            
    # Converte o novo ID para string para manter a consistência com o formato do JSON
    new_id_str = str(new_id)

    new_course = Course(
        id=new_id_str, # Usar o ID como string
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
        # Garante que a comparação seja entre strings, pois course.id é string
        if str(course.id) == str(course_id): 
            return course
    return None

def update_course(course_id, new_course_data):
    """Atualiza um curso existente."""
    courses = _read_courses_data()
    for i, course in enumerate(courses):
        # Garante que a comparação seja entre strings
        if str(course.id) == str(course_id): 
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
    # Garante que a comparação seja entre strings
    courses = [course for course in courses if str(course.id) != str(course_id)] 
    if len(courses) < initial_len:
        _write_courses_data(courses)
        return True
    return False