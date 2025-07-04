import math
import sys

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


import math
import heapq

# Distância Euclidiana
def distancia(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def construir_heap_distancias(dados):
    N = len(dados)
    heap = []
    matriz_dist = {}

    for i in range(N):
        for j in range(i + 1, N):
            d = distancia(dados[i], dados[j])
            matriz_dist[(i, j)] = d
            heapq.heappush(heap, (d, i, j))

    return heap, matriz_dist


def escrever_particao(rotulos, parte, ponto_para_cluster, num_clusters):
    nome_arquivo = f'singlelinks\singlelink_{parte}_{num_clusters}.clu'
    with open(nome_arquivo, 'w') as f:
        for idx, rotulo in enumerate(rotulos):
            cluster_id = ponto_para_cluster[idx]
            f.write(f'{rotulo}\t{cluster_id + 1}\n')  # +1 para clusters começarem em 1

def singlelink_heap(dados, kMin, kMax, nome_data):
    N = len(dados)
    heap, matriz_dist = construir_heap_distancias(dados)
    clusters = {i: [i] for i in range(N)}
    cluster_ids = list(range(N))

    while len(clusters) > kMin:
        print(len(clusters))

        while True:
            dist, a, b = heapq.heappop(heap)
            if a in clusters and b in clusters:
                break

        # funde os clusters de a e b
        clusters[a].extend(clusters[b])
        del clusters[b]

        # atualiza heap com novas distâncias para o cluster fundido
        for cid in clusters:
            if cid != a:
                # menor distância entre qualquer ponto de clusters[a] e clusters[cid]
                min_d = float('inf')
                for i in clusters[a]:
                    for j in clusters[cid]:
                        i_, j_ = min(i, j), max(i, j)
                        d = matriz_dist.get((i_, j_), float('inf'))
                        if d < min_d:
                            min_d = d
                heapq.heappush(heap, (min_d, a, cid))

 # Se o número de clusters atual estiver no intervalo desejado, escreve a partição
        if kMin <= len(clusters) <= kMax:
            ponto_para_cluster = {}
            for cluster_id, pontos in clusters.items():
                for ponto in pontos:
                    ponto_para_cluster[ponto] = cluster_id

            # Remapeia os IDs dos clusters para 0,1,2,...
            id_map = {old_id: new_id for new_id, old_id in enumerate(sorted(clusters))}
            ponto_para_cluster_normalizado = {
                ponto: id_map[cluster_id] for ponto, cluster_id in ponto_para_cluster.items()
            }

            escrever_particao(rotulos, nome_data, ponto_para_cluster_normalizado, len(clusters))

    return ponto_para_cluster_normalizado


if __name__ == '__main__':

    if len(sys.argv) != 5:
        print("Uso: python singlelink.py <arquivo_dados> <iMin> <iMax> <nome_data>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]


    iMin = int(sys.argv[2])
    iMax = int(sys.argv[3])
    rotulos, dados = ler_dados(nome_arquivo)
    clusters = singlelink_heap(dados, iMin, iMax, sys.argv[4])


