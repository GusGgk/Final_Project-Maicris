# models/content.py

class Aula:
    def __init__(self, id: int, titulo: str, tipo: str, url_conteudo: str):
        """
        Inicializa uma Aula.
        - id: Identificador único da aula (dentro do módulo).
        - titulo: Título da aula (ex: "Introdução a If/Else").
        - tipo: 'video' ou 'pdf'.
        - url_conteudo: Link para o vídeo no YouTube ou caminho para o PDF.
        """
        self.id = id
        self.titulo = titulo
        self.tipo = tipo
        self.url_conteudo = url_conteudo

    def to_dict(self):
        return self.__dict__

class Modulo:
    def __init__(self, id: int, titulo: str, aulas: list[Aula] = None):
        """
        Inicializa um Módulo.
        - id: Identificador único do módulo (dentro do curso).
        - titulo: Título do módulo (ex: "Estruturas Condicionais").
        - aulas: Uma lista de objetos da classe Aula.
        """
        self.id = id
        self.titulo = titulo
        self.aulas = aulas if aulas is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "aulas": [aula.to_dict() for aula in self.aulas]
        }