# Previsão de Churn de Clientes

Projeto de machine learning para prever o cancelamento de clientes (churn) em uma empresa de telecomunicações, com base no dataset Telco Customer Churn.

## Contexto de Negócio

A empresa enfrenta dificuldade na fidelização de clientes, com um número elevado de cancelamentos. O objetivo deste projeto é desenvolver um modelo preditivo capaz de identificar os clientes mais propensos a cancelar, permitindo a criação de campanhas e estratégias de retenção direcionadas.

O erro mais custoso para o negócio é o falso negativo, ou seja, deixar de identificar um cliente que de fato irá cancelar. Por isso, o recall da classe Churn foi definido como a métrica prioritária de avaliação, à frente da acurácia geral.

## Dataset

O projeto utiliza o dataset público Telco Customer Churn (`WA_Fn-UseC_-Telco-Customer-Churn.csv`), com 7043 registros de clientes e 21 colunas, incluindo dados demográficos, contratação de serviços, forma de pagamento e a variável alvo Churn.

## Estrutura do Projeto

```
.
├── Churn.ipynb
└── data/
    └── WA_Fn-UseC_-Telco-Customer-Churn.csv
```

## Etapas do Projeto

1. Entendimento do problema e contexto de negócio
2. Coleta e carregamento dos dados
3. Análise exploratória dos dados (EDA), incluindo auditoria de qualidade, análise univariada, verificação de outliers e análise bivariada
4. Pré-processamento, com tratamento de valores ausentes, encoding de variáveis categóricas, padronização de variáveis numéricas e balanceamento de classes com SMOTE
5. Treinamento dos modelos de Regressão Logística e Random Forest
6. Avaliação e comparação dos modelos
7. Interpretação dos coeficientes e considerações finais

## Principais Achados da Análise Exploratória

* A variável alvo é desbalanceada: 73,46% dos clientes não cancelam e 26,54% cancelam.
* Clientes que cancelam permanecem por menos tempo (mediana de 10 meses contra 38 meses) e pagam mensalidades mais altas.
* O tipo de contrato é um forte diferenciador: contratos mensais têm taxa de churn de 42,7%, contra 11,3% em contratos de 1 ano e 2,8% em contratos de 2 anos.
* Clientes com internet via fibra ótica cancelam mais (41,9%) do que clientes com DSL (18,9%) ou sem internet (7,4%).
* A ausência de serviços adicionais, como suporte técnico e segurança online, está associada a taxas de churn mais altas.
* O pagamento por Electronic check concentra a maior taxa de churn entre os métodos disponíveis.

## Metodologia

Os dados foram divididos em treino e teste (80/20) mantendo a proporção da variável alvo. Valores ausentes em TotalCharges foram tratados com a mediana calculada apenas no conjunto de treino, evitando vazamento de dados. Variáveis categóricas foram convertidas com one hot encoding e variáveis numéricas foram padronizadas com StandardScaler. O balanceamento de classes com SMOTE foi aplicado exclusivamente no conjunto de treino, preservando a distribuição original no conjunto de teste.

## Modelos Avaliados

Foram treinados e comparados dois modelos de classificação:

* Regressão Logística
* Random Forest

| Métrica | Regressão Logística | Random Forest |
|---|---|---|
| Recall Churn | 0,71 | 0,62 |
| ROC AUC | 0,819 | 0,820 |

## Conclusão

Considerando que o custo de não identificar um cancelamento é maior do que o custo de uma ação de retenção desnecessária, a Regressão Logística foi escolhida como o modelo mais adequado para esta aplicação, por apresentar maior recall na classe Churn. A interpretação dos coeficientes confirma os achados da análise exploratória: contrato mensal, internet via fibra ótica, pagamento por Electronic check e ausência de serviços como segurança online e suporte técnico aumentam a chance de cancelamento, enquanto maior tempo de permanência e contratos mais longos reduzem essa chance.

## Próximos Passos

* Testar outros algoritmos de classificação
* Ajustar o limiar de decisão para aumentar o recall da classe Churn
* Avaliar validação cruzada para checar a estabilidade das métricas
* Incorporar o custo de cada tipo de erro em uma análise de retorno financeiro das campanhas de retenção

## Tecnologias Utilizadas

* Python
* pandas e numpy
* matplotlib e seaborn
* scikit learn
* imbalanced learn (SMOTE)

## Como Executar

1. Instale as dependências: pandas, numpy, matplotlib, seaborn, scikit-learn, imbalanced-learn
2. Coloque o arquivo `WA_Fn-UseC_-Telco-Customer-Churn.csv` na pasta `data/`
3. Execute o notebook `Churn.ipynb` célula por célula
