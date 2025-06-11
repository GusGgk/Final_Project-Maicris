# Final_Project-Maicris
Projeto final desenvolvido por **Gustavo Giacoia**, **Eduardo Blasczak**, **João Carlos Mezari** e **Lucas Alfaro**.



# 📚 Sistema de Cursos de Programação

![Banner](https://media.giphy.com/media/dWesBcTLavkZuG35MI/giphy.gif)

> Plataforma de cursos online voltada para ensino de linguagens de programação. Projeto acadêmico com foco em backend Python, armazenamento local e interface funcional.


---

## 📚 Objetivo

Criar um sistema completo para gestão de cursos, com áreas para:

- Cadastro e gerenciamento de **usuários** (aluno, instrutor, admin)
- Controle de **cursos** com filtro por linguagem e nível
- Sistema de **matrículas**
- Organização futura de **conteúdos** e **progresso**
- Geração de **relatórios** administrativos

---

## 🧠 **Escopo do Sistema**

**Setores principais interligados:**

- 👤 Usuários (aluno, instrutor, admin)
- 🎓 Cursos (cadastro, filtros, níveis)
- 📂 Conteúdos (vídeos, PDFs, textos)
- ✅ Matrículas (inscrição em cursos)
- 📊 Progresso (porcentagem, acompanhamento)
- 🧾 Relatórios (usuários ativos, cursos mais acessados)
- 🛠 Administração (gerenciamento geral)
---
**Setores feitos e em desenvolvimento**
**Módulos principais:**

- 👤 Usuários (`/usuarios`)
- 🎓 Cursos (`/courses`)
- 📑 Matrículas (`/enrollments`)
- 🪧 Relatórios (futuro)
- 🎲 Progresso (futuro)
- 📂 Conteúdos (futuro)
- ⚒️ Administração (futuro)

---

## 📁 Estrutura do Projeto

```plaintext
sistema-cursos/
│
├── backend_sistema_cursos/
│   ├── main.py                 # Arquivo principal com rotas Flask
│   ├── services/               # Regras de negócio (usuários, cursos, matrículas)
│   ├── models/                 # Modelos de dados (User, Course, Enrollment)
│   ├── data/                   # Armazenamento local em arquivos .json
│   └── utils/ (futuro)         # Funções auxiliares
│
├── frontend/                   # HTML, CSS e JS integrando com a API
│
└── README.md


---

## 🛠 Como rodar o backend

```bash
# Requisitos
Python 3.10+
pip install flask flask-cors bcrypt

# Inicialização
cd backend_sistema_cursos
python main.py

