
import json
import bcrypt
from models.user import User

CAMINHO_JSON = "data/users.json"

def listar_usuarios():
    with open(CAMINHO_JSON, "r", encoding="utf-8") as file:
        usuarios = json.load(file)
    return usuarios

def adicionar_usuario(dados):
    with open(CAMINHO_JSON, "r", encoding="utf-8") as file:
        usuarios = json.load(file)

    # Criptografar a senha com bcrypt
    senha_bytes = dados["password"].encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)

    novo = User(
        dados["id"],
        dados["name"],
        dados["email"],
        senha_hash.decode('utf-8'),
        dados["type"]
    )

    usuarios.append(novo.to_dict())

    with open(CAMINHO_JSON, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4)

    return {"mensagem": f"Usuário {novo.name} cadastrado com sucesso"}
