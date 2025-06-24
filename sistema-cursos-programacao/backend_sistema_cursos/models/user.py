# ======================================================
# 📁 models/user.py
# Modelo de dados para os Usuários (alunos, instrutores, admins)
# ======================================================

# -------------------- CLASSE USER --------------------
class User:
    def __init__(self, id: str, name: str, email: str, password: str, user_type: str):
        """
        Representa um usuário da plataforma.

        Parâmetros:
        - id: Identificador único do usuário (UUID).
        - name: Nome completo do usuário.
        - email: Endereço de e-mail (usado para login).
        - password: Senha do usuário (deve ser armazenada como hash).
        - user_type: Tipo de usuário ('aluno', 'instrutor', ou 'admin').
        """
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type

    def to_dict(self):
        """
        Retorna os dados do usuário em formato de dicionário (para JSON).
        IMPORTANTE: A senha é omitida por segurança.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "user_type": self.user_type
            # A senha nunca é retornada para o cliente
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Cria uma instância de User a partir de um dicionário (vindo do JSON).
        """
        return User(
            data["id"],
            data["name"],
            data["email"],
            data["password"],
            data.get("user_type") or data.get("type") # Compatibilidade com 'type'
        )

    def __str__(self):
        """Retorna uma representação em string do objeto User."""
        return f"Usuário: {self.name} ({self.email}) - Tipo: {self.user_type}"