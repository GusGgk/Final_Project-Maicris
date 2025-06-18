import re

def validar_email(email: str) -> bool:
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(padrao, email) is not None

def validar_senha(senha: str) -> bool:
    if len(senha) < 6:
        return False
    if not any(c.isalpha() for c in senha):
        return False
    if not any(c.isdigit() for c in senha):
        return False
    return True

