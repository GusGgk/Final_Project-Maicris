# backend_sistema_cursos/models/course.py

class Course:
    def __init__(self, id, title, language,description, level, duration, price,instructor_id, image):
        self.id = id
        self.title = title
        self.language = language
        self.description = description
        self.level = level
        self.duration = duration
        self.price = price
        self.instructor_id = instructor_id
        self.image = image


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

    def setImage(self, image):
        self.image = image
    
    def to_dict(self):
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
    def from_dict(data):
        return Course(
            data["id"],
            data["title"],
            data["language"],
            data["description"],
            data["level"],
            data["duration"],
            data["price"],
            data["instructor_id"],
            data.get("image", "")
        )

    def __str__(self):
        return f"Curso: {self.title} ({self.language}) - Nível: {self.level} - Duração do Curso: {self.duration} - Instrutor ID: {self.instructor_id}"