# Relatório de Qualidade de Dados (Skill conferir-csv)

- **Arquivo verificado:** `dados\fornecedores_erro.csv`
- **Total de linhas de dados:** 4
- **Total de colunas:** 5 (`fornecedor, preco_unitario, prazo_dias, defeitos_pct, suporte_nota`)
- **Linhas duplicadas:** 0

## 1. Problemas Encontrados e Evidências Numéricas

Foram identificados **2 valores ausentes** na base de dados:

| Linha no CSV | Fornecedor | Coluna Afetada | Problema Detectado |
| :---: | :--- | :--- | :--- |
| 3 | **Beta** | `suporte_nota` | Valor ausente (vazio) |
| 5 | **Delta** | `preco_unitario` | Valor ausente (vazio) |

## 2. Tratamentos Propostos (Regras de Governança)

1. **Nunca alterar o arquivo original** (`dados/fornecedores_erro.csv`), conforme as regras do projeto.
2. **Tratamento para `preco_unitario` do fornecedor Delta:**
   - *Alerta:* Não se deve preencher com zero (preço zero indicaria gratuidade e distorceria qualquer análise).
   - *Proposta:* Obter a cotação correta com o fornecedor ou descartar a proposta caso esteja incompleta.
3. **Tratamento para `suporte_nota` do fornecedor Beta:**
   - *Alerta:* Ausência é diferente de zero (nota zero indicaria suporte péssimo, mas o dado apenas não foi informado).
   - *Proposta:* Coletar a nota oficial de suporte ou estimar com a média dos demais fornecedores, registrando a ressalva.
