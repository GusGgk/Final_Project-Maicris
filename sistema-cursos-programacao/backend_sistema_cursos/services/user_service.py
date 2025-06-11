import json
import os
from models.user import User # Era 'from models.user import User' ou 'from ..models.user import User'

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

def _read_users_data():
    """Lê os dados dos usuários do arquivo users.json."""
    if not os.path.exists(USERS_FILE) or os.stat(USERS_FILE).st_size == 0:
        return []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [User.from_dict(user_data) for user_data in data]

def _write_users_data(users):
    """Escreve os dados dos usuários no arquivo users.json."""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump([user.to_dict() for user in users], f, indent=4, ensure_ascii=False)

def listar_usuarios():
    """Retorna uma lista de todos os usuários."""
    return [user.to_dict() for user in _read_users_data()]

def adicionar_usuario(dados):
    """Adiciona um novo usuário."""
    users = _read_users_data()
    # Gerar um novo ID simples baseado no timestamp para garantir unicidade
    new_id = str(len(users) + 1) # Pode ser melhorado para IDs mais robustos

    new_user = User(
        id=dados.get("id", new_id), # Usa o ID fornecido ou gera um novo
        name=dados['name'],
        email=dados['email'],
        password=dados['password'],
        type=dados['type']
    )

    # Verifica se o ID já existe
    if any(user.id == new_user.id for user in users):
        return {"mensagem": f"Erro: Usuário com ID {new_user.id} já existe."}

    # Verifica se o email já existe
    if any(user.email == new_user.email for user in users):
        return {"mensagem": f"Erro: Usuário com email {new_user.email} já existe."}

    users.append(new_user)
    _write_users_data(users)
    return {"mensagem": f"Usuário {new_user.name} cadastrado com sucesso", "usuario": new_user.to_dict()}

def get_user_by_id(user_id):
    """Retorna um usuário pelo seu ID."""
    users = _read_users_data()
    for user in users:
        if str(user.id) == str(user_id):
            return user
    return None

def update_user(user_id, new_user_data):
    """Atualiza um usuário existente."""
    users = _read_users_data()
    for i, user in enumerate(users):
        if str(user.id) == str(user_id):
            # Atualiza apenas os campos fornecidos em new_user_data
            user.setName(new_user_data.get('name', user.name))
            user.setEmail(new_user_data.get('email', user.email))
            user.setPassword(new_user_data.get('password', user.password))
            user.setType(new_user_data.get('type', user.type))
            _write_users_data(users)
            return user
    return None

def delete_user(user_id):
    """Deleta um usuário pelo seu ID."""
    users = _read_users_data()
    initial_len = len(users)
    users = [user for user in users if str(user.id) != str(user_id)]
    if len(users) < initial_len:
        _write_users_data(users)
        return True
    return False