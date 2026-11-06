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
print("Quantidade de candidatos por ano:")
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


# GRÁFICOS 4: Comparação entre escolas públicas e privadas

import math

areas = redes["Área"].unique()

# Define a quantidade de linhas e colunas
colunas = 2
linhas = math.ceil(len(areas) / colunas)

# Cria uma única janela com os gráficos organizados em grade
fig, axes = plt.subplots(
    nrows=linhas,
    ncols=colunas,
    figsize=(16, 5 * linhas)
)

# Transforma os eixos em uma lista para facilitar o acesso
axes = axes.flatten()

for i, area in enumerate(areas):
    dados_area = redes[redes["Área"] == area]
    ax = axes[i]

    for rede in ["Pública", "Privada"]:
        dados_rede = dados_area[dados_area["Grupo"] == rede]

        ax.plot(
            dados_rede["Ano"],
            dados_rede["Média"],
            marker="o",
            label="Escola " + rede
        )

    ax.set_title("Desempenho - " + area)
    ax.set_xlabel("Ano")
    ax.set_xticks(dados_area["Ano"].unique())
    ax.set_ylabel("Nota média")
    ax.legend()
    ax.grid()

    # Salva cada gráfico individualmente
    nome_arquivo = area.lower().replace(" ", "_").replace("/", "_")
    nome_arquivo = nome_arquivo.replace("(", "").replace(")", "").replace(",", "")

    fig_individual, ax_individual = plt.subplots(figsize=(10, 6))

    for rede in ["Pública", "Privada"]:
        dados_rede = dados_area[dados_area["Grupo"] == rede]
        ax_individual.plot(
            dados_rede["Ano"],
            dados_rede["Média"],
            marker="o",
            label="Escola " + rede
        )

    ax_individual.set_title("Desempenho das escolas públicas e privadas - " + area)
    ax_individual.set_xlabel("Ano")
    ax_individual.set_xticks(dados_area["Ano"].unique())
    ax_individual.set_ylabel("Nota média")
    ax_individual.legend()
    ax_individual.grid()

    fig_individual.tight_layout()
    fig_individual.savefig("graficos/comparacao_publica_privada_" + nome_arquivo + ".png")
    plt.close(fig_individual)

# Remove espaços vazios caso a quantidade de gráficos seja ímpar
for j in range(len(areas), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.subplots_adjust(
    wspace=0.35,  
    hspace=0.5  
)
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


# GRÁFICO 5: Nota média por faixa de renda familiar
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


# GRÁFICO 6: Nota média por cor/raça nas escolas públicas e privadas
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


# GRÁFICO 7: ANÁLISE POR REGIÃO DO BRASIL

# Leitura dos dados por estado (UF onde o candidato fez a prova)
estados = pd.read_excel("analise_enem_2010_2025.xlsx", sheet_name="por_estado_prova")
estados = estados.sort_values("Ano")

# A redação não entra porque a escala de nota é diferente
estados = estados[estados["Área"] != "Redação (apenas válidas)"]

# Agrupamento dos estados em regiões
regioes_uf = {
    "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte",
    "RO": "Norte", "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste",
    "PB": "Nordeste", "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste", "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste", "MS": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul"
}
estados["Região"] = estados["Grupo"].map(regioes_uf)

# A média da região é uma média ponderada pelo nº de candidatos de cada estado.
# Assim, estados maiores (ex.: SP) pesam mais que estados menores (ex.: AC).
estados["Soma das notas"] = estados["Média"] * estados["Nº de candidatos"]

regiao = (
    estados.groupby(["Ano", "Área", "Região"])
    .agg(soma=("Soma das notas", "sum"), candidatos=("Nº de candidatos", "sum"))
    .reset_index()
)
regiao["Média"] = regiao["soma"] / regiao["candidatos"]

ordem_regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

# Média geral por região (média entre as 4 áreas, como nos gráficos anteriores)
media_regiao = regiao.groupby(["Ano", "Região"])["Média"].mean().unstack("Região")[ordem_regioes]

# Mostra no terminal a média de cada região no último ano disponível
ultimo_ano = media_regiao.index.max()
print("\nNota média por região em", ultimo_ano, ":")
print(media_regiao.loc[ultimo_ano].sort_values(ascending=False).round(1))


# GRÁFICO 8: Evolução por região em cada área (4 painéis)
areas = regiao["Área"].unique()
fig, eixos = plt.subplots(2, 2, figsize=(14, 9), sharex=True)

for eixo, area in zip(eixos.flatten(), areas):
    dados_area = regiao[regiao["Área"] == area]
    for nome in ordem_regioes:
        d = dados_area[dados_area["Região"] == nome]
        eixo.plot(d["Ano"], d["Média"], marker="o", markersize=3, label=nome)
    eixo.set_title(area)
    eixo.set_ylabel("Nota média")
    eixo.grid()

eixos[0][0].legend()
fig.supxlabel("Ano")
fig.suptitle("Nota média por região em cada área do ENEM")
plt.tight_layout()
plt.savefig("graficos/media_por_regiao_por_area.png")
plt.show()


# GRÁFICO 9: Nota média por região em cada área no último ano do enem (barras agrupadas)
ultimo = (
    regiao[regiao["Ano"] == ultimo_ano]
    .pivot(index="Área", columns="Região", values="Média")[ordem_regioes]
)

ax = ultimo.plot(kind="bar", figsize=(11, 6), rot=0)
plt.title("Nota média por região e área - " + str(ultimo_ano))
plt.xlabel("Área")
plt.ylabel("Nota média")
plt.legend(title="Região")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("graficos/regiao_por_area_ultimo_ano.png")
plt.show()


# GRÁFICO 10: Diferença para a melhor região em cada ano
# Mostra o quanto cada região está abaixo da região de maior nota naquele ano.
distancia = media_regiao.sub(media_regiao.max(axis=1), axis=0)

plt.figure(figsize=(10, 6))

for nome in ordem_regioes:
    plt.plot(distancia.index, distancia[nome], marker="o", label=nome)

plt.title("Distância da nota média de cada região para a região de maior nota")
plt.xlabel("Ano")
plt.xticks(distancia.index)
plt.ylabel("Diferença em pontos")
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig("graficos/distancia_melhor_regiao.png")
plt.show()
