# API de Predição com Flask e Scikit-Learn

Este projeto é uma API simples construída com Flask que utiliza um modelo de Machine Learning treinado com `scikit-learn` para prever se um cliente aceitará uma oferta, com base em atributos como idade, tempo de casa, etc.

## 🔧 Como rodar localmente

1. Clone o repositório:
```bash
git clone https://github.com/elsonsoares/ia-aplicada.git
cd ia-aplicada/01_modelo_basico
```

2. Crie um ambiente virtual (opcional):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a API localmente:
```bash
python api_modelo.py
```

## 🔥 Como testar

Use o Postman ou qualquer ferramenta de HTTP client para fazer uma requisição POST para:

```
http://localhost:5000/prever
```

Exemplo de JSON enviado:
```json
{
  "idade": 35,
  "tempo_casa": 4,
  "saldo": 15000
}
```

## 📁 Estrutura do Projeto
```
01_modelo_basico/
├── api_modelo.py
├── modelo_treinado.pkl
├── servicos/
│   └── predicao.py
├── requirements.txt
├── Procfile
```

## ☁️ Deploy (opcional)

Para deploy em plataformas como Render, Railway ou Deta, certifique-se de:
- Apontar o root do projeto para `01_modelo_basico`
- Ter um `Procfile` com: `web: gunicorn api_modelo:app`
- Ter `gunicorn` listado no `requirements.txt`
- Garantir que `modelo_treinado.pkl` esteja na mesma pasta do `api_modelo.py`