# main.py

from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

# Importar os Blueprints dos controllers
from controllers.user_controller import user_bp
from controllers.course_controller import course_bp
from controllers.enrollment_controller import enrollment_bp

# Cria a aplicação Flask
app = Flask(__name__)

# Adição da chave secreta para a criação dos tokens JWT.
app.config['SECRET_KEY'] = 'uma-chave-secreta-bem-forte-e-dificil-de-adivinhar'


CORS(app)  # habilita o CORS

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
ENROLLMENTS_FILE = os.path.join(DATA_DIR, 'enrollments.json')

# -------------------- ROTA DE TESTE --------------------
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"mensagem": "Servidor funcionando"}), 200

# -------------------- REGISTRO DOS BLUEPRINTS --------------------
app.register_blueprint(user_bp)
app.register_blueprint(course_bp)
app.register_blueprint(enrollment_bp)

# -------------------- INICIALIZAÇÃO --------------------
if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Garante que o arquivo de matrículas exista
    if not os.path.exists(ENROLLMENTS_FILE):
        with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    app.run(debug=True)