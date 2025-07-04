import matplotlib.pyplot as plt
import pandas as pd
import sys

def ler_dados(arquivo_dados):
    """Lê os dados (label + D1 + D2) em um DataFrame"""
    return pd.read_csv(arquivo_dados, sep='\t')

def ler_particao(arquivo_particao):
    """Lê o arquivo de partição e retorna um dicionário: {label: cluster_id}"""
    particao = {}
    with open(arquivo_particao, 'r') as f:
        for linha in f:
            partes = linha.strip().split('\t')
            particao[partes[0]] = int(partes[1])
    return particao

def plotar_clusters(dados_df, particao):
    """Plota os dados coloridos por cluster"""
    dados_df['Cluster'] = dados_df['sample_label'].map(particao)

    plt.figure(figsize=(10, 6))
    
    # Plota cada cluster com uma cor
    for cluster_id, grupo in dados_df.groupby('Cluster'):
        plt.scatter(grupo['D1'], grupo['D2'], label=f'Cluster {cluster_id}', s=50)

    plt.title('Visualização dos Clusters')
    plt.xlabel('D1')
    plt.ylabel('D2')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# ======== Execução Principal ========
if __name__ == '__main__':
    caminho_dados = sys.argv[1]
    caminho_particao = sys.argv[2] 

    dados_df = ler_dados(caminho_dados)
    particao = ler_particao(caminho_particao)
    plotar_clusters(dados_df, particao)
