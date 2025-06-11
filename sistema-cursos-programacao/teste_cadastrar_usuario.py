import uuid
import bcrypt
import re

def validar_email():
    while True:
        email = input("Digite seu email: ")

        if email.count("@") != 1:
            print("Email inválido! Deve conter exatamente um '@'.")
            continue

        dominio_partes = email.split(".")
        if len(dominio_partes) < 2 or len(dominio_partes[-1]) not in [2, 3]:
            print("Email inválido! O final deve ter 2 ou 3 letras após o ponto, como '.br' ou '.com'.")
            continue

        return email

def validar_senha():
    while True:
        senha = input("Digite sua senha: ")

        if len(senha) < 8:
            print("A senha deve ter pelo menos 8 caracteres.")
            continue

        if not re.search(r"[A-Z]", senha):
            print("A senha deve conter pelo menos uma letra maiúscula.")
            continue

        if not re.search(r"[0-9]", senha):
            print("A senha deve conter pelo menos um número.")
            continue

        if not re.search(r"[!@#$%^&*()_+\-=👦👦{};':\"\\|,.<>\/?]", senha):
            print("A senha deve conter pelo menos um caractere especial.")
            continue

        return senha

def cadastrar_cadastros():
    usuarios = []

    while True:
        name = input("Digite seu nome (ou digite 0 para sair): ")
        if name == "0":
            break

        email = validar_email()
        password = validar_senha()

        while True:
            type = input("Digite se você é aluno, instrutor ou admin: ").lower()
            if type in ["aluno", "instrutor", "admin"]:
                break
            print("Erro. Tipo inválido. Digite novamente: aluno, instrutor ou admin.")

        id = str(uuid.uuid4())

        senha_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt)

        usuario = {
            "id": id,
            "name": name,
            "email": email,
            "password": senha_hash.decode('utf-8'),
            "type": type
        }

        usuarios.append(usuario)

    return usuarios

usuarios_cadastrados = cadastrar_cadastros()
print("\nUsuários cadastrados com sucesso!!!")
print(usuarios_cadastrados)