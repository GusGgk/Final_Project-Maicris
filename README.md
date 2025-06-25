# 🎓 Final_Project-Maicris

Projeto final desenvolvido por **Gustavo Giacoia**, **Eduardo Blasczak**, **João Carlos Mezari** e **Lucas Alfaro**.

---

## 📚 Sistema de Cursos de Programação

![Banner](https://media.giphy.com/media/dWesBcTLavkZuG35MI/giphy.gif)

> Plataforma de cursos online voltada para ensino de linguagens de programação. Projeto acadêmico com foco em backend Python, armazenamento local em `.json` e interface funcional integrada.

---

## 🎯 Objetivo

Criar um sistema completo de **gestão de cursos online**, com funcionalidades que abrangem:

- Cadastro e gerenciamento de **usuários** (`aluno`, `instrutor`, `admin`)
- Criação, edição e listagem de **cursos**
- Sistema de **matrículas**
- Organização de **módulos e aulas** (em andamento)
- Acompanhamento de **progresso** (futuro)
- Geração de **relatórios administrativos** (futuro)

---

## 🧠 Escopo Geral do Sistema

### **Módulos principais**

| Módulo       | Status       | Endpoint principal      |
|--------------|--------------|--------------------------|
| 👤 Usuários   | ✅ Concluído  | `/usuarios`              |
| 🎓 Cursos     | ✅ Concluído  | `/courses`               |
| 📑 Matrículas | ✅ Concluído  | `/enrollments`           |
| 📂 Conteúdos  | ✅ Concluído | `/contents`      |



---

## 📁 Estrutura do Projeto

```plaintext
sistema-cursos/
│
├── backend_sistema_cursos/
│   ├── main.py                  # Arquivo principal com rotas Flask
│   ├── controllers/             # Arquivos de controle para cada módulo
│   ├── services/                # Lógica de negócio (usuário, curso, matrícula, conteúdo)
    ├── static/                  # Armazena todas as fotos e links utilizados no cadastro dos cursos
│   ├── models/                  # Modelos de dados (User, Course, Enrollment, Content)
│   ├── data/                    # Armazenamento em JSON (usuarios.json, courses.json, etc.)
│   ├── utils/                   # Funções auxiliares (ex: criptografia, validações)
│   ├── start.sh                 # Script para iniciar o servidor no macOS/Linux
│   └── start.bat                # Script para iniciar o servidor no Windows
│
├── frontend/
|   ├── css/                     #todos os css das paginas abaixo
│   ├── cadastrar_usuario.html   # Formulário para cadastro de usuário
|   ├── login.html               # Login do usuário cadastrado
|   ├── menu.html                # Menu com todas as opções de acordo com usuário
|   ├── configurar_conta.html    # Configuração geral de informações da conta
│   ├── listar_usuarios.html     # Listagem de usuários
│   ├── cadastrar_curso.html     # Formulário para cadastro de curso
│   ├── listar_cursos.html       # Listagem de cursos
|   ├── criar_modulo.html        # Cria Modulo do curso
|   ├── criar_aula.html          # Cria aula do curso
│   ├── listar_matriculas.html   # Visualização de matrículas
│   ├── editar_curso.html        # Página de edição de curso
│   ├── gerenciar_conteudo.html  # Central para módulos e aulas
│   ├── editar_modulo.html       # Edição de módulo
│   └── editar_aula.html         # Edição de aula
│
└── README.md                    # Documentação do projeto
```

---

## 🛠 Como rodar o Backend

### ✅ Requisitos

- Python **3.10+**
- Instalar dependências com:

```bash
pip install 
bcrypt==4.3.0
blinker==1.9.0
click==8.2.1
colorama==0.4.6
Flask==3.1.1
flask-cors==6.0.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
PyJWT==2.10.1
Werkzeug==3.1.3
```

### ▶️ Iniciar o servidor

O projeto está pronto para testes imediatos. Basta entrar na pasta `backend_sistema_cursos` e executar o arquivo main.py:

- digitar `python main.py` no terminal para ligar o servidor e acessar o html de cadastro/login

---

## 🌐 Como acessar a API

Após iniciar o servidor, acesse no navegador ou via frontend local:

```
http://localhost:5000
```

### Exemplos de endpoints:

- `GET /usuarios` – Listar usuários
- `POST /usuarios` – Cadastrar usuário
- `GET /courses` – Listar cursos
- `POST /enrollments` – Realizar matrícula

---

## 🧪 Testes Sugeridos

- Cadastrar um novo instrutor e curso
- Matricular um aluno no curso
- Editar o curso e adicionar um módulo
- Editar título de uma aula
- Verificar JSONs atualizados na pasta `/data`

---

## 💡 Diferenciais

- Autenticação com token JWT
- Controle de permissões por tipo de usuário
- Armazenamento local em `.json` simulando banco de dados
- Integração com frontend HTML/CSS
- Estilo moderno com CSS personalizado

---

## 👨‍🏫 Observação

O projeto está pronto para testes imediatos. Basta entrar na pasta `backend_sistema_cursos` e executar o arquivo de acordo com seu sistema:

- digitar `python main.py` no terminal para ligar o servidor e acessar o html de cadastro/login