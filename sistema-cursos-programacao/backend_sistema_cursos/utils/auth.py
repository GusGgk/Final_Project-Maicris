from functools import wraps
from flask import request, jsonify, current_app
import jwt
from services.user_service import get_user_by_id

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # O token é esperado no cabeçalho 'Authorization' como 'Bearer <token>'
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Extrai o token do cabeçalho
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Formato do token inválido'}), 401

        if not token:
            return jsonify({'message': 'Token está faltando'}), 401

        try:
            # Decodifica o token usando a nossa chave secreta
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Busca o usuário no "banco de dados" para garantir que ele ainda existe
            current_user = get_user_by_id(data['sub'])
            if not current_user:
                return jsonify({'message': 'Usuário do token não encontrado'}), 401
            
            # Converte o usuário para um dicionário para fácil acesso no controller
            current_user_dict = current_user.to_dict()

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirou'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        # Passa o usuário decodificado para a rota
        return f(current_user_dict, *args, **kwargs)

    return decorated