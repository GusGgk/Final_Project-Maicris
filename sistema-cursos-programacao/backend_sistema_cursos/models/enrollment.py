# ======================================================
# 📁 models/enrollment.py
# Modelo de dados para as Matrículas dos usuários nos cursos
# ======================================================

# -------------------- CLASSE ENROLLMENT --------------------
class Enrollment:
    def __init__(self, id: str, user_id: str, course_id: str, enrollment_date: str):
        """
        Representa a matrícula de um usuário em um curso.

        Parâmetros:
        - id: Identificador único da matrícula.
        - user_id: ID do usuário que se matriculou.
        - course_id: ID do curso no qual o usuário se matriculou.
        - enrollment_date: Data e hora em que a matrícula foi efetuada.
        """
        self.id = id
        self.user_id = user_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date

    def to_dict(self):
        """Retorna os dados da matrícula em formato de dicionário (para JSON)."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "enrollment_date": self.enrollment_date
        }

    @staticmethod
    def from_dict(data: dict):
        """Cria uma instância de Enrollment a partir de um dicionário."""
        return Enrollment(
            data["id"],
            data["user_id"],
            data["course_id"],
            data["enrollment_date"]
        )

    def __str__(self):
        """Retorna uma representação em string do objeto Enrollment."""
        return f"Matrícula ID: {self.id} - Usuário ID: {self.user_id} - Curso ID: {self.course_id}"