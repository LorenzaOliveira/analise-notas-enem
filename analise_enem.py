import pandas as pd
import matplotlib.pyplot as plt
import os

# Leitura das planilhas
nacional = pd.read_excel("nacional.xlsx")
redes = pd.read_excel("por_rede_so_com_escola.xlsx")

# Organização dos dados por ano
nacional = nacional.sort_values("Ano")
redes = redes.sort_values("Ano")

# Cria a pasta onde os gráficos serão salvos
os.makedirs("graficos", exist_ok=True)

# Mostra no terminal somente a quantidade de candidatos por ano.
# É utilizado o maior número de candidatos entre as áreas daquele ano.
candidatos = nacional.groupby("Ano")["Nº de candidatos"].max()

for ano, quantidade in candidatos.items():
    print(ano, "-", quantidade)


# GRÁFICO 1: Evolução da média nacional por área
plt.figure(figsize=(10, 6))

for area in nacional["Área"].unique():
    dados = nacional[nacional["Área"] == area]
    plt.plot(dados["Ano"], dados["Média"], marker="o", label=area)

plt.title("Evolução da média nacional do ENEM")
plt.xlabel("Ano")
plt.xticks(nacional["Ano"].unique())
plt.ylabel("Nota média")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("graficos/media_nacional.png")
plt.show()


# GRÁFICO 2: Evolução da nota mínima nacional por área
plt.figure(figsize=(10, 6))

for area in nacional["Área"].unique():
    dados = nacional[nacional["Área"] == area]
    plt.plot(dados["Ano"], dados["Nota mínima"], marker="o", label=area)

plt.title("Evolução da nota mínima nacional do ENEM")
plt.xlabel("Ano")
plt.xticks(nacional["Ano"].unique())
plt.ylabel("Nota mínima")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("graficos/nota_minima_nacional.png")
plt.show()


# GRÁFICO 3: Evolução da nota máxima nacional por área
plt.figure(figsize=(10, 6))

for area in nacional["Área"].unique():
    dados = nacional[nacional["Área"] == area]
    plt.plot(dados["Ano"], dados["Nota máxima"], marker="o", label=area)

plt.title("Evolução da nota máxima nacional do ENEM")
plt.xlabel("Ano")
plt.xticks(nacional["Ano"].unique())
plt.ylabel("Nota máxima")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("graficos/nota_maxima_nacional.png")
plt.show()


# GRÁFICOS 4 em diante: Comparação entre escolas públicas e privadas
# É criado um gráfico para cada área, para facilitar a leitura.
for area in redes["Área"].unique():
    dados_area = redes[redes["Área"] == area]

    plt.figure(figsize=(10, 6))

    for rede in ["Pública", "Privada"]:
        dados_rede = dados_area[dados_area["Grupo"] == rede]
        plt.plot(
            dados_rede["Ano"],
            dados_rede["Média"],
            marker="o",
            label="Escola " + rede
        )

    plt.title("Desempenho das escolas públicas e privadas - " + area)
    plt.xlabel("Ano")
    plt.xticks(dados_area["Ano"].unique())
    plt.ylabel("Nota média")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    nome_arquivo = area.lower().replace(" ", "_").replace("/", "_")
    nome_arquivo = nome_arquivo.replace("(", "").replace(")", "").replace(",", "")
    plt.savefig("graficos/comparacao_publica_privada_" + nome_arquivo + ".png")
    plt.show()
