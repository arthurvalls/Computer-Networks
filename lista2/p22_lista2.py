# -*- coding: utf-8 -*-
"""Questão P22 - Lista 2 Redes

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QIHDg_0NFPNvwLih_lMrAlVBzR_ET1tZ

# Arthur Valls da Costa Silva - 120177470
"""

import matplotlib.pyplot as plt

# Função para calcular Dcs (tempo mínimo de distribuição cliente-servidor)
def dist_dcs(N, u):
    return max(N * F / us, F / di)

# Função para calcular DP2P (tempo mínimo de distribuição P2P)
def dist_p2p(N, u):
    return max(F / us, F / di, N * F / (us + N * u)) # como o u_i vai ser o mesmo para cada par basta multiplicarmos u pelo numero de pares (N)

# Dados de entrada
F = 15 * 10**9  # Tamanho do arquivo em bits
us = 30 * 10**6  # Taxa de upload do servidor em bits por segundo
di = 2 * 10**6  # Taxa de download de cada par em bits por segundo
valores_N = [10, 100, 1000]  # Valores de N
valores_U = [300 * 10**3, 700 * 10**3, 2 * 10**6]  # Valores de u em bits por segundo

# Arrays para armazenar os tempos mínimos de distribuição
cliente_servidor_tempos = []
p2p_tempos = []

# Calcula o tempo mínimo de distribuição para cada combinação de N e u
for N in valores_N:
    for u in valores_U:
        # Modo Cliente-Servidor
        cliente_servidor_tempo = dist_dcs(N, u)
        cliente_servidor_tempos.append(cliente_servidor_tempo)

        # Modo Distribuição P2P
        p2p_tempo = dist_p2p(N, u)
        p2p_tempos.append(p2p_tempo)

# Prepara o gráfico
plt.figure(figsize=(10, 6))
plt.plot(range(len(cliente_servidor_tempos)), cliente_servidor_tempos, marker='o', label='Cliente-Servidor')
plt.plot(range(len(p2p_tempos)), p2p_tempos, marker='x', label='P2P')
plt.xticks(range(len(valores_N) * len(valores_U)), [f'N = {N}, u = {u/10**6} Mbps' for N in valores_N for u in valores_U], rotation=45)
plt.xlabel('Combinação de N e u')
plt.ylabel('Tempo Mínimo de Distribuição (s)')
plt.title('Tempo Mínimo de Distribuição para Diferentes Combinações de N e u')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import pandas as pd

# Aqui vamos criar um tabelinha para conseguir visualizar os resultados e
# passá-los para o relatório.

data = {
    'Combinação de N e u': [f'N = {N}, u = {u/10**6} Mbps' for N in valores_N for u in valores_U],
    'Cliente-Servidor (s)': cliente_servidor_tempos,
    'P2P (s)': p2p_tempos
}

df = pd.DataFrame(data)

print(df)