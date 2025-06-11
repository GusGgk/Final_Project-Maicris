

class Enrollment:
    def __init__(self, id, user_id, course_id, enrollment_date):
        self.id = id
        self.user_id = user_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date

    def to_dict(self):
        """Converte o objeto Enrollment em um dicionário."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "enrollment_date": self.enrollment_date
        }

    @staticmethod
    def from_dict(data):
        """Cria um objeto Enrollment a partir de um dicionário."""
        return Enrollment(
            data["id"],
            data["user_id"],
            data["course_id"],
            data["enrollment_date"]
        )

    def __str__(self):
        return f"Matrícula ID: {self.id} - Usuário ID: {self.user_id} - Curso ID: {self.course_id} - Data: {self.enrollment_date}"