import json
import bcrypt
import uuid
import os
from models.user import User

# -------------------------
# Configuração e utilidades
# -------------------------

CAMINHO_JSON = "data/users.json"

# Garante que o arquivo users.json existe
if not os.path.exists(CAMINHO_JSON):
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump([], f)

def listar_usuarios():
    """Lê todos os usuários do arquivo JSON e retorna como lista de objetos User."""
    with open(CAMINHO_JSON, "r", encoding="utf-8") as file:
        try:
            usuarios = json.load(file)
            return [User.from_dict(u).to_dict() for u in usuarios]
        except json.JSONDecodeError:
            return []


def salvar_usuarios(lista_usuarios):
    """Salva a lista de usuários no arquivo JSON."""
    with open(CAMINHO_JSON, "w", encoding="utf-8") as file:
        json.dump(lista_usuarios, file, indent=4)

# -------------------------
# Operações de CRUD
# -------------------------

def get_user_by_id(user_id):
    """Busca um usuário específico pelo ID."""
    usuarios = listar_usuarios()
    for u in usuarios:
        if u["id"] == user_id:
            return User.from_dict(u)
    return None

def update_user(user_id, novos_dados):
    """Atualiza os dados de um usuário existente."""
    usuarios = listar_usuarios()
    for i, u in enumerate(usuarios):
        if u["id"] == user_id:
            usuarios[i].update(novos_dados)
            salvar_usuarios(usuarios)
            return User.from_dict(usuarios[i])
    return None

def delete_user(user_id):
    """Remove um usuário com base no ID."""
    usuarios = listar_usuarios()
    novos_usuarios = [u for u in usuarios if u["id"] != user_id]
    if len(novos_usuarios) == len(usuarios):
        return False
    salvar_usuarios(novos_usuarios)
    return True

# -------------------------
# Cadastro de novo usuário
# -------------------------

def adicionar_usuario(dados):
    """
    Adiciona um novo usuário ao sistema:
    - Valida e-mail
    - Verifica duplicidade
    - Gera ID único
    - Criptografa a senha
    """
    usuarios = listar_usuarios()

    # Verifica se o email já existe
    if any(u["email"] == dados["email"] for u in usuarios):
        return {"mensagem": "Erro: E-mail já cadastrado"}

    # Validação simples de e-mail
    if dados["email"].count("@") != 1 or "." not in dados["email"].split("@")[1]:
        return {"mensagem": "Erro: E-mail inválido"}

    # Criptografar a senha com bcrypt
    senha_bytes = dados["password"].encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)

    # Cria novo usuário com ID automático
    novo = User(
        str(uuid.uuid4()),
        dados["name"],
        dados["email"],
        senha_hash.decode('utf-8'),
        dados["type"]
    )

    # Adiciona e salva
    usuarios.append(novo.to_dict())
    salvar_usuarios(usuarios)

    return {
        "mensagem": f"Usuário {novo.name} cadastrado com sucesso",
        "id": novo.id  # Exibe o ID gerado
    }

def find_user_by_email(email):
    """Busca um usuário pelo seu email."""
    users = _load_users()
    for user_data in users:
        if user_data["email"] == email:
            return User.from_dict(user_data)
    return None