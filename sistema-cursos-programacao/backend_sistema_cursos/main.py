from flask import Flask, jsonify # Importa as classes Flask e jsonify do módulo flask

# A classe Flask é usada para criar a aplicação web.
# A função jsonify é usada para converter dicionários Python em respostas JSON.

app = Flask(__name__) # Cria uma instância da aplicação Flask.
# O argumento '__name__' ajuda o Flask a localizar recursos na aplicação.

from services.user_service import listar_usuarios # Importa a função listar_usuarios
# do módulo user_service dentro do pacote services.
# Esta função será responsável por obter a lista de usuários.

@app.route("/usuarios", methods=["GET"]) # Define uma rota para o URL "/usuarios".
# O decorador @app.route associa a função 'get_usuarios' a este URL.
# O argumento 'methods=["GET"]' especifica que esta rota responderá apenas a requisições GET.
def get_usuarios():
    """
    Retorna a lista de todos os usuários cadastrados.

    Esta função é acionada quando uma requisição GET é feita para /usuarios.
    Ela chama a função listar_usuarios para obter os dados e os retorna como JSON.
    """
    return jsonify(listar_usuarios()), 200 # Converte a lista de usuários em uma resposta JSON
    # e retorna essa resposta junto com o código de status HTTP 200 (OK).

if __name__ == "__main__":
    # Este bloco garante que o servidor Flask só será executado
    # quando o script for executado diretamente (não quando for importado como um módulo).
    app.run(debug=True) # Inicia o servidor de desenvolvimento do Flask.
    # 'debug=True' ativa o modo de depuração, que fornece um recarregamento automático
    # do servidor e mensagens de erro detalhadas no navegador.
