import json
import bcrypt
import uuid
import os
from models.user import User

CAMINHO_JSON = "data/users.json"

# Garante que o arquivo existe
if not os.path.exists(CAMINHO_JSON):
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump([], f)

def listar_usuarios():
    with open(CAMINHO_JSON, "r", encoding="utf-8") as file:
        try:
            usuarios = json.load(file)
        except json.JSONDecodeError:
            usuarios = []
    return usuarios

def adicionar_usuario(dados):
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

    novo = User(
        str(uuid.uuid4()),  # Gera ID único
        dados["name"],
        dados["email"],
        senha_hash.decode('utf-8'),
        dados["type"]
    )

    usuarios.append(novo.to_dict())

    with open(CAMINHO_JSON, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4)

    return {"mensagem": f"Usuário {novo.name} cadastrado com sucesso"}
def get_user_by_id(user_id):
    usuarios = listar_usuarios()
    for u in usuarios:
        if u["id"] == user_id:
            return User.from_dict(u)
    return None

def update_user(user_id, novos_dados):
    usuarios = listar_usuarios()
    for i, u in enumerate(usuarios):
        if u["id"] == user_id:
            usuarios[i].update(novos_dados)
            with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4)
            return User.from_dict(usuarios[i])
    return None

def delete_user(user_id):
    usuarios = listar_usuarios()
    novos_usuarios = [u for u in usuarios if u["id"] != user_id]
    if len(novos_usuarios) == len(usuarios):
        return False
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump(novos_usuarios, f, indent=4)
    return True
