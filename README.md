# 📚 Escopo do Sistema de Cursos de Programação

## 🎯 Objetivo do Sistema
Criar um sistema funcional, local e apresentável, com backend em Python, armazenamento em arquivos JSON e opção de frontend, simulando uma plataforma de cursos com diferenciais como progresso, controle de usuários e relatórios.

---

## 🗂️ Módulos do Sistema (Setores)

1. **Usuários**: Cadastro, login, tipos (Aluno, Instrutor, Admin)
2. **Cursos**: Cadastro, filtros, níveis, linguagem
3. **Conteúdos**: Vídeos, PDFs, texto, associados aos cursos
4. **Matrículas**: Aluno se inscreve em curso
5. **Progresso**: Registro de avanço por aula e por aluno
6. **Relatórios**: Cursos mais acessados, atividade de usuários
7. **Administração**: Acesso restrito para controle do sistema

---

## 🔄 Relacionamento Entre Módulos

- Usuário -> Matrícula -> Curso -> Conteúdo  
- Usuário -> Progresso -> Relatório  
- Admin/Instrutor -> Gerencia cursos e usuários

---

## 💾 Estrutura de Armazenamento (JSON)

- `users.json`
- `courses.json`
- `contents.json`
- `enrollments.json`
- `progress.json`
- `reports.json` 

---

## 🧱 Arquitetura Técnica do Backend (Python)

```
backend_sistema_cursos/
├── main.py
├── controllers/
│   ├── user_controller.py
│   ├── course_controller.py
│   ├── enrollment_controller.py
├── services/
│   ├── user_service.py
│   ├── course_service.py
│   ├── enrollment_service.py
├── models/
│   ├── user.py
│   ├── course.py
│   ├── enrollment.py
│   ├── content.py
├── utils/
│   ├── helpers.py
├── data/
│   ├── users.json
│   ├── courses.json
│   ├── enrollments.json
│   ├── contents.json
│   ├── progress.json
```

---

## 🌐 Integração com Frontend 

**Frontend em HTML/CSS/JS ou React**:
- Página de login
- Catálogo de cursos com filtros
- Página de conteúdo do curso
- Painel do aluno
- Painel administrativo

---


