import json
from models.user import User

def listar_usuarios():
    with open("data/users.json", "r", encoding="utf-8") as file:
        usuarios = json.load(file)
    return usuarios

def adicionar_usuario(dados):
    with open("data/users.json", "r", encoding="utf-8") as file:
        usuarios = json.load(file)

    novo = User(
        dados["id"],
        dados["name"],
        dados["email"],
        dados["password"],
        dados["type"]
    )

    usuarios.append(novo.to_dict())

    with open("data/users.json", "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4)

    return {"mensagem": f"Usuário {novo.name} cadastrado com sucesso"}
