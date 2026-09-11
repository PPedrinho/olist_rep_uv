# Olist

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">

    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />

</a>

br e-commerce public dataset

---

## Project Organization

```
├── LICENSE
├── Makefile
├── README.md
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
│
├── docs
│
├── models
│   │
│   ├── best_model.joblib        <- Modelo final treinado
│   ├── metadata.json            <- Informações do modelo e threshold
│   └── olist_model.pkl          <- Modelo antigo
│
├── notebooks
│
├── pyproject.toml
│
├── references
│
├── reports
│   └── figures                <- Gráficos e resultados gerados
│
├── requirements.txt
│
├── setup.cfg
│
└── module_olist
    │
    ├── __init__.py
    │
    ├── config.py                <- Configurações e caminhos do projeto
    │
    ├── dataset.py               <- Carregamento e preparação dos dados
    │
    ├── features.py              <- Criação das features utilizadas no modelo
    │
    ├── inference.py             <- Execução de inferência utilizando modelo treinado
    │
    ├── explain.py               <- Geração da explicabilidade utilizando SHAP
    │
    ├── plots.py                 <- Criação de visualizações
    │
    ├── main.py                  <- Pipeline principal de treinamento
    │
    ├── teste.py                 <- Arquivo auxiliar para testes
    │
    └── modeling
        │
        ├── __init__.py
        │
        ├── pipeline.py          <- Construção dos pipelines dos modelos
        │
        ├── train.py             <- Treinamento dos modelos
        │
        ├── split.py             <- Separação treino/teste
        │
        ├── cross_validation.py  <- Validação cruzada e escolha do modelo
        │
        ├── evaluate.py          <- Avaliação dos modelos
        │
        ├── predict.py            <- Funções de carregamento e predição
        │
        └── interpret.py          <- Funções auxiliares para SHAP
```

---

# Execução do Projeto

## 1. Preparação do ambiente

Instalar as dependências:

```powershell
uv sync
```

Verificar o ambiente:

```powershell
uv run python --version
```

---

# 2. Treinamento do modelo

O treinamento completo deve ser executado através da:

```text
module_olist.main
```

Comando:

```powershell
uv run python -m module_olist.main
```

A `main.py` executa o pipeline completo:

```
Carregamento dos dados brutos
            ↓
Criação do dataset
            ↓
Engenharia de features
            ↓
Separação treino/teste
            ↓
Cross Validation
            ↓
Seleção do melhor modelo
            ↓
Treinamento final
            ↓
Salvar modelo treinado
            ↓
Salvar metadata
```

Ao final da execução serão gerados:

```
models/

├── best_model.joblib
└── metadata.json
```

O arquivo `best_model.joblib` contém o modelo final treinado.

O arquivo `metadata.json` contém:

- nome do modelo escolhido;
- threshold utilizado na classificação.

Exemplo:

```json
{
    "model_name": "LightGBM",
    "threshold": 0.14
}
```

---

# 3. Inferência do modelo

Após o treinamento, o modelo pode ser utilizado para realizar previsões sem necessidade de novo treinamento.

Comando:

```powershell
uv run python -m module_olist.inference
```

O fluxo realizado é:

```
Dados de entrada
        ↓
Carregar modelo salvo
        ↓
Carregar threshold
        ↓
Gerar probabilidades
        ↓
Classificação final
```

O resultado apresenta:

```
prob_is_late
prediction
```

Onde:

- `prob_is_late`: probabilidade do pedido apresentar atraso;
- `prediction`: classificação final utilizando o threshold definido.

Exemplo:

```
prob_is_late     prediction

0.08             0
0.21             1
0.04             0
```

Interpretação:

```
0 → Pedido previsto como pontual

1 → Pedido previsto como atrasado
```

---

# 4. Explicabilidade do modelo (SHAP)

A análise de explicabilidade deve ser executada após o treinamento do modelo.

Comando:

```powershell
uv run python -m module_olist.explain
```

O fluxo realizado é:

```
Carregar modelo treinado
          ↓
Preparar dados para SHAP
          ↓
Calcular valores SHAP
          ↓
Gerar gráficos de interpretação
```

O resultado será salvo em:

```
reports/figures/
```

Exemplo:

```
reports/

└── figures

    └── shap_summary.png
```

O gráfico permite analisar:

- quais variáveis possuem maior impacto no modelo;
- como cada variável influencia a previsão;
- quais características aumentam ou reduzem a probabilidade de atraso.

---

# 5. Fluxo recomendado de execução

## Primeira execução ou após alterações no modelo

Executar:

```powershell
uv run python -m module_olist.main
```

Esse processo realiza:

- preparação dos dados;
- criação das features;
- validação cruzada;
- treinamento;
- salvamento do modelo.

---

## Para gerar previsões

Após o modelo existir:

```powershell
uv run python -m module_olist.inference
```

Utilizado quando:

- novos pedidos precisam ser avaliados;
- deseja-se simular o ambiente de produção;
- não é necessário realizar novo treinamento.

---

## Para interpretar o modelo

Executar:

```powershell
uv run python -m module_olist.explain
```

Utilizado quando:

- deseja analisar importância das variáveis;
- gerar explicações do modelo;
- criar gráficos SHAP.

---

# Fluxo geral do projeto

```
                 TREINAMENTO

main.py

Dados brutos
      ↓
Dataset
      ↓
Features
      ↓
Cross Validation
      ↓
Treinamento
      ↓
best_model.joblib
metadata.json


                 INFERÊNCIA

inference.py

Novos dados
      ↓
Modelo salvo
      ↓
Predict
      ↓
Resultado


                 EXPLICAÇÃO

explain.py

Modelo salvo
      ↓
SHAP
      ↓
Interpretação
```

---

# Resumo dos comandos

## Treinar modelo

```powershell
uv run python -m module_olist.main
```

## Realizar inferência

```powershell
uv run python -m module_olist.inference
```

## Gerar explicabilidade SHAP

```powershell
uv run python -m module_olist.explain
```

---

# Observações

- A `main.py` deve ser executada sempre que houver alterações nos dados, features, modelos ou parâmetros de treinamento.
- O `inference.py` deve ser utilizado quando o modelo já estiver treinado e novas previsões forem necessárias.
- O `explain.py` deve ser utilizado para interpretar o comportamento do modelo utilizando SHAP.
- O modelo salvo em `models/best_model.joblib` permite realizar previsões sem executar novamente o treinamento.
- O arquivo `olist_model.pkl` corresponde a uma versão anterior do modelo e pode ser removido caso não seja mais utilizado.