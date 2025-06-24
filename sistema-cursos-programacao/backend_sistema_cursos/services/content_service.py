# ======================================================
# 📁 services/content_service.py
# Lógica de negócio para conteúdos de cursos (módulos e aulas)
# ======================================================

# -------------------- IMPORTAÇÕES --------------------
import json
from models.content import Modulo, Aula

# -------------------- CONSTANTES --------------------
DATA_FILE = 'data/contents.json'

# -------------------- FUNÇÕES INTERNAS DE ARQUIVO ----------------------
def _load_data():
    """Função interna para carregar os dados do JSON."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_data(data):
    """Função interna para salvar os dados no JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# -------------------- CONSULTA DE CONTEÚDO --------------------
def get_content_by_course_id(course_id: int):
    """Retorna todos os módulos e aulas de um curso específico."""
    all_contents = _load_data()
    for content in all_contents:
        if content.get('course_id') == course_id:
            return content
    return None # Retorna None se o curso não tiver conteúdo cadastrado

# -------------------- ADIÇÃO DE MÓDULOS E AULAS --------------------
def add_module_to_course(course_id: int, module_title: str):
    """Adiciona um novo módulo a um curso."""
    all_contents = _load_data()
    course_content = None
    
    # Encontra o bloco de conteúdo do curso
    for content in all_contents:
        if content.get('course_id') == course_id:
            course_content = content
            break

    # Se o curso ainda não tem nenhum conteúdo, cria a estrutura inicial
    if course_content is None:
        course_content = {"course_id": course_id, "modulos": []}
        all_contents.append(course_content)
    
    # Define o ID do novo módulo
    new_module_id = 1
    if course_content['modulos']:
        new_module_id = max(m['id'] for m in course_content['modulos']) + 1
        
    new_module = Modulo(id=new_module_id, titulo=module_title)
    course_content['modulos'].append(new_module.to_dict())
    
    _save_data(all_contents)
    return new_module.to_dict()

def add_lesson_to_module(course_id: int, module_id: int, lesson_data: dict):
    """Adiciona uma nova aula a um módulo específico de um curso."""
    all_contents = _load_data()
    course_content = None
    
    for content in all_contents:
        if content.get('course_id') == course_id:
            course_content = content
            break
            
    if not course_content:
        raise ValueError("Curso não encontrado ou sem conteúdo.")

    target_module = None
    for module in course_content['modulos']:
        if module.get('id') == module_id:
            target_module = module
            break

    if not target_module:
        raise ValueError("Módulo não encontrado.")
        
    # Define o ID da nova aula
    new_lesson_id = 1
    if target_module['aulas']:
        new_lesson_id = max(l['id'] for l in target_module['aulas']) + 1

    new_lesson = Aula(
        id=new_lesson_id,
        titulo=lesson_data['titulo'],
        tipo=lesson_data['tipo'],
        url_conteudo=lesson_data['url_conteudo']
    )
    
    target_module['aulas'].append(new_lesson.to_dict())
    _save_data(all_contents)
    return new_lesson.to_dict()

# -------------------- EDIÇÃO DE MÓDULOS E AULAS --------------------
def update_module_title(course_id: int, module_id: int, new_title: str):
    """Atualiza o título de um módulo específico."""
    all_contents = _load_data()

    for content in all_contents:
        if content.get("course_id") == course_id:
            for module in content.get("modulos", []):
                if module.get("id") == module_id:
                    module["titulo"] = new_title
                    _save_data(all_contents)
                    return module
    raise ValueError("Módulo não encontrado para este curso.")


def update_lesson(course_id: int, module_id: int, lesson_id: int, new_data: dict):
    """Atualiza os dados de uma aula específica."""
    all_contents = _load_data()

    for content in all_contents:
        if content.get("course_id") == course_id:
            for module in content.get("modulos", []):
                if module.get("id") == module_id:
                    for lesson in module.get("aulas", []):
                        if lesson.get("id") == lesson_id:
                            lesson["titulo"] = new_data.get("titulo", lesson["titulo"])
                            lesson["url_conteudo"] = new_data.get("url_conteudo", lesson["url_conteudo"])
                            _save_data(all_contents)
                            return lesson
    raise ValueError("Aula não encontrada.")
