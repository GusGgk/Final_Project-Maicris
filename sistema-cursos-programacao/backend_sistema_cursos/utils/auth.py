# ======================================================
# 📁 utils/auth.py
# Middleware para autenticação via token JWT
# ======================================================

# -------------------- IMPORTAÇÕES --------------------
from functools import wraps
from flask import request, jsonify, current_app
import jwt
from services.user_service import get_user_by_id

# -------------------- DECORADOR DE AUTENTICAÇÃO --------------------
def token_required(f):
    """
    Decorador que protege rotas com verificação de token JWT.

    Espera um cabeçalho Authorization no formato:
    Authorization: Bearer <token>
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Tenta extrair o token do cabeçalho
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Formato do token inválido'}), 401

        if not token:
            return jsonify({'message': 'Token está faltando'}), 401

        try:
            # Decodifica o token com a chave secreta da aplicação
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            # Busca o usuário no "banco de dados"
            current_user = get_user_by_id(data['sub'])
            if not current_user:
                return jsonify({'message': 'Usuário do token não encontrado'}), 401

            current_user_dict = current_user.to_dict()

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirou'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        # Executa a função original com o usuário como argumento adicional
        return f(current_user_dict, *args, **kwargs)

    return decorated
