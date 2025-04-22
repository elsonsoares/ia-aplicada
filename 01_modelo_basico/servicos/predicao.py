
import joblib
import pandas as pd
from flask import jsonify
from sklearn.tree import _tree
from datetime import datetime
import os

# Carregar modelo treinado uma única vez.
modelo = joblib.load('01_modelo_basico/modelo_treinado.pkl')
#caminho_base = os.path.dirname(os.path.abspath(__file__))
#caminho_modelo = os.path.join(caminho_base, '..', '01_modelo_basico', 'modelo_treinado.pkl')
#modelo = joblib.load(os.path.abspath(caminho_modelo))


# Função para extrair o caminho da decisão
def caminho_decisao(modelo, dados_entrada):
    arvore = modelo.tree_
    feature_names = ['idade', 'renda', 'tempo_de_casa']
    caminho = []
    node_indicator = modelo.decision_path(dados_entrada)
    leave_id = modelo.apply(dados_entrada)
    
    feature = arvore.feature
    threshold = arvore.threshold

    node_index = node_indicator.indices[node_indicator.indptr[0]:node_indicator.indptr[1]]

    for node_id in node_index:
        if leave_id[0] == node_id:
            break
        if dados_entrada.iloc[0, feature[node_id]] <= threshold[node_id]:
            threshold_sign = "<="
        else:
            threshold_sign = ">"

        caminho.append(f"{feature_names[feature[node_id]]} {threshold_sign} {threshold[node_id]:.2f}")

    return caminho

def salvar_historico(dados, resultado, interpretacao):
    arquivo = 'historico.csv'
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = {
        'data_hora': data_hora,
        'idade': dados['idade'],
        'renda': dados['renda'],
        'tempo_de_casa': dados['tempo_de_casa'],
        'resultado': resultado,
        'interpretacao': interpretacao
    }

    # Criar o arquivo se não existir
    if not os.path.isfile(arquivo):
        pd.DataFrame([linha]).to_csv(arquivo, index=False, mode='w')
    else:
        pd.DataFrame([linha]).to_csv(arquivo, index=False, mode='a', header=False)

def prever_cliente(dados):
    campos_esperados = ['idade', 'renda', 'tempo_de_casa']
    for campo in campos_esperados:
        if campo not in dados:
            return jsonify({'erro': f'Campo obrigatório ausente: {campo}'}), 400

        try:
            valor = float(dados[campo])
        except (ValueError, TypeError):
            return jsonify({'erro': f'O campo {campo} deve ser numérico'}), 400

    entrada = pd.DataFrame([[float(dados[campo]) for campo in campos_esperados]], columns=campos_esperados)
    resultado = modelo.predict(entrada)[0]

    interpretacao = 'Provavelmente compraria.' if resultado == 1 else 'Provavelmente não compraria.'

    # Salvar histórico automaticamente
    salvar_historico(dados, int(resultado), interpretacao)

    # Obter explicação detalhada
    explicacao = caminho_decisao(modelo, entrada)

    folha = modelo.apply(entrada)[0]
    compradores = modelo.tree_.value[folha][0][1]
    nao_compradores = modelo.tree_.value[folha][0][0]
    total = compradores + nao_compradores
    confianca = f"{compradores / total:.0%}" if resultado == 1 else f"{nao_compradores / total:.0%}"

    return jsonify({
        'entrada': dados,
        'resultado': int(resultado),
        'interpretacao': interpretacao,
        'explicacao': explicacao,
        'grupo_final': {
            'compradores': int(compradores),
            'nao_compradores': int(nao_compradores),
            'confianca': confianca
        }
    })
