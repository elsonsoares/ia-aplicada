import os

print("🔎 Diretório atual:", os.getcwd())
print("📂 Conteúdo do diretório:")
print(os.listdir(os.getcwd()))

for root, dirs, files in os.walk(".", topdown=True):
    for name in files:
        print(os.path.join(root, name))

        
from flask import Flask, request
from servicos.predicao import prever_cliente

app = Flask(__name__)

@app.route('/prever', methods=['POST'])
def prever():
    dados = request.get_json()
    return prever_cliente(dados)

if __name__ == '__main__':
    app.run(debug=True)
