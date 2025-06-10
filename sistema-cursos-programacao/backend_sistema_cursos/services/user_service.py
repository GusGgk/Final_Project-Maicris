import json
from models.user import User

CAMINHO_JSON = "data/users.json"

def listar_usuarios():
    with open(CAMINHO_JSON, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data  # já está em formato de dicionário, ideal pro jsonify

def adicionar_usuario(dados):
    with open(CAMINHO_JSON, "r", encoding="utf-8") as file:
        usuarios = json.load(file)

    novo = User(
        dados["id"],
        dados["name"],
        dados["email"],
        dados["password"],
        dados["type"]
    )

    usuarios.append(novo.to_dict())

    with open(CAMINHO_JSON, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4)

    return {"mensagem": f"Usuário {novo.name} cadastrado com sucesso"}
