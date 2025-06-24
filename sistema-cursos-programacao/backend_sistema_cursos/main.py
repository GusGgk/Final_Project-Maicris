# ======================================================
# 📁 main.py
# Arquivo principal para inicialização do servidor Flask
# ======================================================

# -------------------- IMPORTAÇÕES --------------------
from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

# Importação dos Blueprints dos módulos
from controllers.user_controller import user_bp
from controllers.course_controller import course_bp
from controllers.enrollment_controller import enrollment_bp
from controllers.content_controller import content_bp  

# -------------------- CONFIGURAÇÃO DO APP --------------------
app = Flask(__name__)

# Chave secreta para autenticação JWT
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-forte-e-dificil-de-adivinhar'

# Habilita o CORS
CORS(app)

# Caminhos para diretórios e arquivos de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ENROLLMENTS_FILE = os.path.join(DATA_DIR, 'enrollments.json')

# -------------------- ROTA DE TESTE --------------------
@app.route("/ping", methods=["GET"])
def ping():
    """Verifica se o servidor está online."""
    return jsonify({"mensagem": "Servidor funcionando"}), 200

# -------------------- REGISTRO DOS BLUEPRINTS --------------------
app.register_blueprint(user_bp)
app.register_blueprint(course_bp)
app.register_blueprint(enrollment_bp)
app.register_blueprint(content_bp)  

# -------------------- INICIALIZAÇÃO DO SERVIDOR --------------------
if __name__ == "__main__":
    # Garante que o diretório de dados exista
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Garante que o arquivo de matrículas exista
    if not os.path.exists(ENROLLMENTS_FILE):
        with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    # Inicia o servidor Flask
    app.run(debug=True)
