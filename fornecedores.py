import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# SKILLS: DECISION-MATRIX + CHART-IMAGE (PUBLICATION QUALITY)
# ==============================================================================

# 1. Caminhos dos arquivos (Regras de governança do projeto)
CAMINHO_DADOS = os.path.join("dados", "fornecedores.csv")
PASTA_RESULTADOS = "resultados"
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

CAMINHO_RELATORIO = os.path.join(PASTA_RESULTADOS, "relatorio_fornecedores.md")
CAMINHO_GRAFICO_PRINCIPAL = os.path.join(PASTA_RESULTADOS, "grafico_fornecedores.png")
CAMINHO_GRAFICO_RADAR = os.path.join(PASTA_RESULTADOS, "grafico_radar_fornecedores.png")
CAMINHO_GRAFICO_TRADEOFF = os.path.join(PASTA_RESULTADOS, "grafico_tradeoff_fornecedores.png")
CAMINHO_GRAFICO_COMPOSICAO = os.path.join(PASTA_RESULTADOS, "grafico_composicao_notas.png")

# 2. Definição dos pesos dos critérios
PESOS = {
    "preco": 0.30,
    "qualidade": 0.30,
    "prazo": 0.25,
    "suporte": 0.15
}

# 3. Leitura e estruturação dos dados brutos
fornecedores_brutos = []
with open(CAMINHO_DADOS, mode="r", encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        fornecedores_brutos.append({
            "fornecedor": linha["fornecedor"],
            "preco_unitario": float(linha["preco_unitario"]),
            "prazo_dias": float(linha["prazo_dias"]),
            "defeitos_pct": float(linha["defeitos_pct"]),
            "suporte_nota": float(linha["suporte_nota"])
        })

# 4. Melhores valores para normalização (escala 1 a 10)
melhor_preco = min(item["preco_unitario"] for item in fornecedores_brutos)
melhor_prazo = min(item["prazo_dias"] for item in fornecedores_brutos)
melhor_defeito = min(item["defeitos_pct"] for item in fornecedores_brutos)
melhor_suporte = max(item["suporte_nota"] for item in fornecedores_brutos)

# 5. Cálculo das notas normalizadas e ponderadas
matriz_decisao = []
for item in fornecedores_brutos:
    nota_preco = 10.0 * (melhor_preco / item["preco_unitario"])
    nota_prazo = 10.0 * (melhor_prazo / item["prazo_dias"])
    nota_qualidade = 10.0 * (melhor_defeito / item["defeitos_pct"])
    nota_suporte = 10.0 * (item["suporte_nota"] / melhor_suporte)

    pontuacao_final = (
        nota_preco * PESOS["preco"] +
        nota_qualidade * PESOS["qualidade"] +
        nota_prazo * PESOS["prazo"] +
        nota_suporte * PESOS["suporte"]
    )

    matriz_decisao.append({
        "fornecedor": item["fornecedor"],
        "dados_brutos": item,
        "nota_preco": nota_preco,
        "nota_prazo": nota_prazo,
        "nota_qualidade": nota_qualidade,
        "nota_suporte": nota_suporte,
        "pontuacao_final": pontuacao_final,
        # Contribuições ponderadas para o gráfico empilhado
        "contrib_preco": nota_preco * PESOS["preco"],
        "contrib_qualidade": nota_qualidade * PESOS["qualidade"],
        "contrib_prazo": nota_prazo * PESOS["prazo"],
        "contrib_suporte": nota_suporte * PESOS["suporte"]
    })

# Ordenação decrescente por pontuação
matriz_decisao.sort(key=lambda x: x["pontuacao_final"], reverse=True)
vencedor = matriz_decisao[0]

# Cores consistentes para publicação
CORES_FORNECEDORES = {
    "Delta": "#2ca02c",  # Verde destaque (vencedor)
    "Beta": "#1f77b4",   # Azul
    "Alfa": "#ff7f0e",   # Laranja
    "Gama": "#9467bd"    # Roxo
}

# 6. Geração do Relatório Markdown
with open(CAMINHO_RELATORIO, mode="w", encoding="utf-8") as f:
    f.write("# Relatório de Avaliação de Fornecedores\n\n")
    f.write("Relatório estruturado com base nas skills **decision-matrix** e **chart-image**.\n\n")
    f.write("## 1. Recomendação Final\n\n")
    f.write(f"- **Vencedor:** **{vencedor['fornecedor']}**\n")
    f.write(f"- **Pontuação Ponderada:** **{vencedor['pontuacao_final']:.2f} / 10.0**\n")
    f.write(f"- **Destaques:** Menor índice de defeitos ({vencedor['dados_brutos']['defeitos_pct']}%), entrega mais rápida ({vencedor['dados_brutos']['prazo_dias']:.0f} dias) e nota máxima de suporte.\n\n")

    f.write("## 2. Matriz de Decisão (Notas Normalizadas de 1 a 10)\n\n")
    f.write("| Posição | Fornecedor | Preço (30%) | Qualidade (30%) | Prazo (25%) | Suporte (15%) | Pontuação Final |\n")
    f.write("| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n")
    for pos, item in enumerate(matriz_decisao, start=1):
        tag = " *(Vencedor)*" if pos == 1 else ""
        f.write(f"| {pos}º | **{item['fornecedor']}**{tag} | {item['nota_preco']:.2f} | {item['nota_qualidade']:.2f} | {item['nota_prazo']:.2f} | {item['nota_suporte']:.2f} | **{item['pontuacao_final']:.2f}** |\n")

# ==============================================================================
# 7. GRÁFICOS (APLICAÇÃO DAS DIRETRIZES DA SKILL CHART-IMAGE)
# Diretrizes: Rótulos legíveis, unidades explícitas, grid suave, contraste alto.
# ==============================================================================

# ------------------------------------------------------------------------------
# GRÁFICO 1: GRÁFICO PRINCIPAL APRIMORADO (Ranking + Comparativo por Critério)
# ------------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

nomes = [item["fornecedor"] for item in matriz_decisao]
pontuacoes = [item["pontuacao_final"] for item in matriz_decisao]
cores_barras = [CORES_FORNECEDORES[nome] for nome in nomes]

# Painel 1: Ranking
barras = ax1.bar(nomes, pontuacoes, color=cores_barras, width=0.55, edgecolor='#333333', linewidth=1)
ax1.set_ylim(0, 10.5)
ax1.set_title("Ranking Geral Ponderado", fontsize=13, fontweight='bold', pad=12)
ax1.set_ylabel("Pontuação Ponderada (Escala 0 a 10)", fontsize=11)
ax1.set_xlabel("Fornecedores Avaliados", fontsize=11)
ax1.grid(axis='y', linestyle='--', alpha=0.5)

for barra in barras:
    yval = barra.get_height()
    ax1.annotate(f"{yval:.2f}",
                 xy=(barra.get_x() + barra.get_width() / 2, yval),
                 xytext=(0, 5), textcoords="offset points",
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

# Painel 2: Desempenho por Critério
criterios = ['Preço (30%)', 'Qualidade (30%)', 'Prazo (25%)', 'Suporte (15%)']
x_indices = np.arange(len(criterios))
largura = 0.18

for idx, item in enumerate(matriz_decisao):
    valores = [item["nota_preco"], item["nota_qualidade"], item["nota_prazo"], item["nota_suporte"]]
    offset = (idx - 1.5) * largura
    ax2.bar(x_indices + offset, valores, largura, label=item["fornecedor"],
            color=CORES_FORNECEDORES[item["fornecedor"]], edgecolor='#333333', linewidth=0.8)

ax2.set_xticks(x_indices)
ax2.set_xticklabels(criterios, fontsize=10, fontweight='bold')
ax2.set_ylim(0, 11)
ax2.set_title("Notas Normalizadas por Critério (1 a 10)", fontsize=13, fontweight='bold', pad=12)
ax2.set_ylabel("Nota Normalizada", fontsize=11)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.legend(title="Fornecedor", loc='upper right', frameon=True)

plt.suptitle("Avaliação Estruturada de Fornecedores (Decision Matrix)", fontsize=15, fontweight='bold', y=0.98)
fig.text(0.99, 0.01, "Fonte: dados/fornecedores.csv | Skill: chart-image", ha='right', fontsize=9, color='#666666')
plt.tight_layout()
plt.savefig(CAMINHO_GRAFICO_PRINCIPAL, dpi=160)
plt.close()

# ------------------------------------------------------------------------------
# GRÁFICO 2: RADAR CHART (VISÃO 360° DOS FORNECEDORES)
# ------------------------------------------------------------------------------
categorias_radar = ['Preço', 'Qualidade\n(Defeitos)', 'Prazo de\nEntrega', 'Suporte\nTécnico']
num_vars = len(categorias_radar)
angulos = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angulos += angulos[:1]

fig, ax = plt.subplots(figsize=(7.5, 7.5), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angulos[:-1]), categorias_radar, fontsize=11, fontweight='bold')
ax.set_ylim(0, 10)
ax.grid(True, linestyle=':', alpha=0.6)

for item in matriz_decisao:
    vals = [item["nota_preco"], item["nota_qualidade"], item["nota_prazo"], item["nota_suporte"]]
    vals += vals[:1]
    cor = CORES_FORNECEDORES[item["fornecedor"]]
    lw = 2.5 if item["fornecedor"] == vencedor["fornecedor"] else 1.5
    ax.plot(angulos, vals, color=cor, linewidth=lw, label=f"{item['fornecedor']} ({item['pontuacao_final']:.2f})")
    ax.fill(angulos, vals, color=cor, alpha=0.12)

ax.set_title("Perfil Competitivo 360° dos Fornecedores\n(Escala 1 a 10 - Quanto mais externo, melhor)",
             fontsize=13, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), title="Fornecedores")
