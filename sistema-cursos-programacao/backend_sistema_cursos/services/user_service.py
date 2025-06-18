import json
import bcrypt
import uuid
import os
from models.user import User
from utils.helpers import validar_email, validar_senha



# --- CAMINHO DO ARQUIVO ---
# Definido no topo para ser usado por todas as funções e de forma segura.
CAMINHO_JSON = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

# --- FUNÇÕES AUXILIARES INTERNAS ---

def _carregar_usuarios_raw():
    """Função interna para carregar a lista bruta de usuários do JSON."""
    if not os.path.exists(CAMINHO_JSON) or os.stat(CAMINHO_JSON).st_size == 0:
        return []
    with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _salvar_usuarios(lista_usuarios_dict):
    """Função interna para salvar a lista de dicionários de usuários no JSON."""
    with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
        json.dump(lista_usuarios_dict, f, indent=4, ensure_ascii=False)

# --- FUNÇÕES DE SERVIÇO PARA OS CONTROLLERS ---

def list_all_users():
    """Retorna uma lista de todos os usuários como objetos User."""
    usuarios_raw = _carregar_usuarios_raw()
    return [User.from_dict(u) for u in usuarios_raw]

def find_user_by_email(email):
    """Busca um usuário pelo email e retorna como objeto User."""
    usuarios_raw = _carregar_usuarios_raw()
    for u in usuarios_raw:
        if u["email"] == email:
            return User.from_dict(u)
    return None

def get_user_by_id(user_id):
    """Busca um usuário pelo ID e retorna como objeto User."""
    usuarios_raw = _carregar_usuarios_raw()
    for u in usuarios_raw:
        if u["id"] == user_id:
            return User.from_dict(u)
    return None

def add_user(dados):
    """Adiciona um novo usuário, validando e criptografando a senha."""
    usuarios_raw = _carregar_usuarios_raw()

    # Valida e-mail duplicado
    if any(u["email"] == dados["email"] for u in usuarios_raw):
        raise ValueError("Erro: E-mail já cadastrado")

    # Valida formato do e-mail
    if not validar_email(dados["email"]):
        raise ValueError("Erro: E-mail inválido")

    # Valida força da senha
    if not validar_senha(dados["password"]):
        raise ValueError("Erro: Senha fraca. Use pelo menos 6 caracteres, incluindo letras e números.")


    senha_bytes = dados["password"].encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)

    novo_usuario_obj = User(
        id=str(uuid.uuid4()),
        name=dados["name"],
        email=dados["email"],
        password=senha_hash.decode('utf-8'),
        user_type=dados["user_type"]
    )
    
    usuarios_raw.append(novo_usuario_obj.to_dict())
    _salvar_usuarios(usuarios_raw)

    return novo_usuario_obj

def update_user(user_id, novos_dados):
    """Atualiza um usuário, garantindo a criptografia da senha e validações."""
    from utils.helpers import validar_email, validar_senha  # Garantir import

    usuarios_raw = _carregar_usuarios_raw()
    usuario_encontrado_obj = None

    for i, u_dict in enumerate(usuarios_raw):
        if u_dict["id"] == user_id:

            # Valida email, se for alterar
            if 'email' in novos_dados:
                if not validar_email(novos_dados['email']):
                    raise ValueError("Email inválido.")

            # Valida senha, se for alterar
            if 'password' in novos_dados and novos_dados['password']:
                if not validar_senha(novos_dados['password']):
                    raise ValueError("Senha deve ter ao menos 6 caracteres, 1 letra e 1 número.")
                senha_bytes = novos_dados["password"].encode('utf-8')
                salt = bcrypt.gensalt()
                novos_dados['password'] = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

            # Atualiza os campos restantes (nome, tipo, etc)
            u_dict.update(novos_dados)
            usuario_encontrado_obj = User.from_dict(u_dict)
            usuarios_raw[i] = u_dict
            break

    if usuario_encontrado_obj:
        _salvar_usuarios(usuarios_raw)
        return usuario_encontrado_obj
    return None

def delete_user(user_id):
    """Remove um usuário do sistema."""
    usuarios_raw = _carregar_usuarios_raw()
    usuarios_filtrados = [u for u in usuarios_raw if u["id"] != user_id]
    
    if len(usuarios_raw) == len(usuarios_filtrados):
        return False
    
    _salvar_usuarios(usuarios_filtrados)
    return True