import math
import sys
import heapq
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

def escrever_particao(rotulos, ponto_para_cluster, num_clusters, nome):
    os.makedirs("completelinks", exist_ok=True)
    nome_arquivo = f'completelinks/complete_{nome}_{num_clusters}.clu'
    with open(nome_arquivo, 'w') as f:
        for idx, rotulo in enumerate(rotulos):
            cluster_id = ponto_para_cluster[idx]
            f.write(f'{rotulo}\t{cluster_id + 1}\n')  # +1 para começar do 1

def complete_link_heap(dados, rotulos, kMin, kMax, nome_data):
    N = len(dados)
    heap, matriz_dist = construir_heap_distancias(dados)
    clusters = {i: [i] for i in range(N)}



    while len(clusters) > kMin:
        #debug
        #print(len(clusters))
        # Remove pares inválidos do heap
        while True:
            dist, a, b = heapq.heappop(heap)
            if a in clusters and b in clusters:
                break

        clusters[a].extend(clusters[b])
        del clusters[b]

        # Atualiza distâncias
        for cid in clusters:
            if cid == a:
                continue
            max_d = -float('inf')
            for i in clusters[a]:
                for j in clusters[cid]:
                    i_, j_ = min(i, j), max(i, j)
                    d = matriz_dist.get((i_, j_), float('inf'))
                    if d > max_d:
                        max_d = d
            heapq.heappush(heap, (max_d, a, cid))


        # Salva partição se dentro do intervalo
        if kMin <= len(clusters) <= kMax:
            ponto_para_cluster = {}
            for cluster_id, pontos in clusters.items():
                for ponto in pontos:
                    ponto_para_cluster[ponto] = cluster_id

            # Normaliza IDs para salvar
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
    clusters = complete_link_heap(dados, rotulos, iMin, iMax, sys.argv[4])
