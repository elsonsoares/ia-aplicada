from flask import Flask, request
from servicos.predicao import prever_cliente

app = Flask(__name__)

@app.route('/prever', methods=['POST'])
def prever():
    dados = request.get_json()
    return prever_cliente(dados)

if __name__ == '__main__':
    app.run(debug=True)
