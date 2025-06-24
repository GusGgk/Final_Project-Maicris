# ======================================================
# 📁 models/course.py
# Modelo de dados para os Cursos da plataforma
# ======================================================

# -------------------- CLASSE COURSE --------------------
class Course:
    def __init__(self, id: str, title: str, language: str, description: str, level: str, duration: str, price: float, instructor_id: str, image: str):
        """
        Representa um curso na plataforma de ensino.

        Parâmetros:
        - id: Identificador único do curso.
        - title: Título do curso (ex: "Python para Iniciantes").
        - language: Idioma do curso (ex: "Português").
        - description: Descrição detalhada do conteúdo do curso.
        - level: Nível de dificuldade (ex: "Iniciante", "Intermediário").
        - duration: Duração total do curso (ex: "10 horas").
        - price: Preço do curso.
        - instructor_id: ID do usuário instrutor responsável pelo curso.
        - image: Caminho ou URL para a imagem de capa do curso.
        """
        self.id = id
        self.title = title
        self.language = language
        self.description = description
        self.level = level
        self.duration = duration
        self.price = price
        self.instructor_id = instructor_id
        self.image = image

    def to_dict(self):
        """Retorna os dados do curso em formato de dicionário (para JSON)."""
        return {
            "id": self.id,
            "title": self.title,
            "language": self.language,
            "description": self.description,
            "level": self.level,
            "duration": self.duration,
            "price": self.price,
            "instructor_id": self.instructor_id,
            "image": self.image
        }

    @staticmethod
    def from_dict(data: dict):
        """Cria uma instância de Course a partir de um dicionário."""
        return Course(
            data["id"],
            data["title"],
            data["language"],
            data["description"],
            data["level"],
            data["duration"],
            data["price"],
            data["instructor_id"],
            data.get("image", "")  # Garante que 'image' sempre exista
        )

    def __str__(self):
        """Retorna uma representação em string do objeto Course."""
        return f"Curso: {self.title} ({self.language}) - Nível: {self.level}"