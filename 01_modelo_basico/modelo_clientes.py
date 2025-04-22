
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Carregar dataset
df = pd.read_csv('clientes_simulados.csv')

# Separar variáveis e alvo
X = df[['idade', 'renda', 'tempo_de_casa']]
y = df['comprou']

# Dividir treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Treinar modelo
modelo = DecisionTreeClassifier()
modelo.fit(X_train, y_train)

# Testar modelo
predicoes = modelo.predict(X_test)
print("Acurácia:", accuracy_score(y_test, predicoes))

# Simular entrada nova
entrada = pd.DataFrame([[40, 7000, 5]], columns=['idade', 'renda', 'tempo_de_casa'])
print("Predição para novo cliente:", modelo.predict(entrada))

import joblib

# Salvar o modelo treinado
joblib.dump(modelo, 'modelo_treinado.pkl')
print("Modelo salvo como modelo_treinado.pkl")
