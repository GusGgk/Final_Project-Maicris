class Curso:
    lista_cursos = []

    def __init__(self, nome, descricao, carga_horaria, nivel):
        self.nome = nome
        self.descricao = descricao
        self.carga_horaria = carga_horaria
        self.nivel = nivel

    def salvar(self):
        Curso.lista_cursos.append(self)

    @staticmethod
    def listar_cursos():
        if not Curso.lista_cursos:
            print("Nenhum curso cadastrado.")
            return
        for i, curso in enumerate(Curso.lista_cursos, 1):
            print(f"\nCurso {i}:")
            print(f"Nome: {curso.nome}")
            print(f"Descrição: {curso.descricao}")
            print(f"Carga Horária: {curso.carga_horaria} horas")
            print(f"Nível: {curso.nivel}")

# Cadastrando cursos automaticamente com níveis
cursos_predefinidos = [
    ("Python", "Curso de programação com a linguagem Python.", 40, "iniciante"),
    ("Lógica de programação", "Fundamentos da lógica para desenvolvimento.", 30, "iniciante"),
    ("C#", "Programação com C# e .NET.", 50, "intermediário"),
    ("Java", "Desenvolvimento com a linguagem Java.", 50, "intermediário"),
    ("Web (HTML, CSS, JS)", "Criação de páginas web com HTML, CSS e JavaScript.", 45, "iniciante"),
    ("React", "Desenvolvimento de interfaces com React.js.", 35, "intermediário"),
    ("C++", "Programação estruturada e orientada a objetos com C++.", 50, "intermediário"),
    ("Banco de Dados", "Modelagem e manipulação de bancos de dados relacionais.", 40, "intermediário"),
    ("DevOps", "Integração e entrega contínua com práticas DevOps.", 25, "intermediário"),
]

# Criando objetos e salvando na lista
for nome, descricao, carga, nivel in cursos_predefinidos:
    curso = Curso(nome, descricao, carga, nivel)
    curso.salvar()

# Exibindo os cursos cadastrados
print("\n--- Lista de Cursos Cadastrados ---")
Curso.listar_cursos()
