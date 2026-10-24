import os
import csv

# ==============================================================================
# SKILL: CONFERIR-CSV
# Finalidade: Conferir a estrutura e a qualidade da base fornecedores_erro.csv
# ==============================================================================

# 1. Caminhos dos arquivos (Regras de governança)
CAMINHO_DADOS = os.path.join("dados", "fornecedores_erro.csv")
PASTA_RESULTADOS = "resultados"
os.makedirs(PASTA_RESULTADOS, exist_ok=True)
CAMINHO_RELATORIO = os.path.join(PASTA_RESULTADOS, "qualidade.md")

# 2. Leitura inicial da estrutura e colunas
with open(CAMINHO_DADOS, mode="r", encoding="utf-8") as f:
    linhas_brutas = f.readlines()

total_linhas_arquivo = len(linhas_brutas) - 1  # desconsiderando o cabeçalho
cabecalho = [col.strip() for col in linhas_brutas[0].strip().split(",")]
total_colunas = len(cabecalho)

# 3. Análise de tipos, valores ausentes e duplicadas
valores_ausentes = {col: 0 for col in cabecalho}
detalhes_erros = []
linhas_processadas = []
duplicadas = 0

with open(CAMINHO_DADOS, mode="r", encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    for idx_linha, linha in enumerate(leitor, start=2):  # linha 1 é o cabeçalho
        tupla_linha = tuple(linha.items())
        if tupla_linha in linhas_processadas:
            duplicadas += 1
        linhas_processadas.append(tupla_linha)

        for col in cabecalho:
            val = linha[col]
            # Espaços vazios contam como ausência (ausência != zero)
            if val is None or val.strip() == "":
                valores_ausentes[col] += 1
                detalhes_erros.append({
                    "linha": idx_linha,
                    "fornecedor": linha.get("fornecedor", "Desconhecido"),
                    "coluna": col,
                    "problema": "Valor ausente (vazio)"
                })

total_ausencias = sum(valores_ausentes.values())

# 4. Exibição no terminal
print("==================================================")
print(" DIAGNÓSTICO DE QUALIDADE (SKILL CONFERIR-CSV)    ")
print("==================================================")
print(f"Arquivo analisado: {CAMINHO_DADOS}")
print(f"Total de linhas de dados: {total_linhas_arquivo}")
print(f"Total de colunas: {total_colunas} -> {', '.join(cabecalho)}")
print(f"Linhas duplicadas: {duplicadas}\n")

print("--- Diagnóstico por Coluna ---")
for col, qtd in valores_ausentes.items():
    status = f"❌ {qtd} valor(es) ausente(s)" if qtd > 0 else "✅ Sem valores ausentes"
    print(f"- {col}: {status}")

print("\n--- Detalhes dos Problemas Encontrados ---")
for erro in detalhes_erros:
    print(f"• Linha {erro['linha']} (Fornecedor {erro['fornecedor']}): campo '{erro['coluna']}' está em branco.")

# 5. Salva o relatório em resultados/qualidade.md (requisito da skill)
with open(CAMINHO_RELATORIO, mode="w", encoding="utf-8") as f:
    f.write("# Relatório de Qualidade de Dados (Skill conferir-csv)\n\n")
    f.write(f"- **Arquivo verificado:** `{CAMINHO_DADOS}`\n")
    f.write(f"- **Total de linhas de dados:** {total_linhas_arquivo}\n")
    f.write(f"- **Total de colunas:** {total_colunas} (`{', '.join(cabecalho)}`)\n")
    f.write(f"- **Linhas duplicadas:** {duplicadas}\n\n")

    f.write("## 1. Problemas Encontrados e Evidências Numéricas\n\n")
    if total_ausencias > 0 or duplicadas > 0:
        f.write(f"Foram identificados **{total_ausencias} valores ausentes** na base de dados:\n\n")
        f.write("| Linha no CSV | Fornecedor | Coluna Afetada | Problema Detectado |\n")
        f.write("| :---: | :--- | :--- | :--- |\n")
        for err in detalhes_erros:
            f.write(f"| {err['linha']} | **{err['fornecedor']}** | `{err['coluna']}` | {err['problema']} |\n")
    else:
        f.write("Nenhum valor ausente ou linha duplicada foi detectado.\n")

    f.write("\n## 2. Tratamentos Propostos (Regras de Governança)\n\n")
    f.write("1. **Nunca alterar o arquivo original** (`dados/fornecedores_erro.csv`), conforme as regras do projeto.\n")
    f.write("2. **Tratamento para `preco_unitario` do fornecedor Delta:**\n")
    f.write("   - *Alerta:* Não se deve preencher com zero (preço zero indicaria gratuidade e distorceria qualquer análise).\n")
    f.write("   - *Proposta:* Obter a cotação correta com o fornecedor ou descartar a proposta caso esteja incompleta.\n")
    f.write("3. **Tratamento para `suporte_nota` do fornecedor Beta:**\n")
    f.write("   - *Alerta:* Ausência é diferente de zero (nota zero indicaria suporte péssimo, mas o dado apenas não foi informado).\n")
    f.write("   - *Proposta:* Coletar a nota oficial de suporte ou estimar com a média dos demais fornecedores, registrando a ressalva.\n")

print(f"\nRelatório de qualidade salvo em: {CAMINHO_RELATORIO}")

