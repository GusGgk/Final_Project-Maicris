# backend_sistema_cursos/teste_course.py

import os
import sys
import json

# Adiciona o diretório pai ao PYTHONPATH para permitir importações relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_sistema_cursos.services import course_service
from backend_sistema_cursos.models.course import Course

# Define o caminho para o arquivo courses.json
COURSES_FILE = os.path.join(os.path.dirname(__file__), 'data', 'courses.json')

def testar_servico_cursos():
    print("--- Testando o Serviço de Cursos ---")

    # 1. Testar adicionar um curso
    print("\nAdicionando um novo curso...")
    new_course_data = {
        "title": "Curso Teste",
        "language": "Python",
        "level": "Iniciante",
        "instructor_id": "002" # exemplo com ID de instrutor (gk)
    }
    added_course = course_service.add_course(new_course_data)
    print(f"Curso adicionado: {added_course.to_dict()}")

    # 2. Verificar o conteúdo do courses.json após adição
    print(f"Verifique o arquivo '{COURSES_FILE}' para confirmar que o curso foi adicionado.")
    input("Pressione Enter para continuar após verificar o arquivo...")

    # 3. Testar listar todos os cursos
    print("\nListando todos os cursos...")
    all_courses = course_service.list_all_courses()
    if all_courses:
        print(f"Total de cursos encontrados: {len(all_courses)}")
        for course in all_courses:
            print(f"- {course.to_dict()}")
    else:
        print("Nenhum curso encontrado.")

    # 4. Testar buscar um curso por ID (se houver cursos)
    if all_courses:
        first_course_id = all_courses[0].id
        print(f"\nBuscando curso com ID: {first_course_id}...")
        found_course = course_service.get_course_by_id(first_course_id)
        if found_course:
            print(f"Curso encontrado: {found_course.to_dict()}")
        else:
            print(f"Curso com ID {first_course_id} não encontrado.")

    # 5. Testar atualizar um curso (se houver cursos)
    if all_courses:
        course_to_update_id = all_courses[0].id
        print(f"\nAtualizando curso com ID: {course_to_update_id}...")
        updated_data = {"level": "Intermediário", "title": "Python para Iniciantes"}
        updated_course = course_service.update_course(course_to_update_id, updated_data)
        if updated_course:
            print(f"Curso atualizado: {updated_course.to_dict()}")
        else:
            print(f"Curso com ID {course_to_update_id} não encontrado para atualização.")

        # Verificar o conteúdo do courses.json após atualização
        print(f"Verifique o arquivo '{COURSES_FILE}' para confirmar que o curso foi atualizado.")
        input("Pressione Enter para continuar após verificar o arquivo...")


    # 6. Testar deletar um curso (cuidado ao rodar isso em produção!)
    # Descomente para testar a deleção. Sugiro criar um curso de teste para deletar.
    # if all_courses:
    #     course_to_delete_id = all_courses[0].id # Ou adicione um curso especificamente para deletar
    #     print(f"\nDeletando curso com ID: {course_to_delete_id}...")
    #     if course_service.delete_course(course_to_delete_id):
    #         print(f"Curso com ID {course_to_delete_id} deletado com sucesso.")
    #     else:
    #         print(f"Falha ao deletar curso com ID {course_to_delete_id}.")

    #     # Verificar o conteúdo do courses.json após deleção
    #     print(f"Verifique o arquivo '{COURSES_FILE}' para confirmar a deleção.")
    #     input("Pressione Enter para continuar após verificar o arquivo...")


    print("\n--- Testes do Serviço de Cursos Concluídos ---")

if __name__ == "__main__":
    testar_servico_cursos()