fig.text(0.95, 0.02, "Fonte: dados/fornecedores.csv | Skill: chart-image", ha='right', fontsize=9, color='#666666')
plt.tight_layout()
plt.savefig(CAMINHO_GRAFICO_RADAR, dpi=160)
plt.close()

# ------------------------------------------------------------------------------
# GRÁFICO 3: TRADE-OFF DE NEGÓCIO (PREÇO vs QUALIDADE vs PRAZO)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))

for item in matriz_decisao:
    dados = item["dados_brutos"]
    nome = item["fornecedor"]
    cor = CORES_FORNECEDORES[nome]
    # O tamanho do ponto reflete a agilidade (menor prazo = maior diâmetro visual)
    tamanho = (15 - dados["prazo_dias"]) * 45
    ax.scatter(dados["preco_unitario"], dados["defeitos_pct"],
               s=tamanho, color=cor, alpha=0.85, edgecolors='black', linewidth=1.2, label=nome)

    offset_y = 0.15 if nome != "Beta" else -0.2
    ax.annotate(f"{nome}\nR$ {dados['preco_unitario']:.0f} | {dados['defeitos_pct']}% def.\nPrazo: {dados['prazo_dias']:.0f} dias",
                xy=(dados["preco_unitario"], dados["defeitos_pct"]),
                xytext=(0, 15 if offset_y > 0 else -30), textcoords="offset points",
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=cor, lw=1.2, alpha=0.9))

