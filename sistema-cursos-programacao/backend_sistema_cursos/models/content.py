# ======================================================
# 📁 models/content.py
# Modelos de dados para Módulos e Aulas dos cursos
# ======================================================

# -------------------- CLASSE AULA --------------------
class Aula:
    def __init__(self, id: int, titulo: str, tipo: str, url_conteudo: str):
        """
        Representa uma aula dentro de um módulo.

        Parâmetros:
        - id: Identificador único da aula (dentro do módulo).
        - titulo: Título da aula (ex: "Introdução a If/Else").
        - tipo: Tipo de conteúdo ('video' ou 'pdf').
        - url_conteudo: Link para o vídeo (YouTube) ou caminho do PDF.
        """
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.url_conteudo = url_conteudo

    def to_dict(self):
        """Retorna os dados da aula em formato de dicionário (para JSON)."""
        return self.__dict__

# -------------------- CLASSE MÓDULO --------------------
class Modulo:
    def __init__(self, id: int, titulo: str, aulas: list[Aula] = None):
        """
        Representa um módulo dentro de um curso.

        Parâmetros:
        - id: Identificador único do módulo (dentro do curso).
        - titulo: Nome/título do módulo (ex: "Estruturas Condicionais").
        - aulas: Lista de objetos Aula pertencentes a este módulo.
        """
        self.id = id
        self.titulo = titulo
        self.aulas = aulas if aulas is not None else []

    def to_dict(self):
        """Retorna os dados do módulo em formato de dicionário (para JSON)."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "aulas": [aula.to_dict() for aula in self.aulas]
        }
