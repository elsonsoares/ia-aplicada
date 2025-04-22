import joblib
import pandas as pd

# Carregar o modelo salvo
modelo = joblib.load('modelo_treinado.pkl')

# Criar dados de entrada com nomes de coluna
entrada = pd.DataFrame([[50, 2500, 25]], columns=['idade', 'renda', 'tempo_de_casa'])

# Fazer predição
resultado = modelo.predict(entrada)
print("Predição:", resultado[0])

from sklearn import tree
import matplotlib.pyplot as plt

# Visualizar árvore
plt.figure(figsize=(10,6))
tree.plot_tree(modelo, feature_names=['idade', 'renda', 'tempo_de_casa'], class_names=['Não Compra', 'Compra'], filled=True)
plt.show()
