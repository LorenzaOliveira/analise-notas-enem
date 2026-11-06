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

# Leitura da planilha com os dados socioeconômicos
renda = pd.read_excel("analise_enem_2010_2025.xlsx", sheet_name="por_renda")
raca = pd.read_excel("analise_enem_2010_2025.xlsx", sheet_name="cruzamentos")

renda = renda.sort_values("Ano")
raca = raca.sort_values("Ano")

# A redação não entra porque a escala de nota é diferente
renda = renda[renda["Área"] != "Redação (apenas válidas)"]
raca = raca[raca["Área"] != "Redação (apenas válidas)"]
raca = raca[raca["Dimensão"] == "Cor/raça"]


# GRÁFICO 9: Nota média por faixa de renda familiar
plt.figure(figsize=(10, 6))

faixas = ["Nenhuma renda", "Até 1 SM", "De 1 a 3 SM", "De 3 a 6 SM", "De 6 a 9 SM", "De 9 a 12 SM", "De 12 a 15 SM", "Mais de 15 SM"]

for faixa in faixas:
    dados = renda[renda["Grupo"] == faixa]
    media = dados.groupby("Ano")["Média"].mean()
    plt.plot(media.index, media.values, marker="o", label=faixa)

plt.title("Nota média do ENEM por faixa de renda familiar")
plt.xlabel("Ano")
plt.xticks(renda["Ano"].unique())
plt.ylabel("Nota média")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("graficos/renda_familiar.png")
plt.show()


# GRÁFICO 10: Nota média por cor/raça nas escolas públicas e privadas
plt.figure(figsize=(10, 6))

for rede in ["Pública", "Privada"]:
    dados_rede = raca[raca["Rede"] == rede]

    for cor in ["Branca", "Parda", "Preta"]:
        dados = dados_rede[dados_rede["Sexo ou Cor/raça"] == cor]
        media = dados.groupby("Ano")["Média"].mean()
        plt.plot(media.index, media.values, marker="o", label=cor + " - Escola " + rede)

plt.title("Nota média por cor/raça nas escolas públicas e privadas")
plt.xlabel("Ano")
plt.xticks(raca["Ano"].unique())
plt.ylabel("Nota média")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("graficos/cor_raca_por_rede.png")
plt.show()