ax.set_title("Análise de Trade-off: Preço vs Taxa de Defeitos", fontsize=14, fontweight='bold', pad=12)
ax.set_xlabel("Preço Unitário (R$) - [Menor é melhor]", fontsize=11)
ax.set_ylabel("Taxa de Defeitos (%) - [Menor é melhor]", fontsize=11)
ax.set_xlim(80, 120)
ax.set_ylim(-0.2, 5.0)
ax.grid(True, linestyle='--', alpha=0.5)

# Linhas indicativas de região ideal (baixo custo e baixo defeito)
ax.axvspan(80, 95, 0, 0.4, color='green', alpha=0.08, label="Zona Ideal (Custo & Defeito Baixos)")
ax.legend(loc='upper left', frameon=True)
fig.text(0.99, 0.01, "Nota: O tamanho da bolha indica agilidade no prazo | Fonte: dados/fornecedores.csv",
         ha='right', fontsize=9, color='#666666')
plt.tight_layout()
plt.savefig(CAMINHO_GRAFICO_TRADEOFF, dpi=160)
plt.close()

# ------------------------------------------------------------------------------
# GRÁFICO 4: COMPOSIÇÃO DA NOTA PONDERADA (BARRAS EMPILHADAS)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

f_nomes = [item["fornecedor"] for item in matriz_decisao]
c_preco = [item["contrib_preco"] for item in matriz_decisao]
c_qualidade = [item["contrib_qualidade"] for item in matriz_decisao]
c_prazo = [item["contrib_prazo"] for item in matriz_decisao]
c_suporte = [item["contrib_suporte"] for item in matriz_decisao]

p1 = ax.bar(f_nomes, c_qualidade, label='Qualidade (30%)', color='#2ca02c', width=0.5, edgecolor='#333333')
p2 = ax.bar(f_nomes, c_preco, bottom=c_qualidade, label='Preço (30%)', color='#1f77b4', width=0.5, edgecolor='#333333')

bottom_prazo = np.array(c_qualidade) + np.array(c_preco)
p3 = ax.bar(f_nomes, c_prazo, bottom=bottom_prazo, label='Prazo (25%)', color='#ff7f0e', width=0.5, edgecolor='#333333')

bottom_suporte = bottom_prazo + np.array(c_prazo)
p4 = ax.bar(f_nomes, c_suporte, bottom=bottom_suporte, label='Suporte (15%)', color='#9467bd', width=0.5, edgecolor='#333333')

ax.set_ylim(0, 11)
ax.set_ylabel("Pontuação Acumulada (Máximo 10)", fontsize=11)
ax.set_title("Decomposição da Nota Final: Contribuição de Cada Critério", fontsize=14, fontweight='bold', pad=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.legend(loc='upper right', frameon=True)

# Anotação da nota total no topo das barras
for idx, item in enumerate(matriz_decisao):
    total = item["pontuacao_final"]
    ax.annotate(f"Total: {total:.2f}",
                xy=(idx, total),
                xytext=(0, 6), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold')

fig.text(0.99, 0.01, "Fonte: dados/fornecedores.csv | Skill: chart-image", ha='right', fontsize=9, color='#666666')
plt.tight_layout()
plt.savefig(CAMINHO_GRAFICO_COMPOSICAO, dpi=160)
plt.close()

# Mensagens de conclusão
print("==================================================")
print(" SUCESSO: RELATÓRIO E 4 GRÁFICOS GERADOS!        ")
print("==================================================")
print(f"1. Gráfico Principal (Aprimorado): {CAMINHO_GRAFICO_PRINCIPAL}")
print(f"2. Gráfico Radar (Perfil 360°):    {CAMINHO_GRAFICO_RADAR}")
print(f"3. Gráfico Trade-off (Dispersão):  {CAMINHO_GRAFICO_TRADEOFF}")
print(f"4. Gráfico Composição Empilhada:   {CAMINHO_GRAFICO_COMPOSICAO}")
print(f"5. Relatório Atualizado:           {CAMINHO_RELATORIO}")
