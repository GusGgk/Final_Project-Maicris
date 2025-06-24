import json
import uuid
import bcrypt
from models.user import User

# Caminho para o arquivo JSON que simula o banco de dados de usuários
USERS_FILE = 'data/users.json'

def _load_users():
    """Carrega os usuários do arquivo JSON."""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            return [User.from_dict(user) for user in users_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_users(users):
    """Salva a lista de usuários no arquivo JSON."""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        # AQUI ESTÁ A CORREÇÃO: Usamos o novo método para salvar
        json.dump([user.to_persistence_dict() for user in users], f, indent=4)

def list_all_users():
    """Retorna uma lista de todos os usuários."""
    return _load_users()

def find_user_by_email(email):
    """Encontra um usuário pelo seu endereço de e-mail."""
    users = _load_users()
    for user in users:
        if user.email == email:
            return user
    return None

def get_user_by_id(user_id):
    """Busca um usuário pelo seu ID."""
    users = _load_users()
    for user in users:
        if user.id == user_id:
            return user
    return None

def add_user(data):
    """Adiciona um novo usuário ao sistema."""
    if find_user_by_email(data['email']):
        raise ValueError("Erro: E-mail já cadastrado.")

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(
        id=str(uuid.uuid4()),
        name=data['name'],
        email=data['email'],
        password=hashed_password.decode('utf-8'),
        user_type=data['user_type']
    )
    
    users = _load_users()
    users.append(new_user)
    _save_users(users)
    
    return new_user

def update_user(user_id, data_to_update):
    """Atualiza os dados de um usuário existente."""
    users = _load_users()
    user_to_update = None
    for user in users:
        if user.id == user_id:
            user_to_update = user
            break
            
    if not user_to_update:
        return None

    # Atualiza os campos fornecidos
    for key, value in data_to_update.items():
        if hasattr(user_to_update, key):
            # Se for a senha, hasheia antes de atualizar
            if key == 'password' and value:
                hashed = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
                setattr(user_to_update, key, hashed.decode('utf-8'))
            elif key != 'password': # Evita apagar a senha se o campo vier vazio
                 setattr(user_to_update, key, value)

    _save_users(users)
    return user_to_update

def delete_user(user_id):
    """Deleta um usuário do sistema."""
    users = _load_users()
    user_found = False
    
    # Filtra a lista, mantendo todos os usuários exceto o que será deletado
    updated_users = [user for user in users if user.id != user_id]
    
    if len(updated_users) < len(users):
        user_found = True
        _save_users(updated_users)
        
    return user_found