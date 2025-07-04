import math
import sys
import os

def ler_dados(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()[1:]  # Ignora o cabeçalho

    rotulos = []
    dados = []
    for linha in linhas:
        partes = linha.strip().split('\t')
        rotulos.append(partes[0])
        dados.append([float(x) for x in partes[1:]])
    return rotulos, dados

def distancia(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def escrever_particao(rotulos, ponto_para_cluster, num_clusters, nome):
    os.makedirs("completelinks", exist_ok=True)
    nome_arquivo = f'completelinks/complete_{nome}_{num_clusters}.clu'
    with open(nome_arquivo, 'w') as f:
        for idx, rotulo in enumerate(rotulos):
            cluster_id = ponto_para_cluster[idx]
            f.write(f'{rotulo}\t{cluster_id + 1}\n')  # +1 para clusters começarem em 1

def complete_link_matriz(dados, rotulos, kMin, kMax, nome_data):
    N = len(dados)
    
    # Inicializa clusters: {id: [índices dos pontos]}
    clusters = {i: [i] for i in range(N)}

    # Matriz de distância entre pontos
    dist_pontos = {}
    for i in range(N):
        for j in range(i + 1, N):
            dist_pontos[(i, j)] = distancia(dados[i], dados[j])

    # Matriz de distâncias entre clusters (chave ordenada)
    dist_clusters = {}
    for i in clusters:
        for j in clusters:
            if i < j:
                max_d = max(
                    dist_pontos.get((min(a, b), max(a, b)), 0)
                    for a in clusters[i]
                    for b in clusters[j]
                )
                dist_clusters[(i, j)] = max_d

    while len(clusters) > kMin:
        # Encontra o par de clusters com menor distância completa
        (c1, c2), _ = min(dist_clusters.items(), key=lambda x: x[1])
        a, b = min(c1, c2), max(c1, c2)  # Mantemos o menor índice

        # Funde b em a
        clusters[a].extend(clusters[b])
        del clusters[b]

        # Remove distâncias envolvendo b
        dist_clusters = {
            (i, j): d for (i, j), d in dist_clusters.items()
            if b not in (i, j)
        }

        # Atualiza distâncias de a com os demais clusters
        for cid in clusters:
            if cid == a:
                continue
            max_d = max(
                dist_pontos.get((min(i, j), max(i, j)), 0)
                for i in clusters[a]
                for j in clusters[cid]
            )
            i, j = sorted([a, cid])
            dist_clusters[(i, j)] = max_d

        # Salva partição se estiver no intervalo desejado
        if kMin <= len(clusters) <= kMax:
            ponto_para_cluster = {}
            for cluster_id, pontos in clusters.items():
                for ponto in pontos:
                    ponto_para_cluster[ponto] = cluster_id

            # Normaliza IDs para salvar em arquivo (0, 1, 2, ...)
            id_map = {old_id: new_id for new_id, old_id in enumerate(sorted(clusters))}
            ponto_para_cluster_normalizado = {
                ponto: id_map[cluster_id] for ponto, cluster_id in ponto_para_cluster.items()
            }

            escrever_particao(rotulos, ponto_para_cluster_normalizado, len(clusters), nome_data)

    return ponto_para_cluster_normalizado

# ==== Main ====

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Uso: python completelink.py <arquivo_dados> <iMin> <iMax> <nome_data>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    iMin = int(sys.argv[2])
    iMax = int(sys.argv[3])

    rotulos, dados = ler_dados(nome_arquivo)
    clusters = complete_link_matriz(dados, rotulos, iMin, iMax, sys.argv[4])
