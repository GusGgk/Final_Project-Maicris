from flask import Flask, jsonify

app = Flask(__name__)

from services.user_service import listar_usuarios

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    return jsonify(listar_usuarios()), 200


if __name__ == "__main__":
    app.run(debug=True)
