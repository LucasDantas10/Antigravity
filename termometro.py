import os
import matplotlib.pyplot as plt

# 1. Definição dos pontos conhecidos (calibração do sensor):
# x: Temperatura em graus Celsius (°C)
# y: Corrente elétrica em miliamperes (mA)
# Ponto 1: (0 °C, 4 mA)
# Ponto 2: (100 °C, 20 mA)
x1, y1 = 0, 4
x2, y2 = 100, 20

# 2. Cálculo dos coeficientes da reta y = ax + b:
# 'a' é a inclinação (variação de corrente por grau de temperatura)
a = (y2 - y1) / (x2 - x1)

# 'b' é o valor da corrente quando x = 0 °C
b = y1 - a * x1

print(f"Coeficiente a: {a}")
print(f"Coeficiente b: {b}")
print(f"Equação da reta: y = {a} * x + {b}\n")


# 3. Funções de classificação e verificação de limites:
def classificar_temperatura(temp):
    """Classifica a temperatura em baixa, média ou alta."""
    if temp <= 30:
        return "Baixa (até 30 °C)"
    elif temp <= 60:
        return "Média (até 60 °C)"
    else:
        return "Alta (acima de 60 °C)"


def verificar_limites(temp, corr):
    """Emite avisos se a corrente ou a temperatura estiverem fora das faixas nominais."""
    avisos = []
    if corr < 4 or corr > 20:
        avisos.append(f"[AVISO] Corrente fora da faixa permitida de 4 a 20 mA (Atual: {corr:.2f} mA)")
    if temp < 0 or temp > 100:
        avisos.append(f"[AVISO] Temperatura fora da faixa permitida de 0 a 100 °C (Atual: {temp:.2f} °C)")
    return avisos


# 4. Cálculo e exibição para x = 50 °C (ponto solicitado):
x_teste = 50
y_teste = a * x_teste + b
classe_teste = classificar_temperatura(x_teste)
avisos_teste = verificar_limites(x_teste, y_teste)

print(f"--- Resultado para x = {x_teste} °C ---")
print(f"Corrente elétrica (y): {y_teste:.2f} mA")
print(f"Classificação da temperatura: {classe_teste}")
if avisos_teste:
    for aviso in avisos_teste:
        print(aviso)
else:
    print("Status: Operação normal (temperatura e corrente dentro das faixas).")
print()

# 5. Teste demonstrativo com valor fora da faixa (exemplo: x = 110 °C):
x_fora = 110
y_fora = a * x_fora + b
print(f"--- Exemplo com valor fora da faixa: x = {x_fora} °C ---")
print(f"Corrente elétrica calculada: {y_fora:.2f} mA")
print(f"Classificação: {classificar_temperatura(x_fora)}")
for aviso in verificar_limites(x_fora, y_fora):
    print(aviso)
print()


# 6. Geração do gráfico com Matplotlib:
# Garante a existência da pasta resultados/
os.makedirs("resultados", exist_ok=True)

# Gera pontos para a reta de 0 °C a 100 °C
temperaturas = [0, 20, 40, 60, 80, 100]
correntes = [a * t + b for t in temperaturas]

plt.figure(figsize=(8, 5))
plt.plot(temperaturas, correntes, marker='o', color='blue', label='Linha de calibração (y = ax + b)')
plt.plot(x_teste, y_teste, marker='*', markersize=14, color='red', label=f'Ponto teste (50 °C, {y_teste:.1f} mA)')

# Linhas pontilhadas indicando as regiões de classificação
plt.axvline(x=30, color='gray', linestyle='--', alpha=0.6, label='Limite Baixa/Média (30 °C)')
plt.axvline(x=60, color='orange', linestyle='--', alpha=0.6, label='Limite Média/Alta (60 °C)')

plt.title("Termômetro: Corrente Elétrica vs Temperatura")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

# Salva o gráfico gerado na pasta resultados/
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico)
plt.close()

print(f"Gráfico salvo com sucesso em: {caminho_grafico}")

