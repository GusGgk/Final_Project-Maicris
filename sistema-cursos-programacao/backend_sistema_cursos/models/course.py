# backend_sistema_cursos/models/course.py

class Course:
    def __init__(self, id, title, language, level, instructor_id):
        self.id = id
        self.title = title
        self.language = language
        self.level = level
        self.instructor_id = instructor_id # ID do instrutor que ministra o curso

    def setId(self, id):
        self.id = id

    def setTitle(self, title):
        self.title = title

    def setLanguage(self, language):
        self.language = language

    def setLevel(self, level):
        self.level = level

    def setInstructorId(self, instructor_id):
        self.instructor_id = instructor_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "language": self.language,
            "level": self.level,
            "instructor_id": self.instructor_id
        }

    @staticmethod
    def from_dict(data):
        return Course(
            data["id"],
            data["title"],
            data["language"],
            data["level"],
            data["instructor_id"]
        )

    def __str__(self):
        return f"Curso: {self.title} ({self.language}) - Nível: {self.level} - Instrutor ID: {self.instructor_id}"