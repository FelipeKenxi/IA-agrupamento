import random
import math
import sys

class Ponto:
    def __init__(self, partes):
        self.label = partes[0]
        self.dados = [float(x) for x in partes[1:]]
        self.cluster = None

    def distancia_para(self, outro):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.dados, outro.dados)))

def ler_dados(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()[1:]  # Ignora o cabeçalho

    pontos = [Ponto(linha.strip().split('\t')) for linha in linhas]
    return pontos

def media_grupo(grupo):
    if not grupo:
        return None
    dim = len(grupo[0].dados)
    soma = [0.0] * dim
    for ponto in grupo:
        for i in range(dim):
            soma[i] += ponto.dados[i]
    return [x / len(grupo) for x in soma]

def kmeans(pontos, k=2, max_iter=100):
    centróides = random.sample([p.dados for p in pontos], k)

    for _ in range(max_iter):
        grupos = [[] for _ in range(k)]

        # Atribui cada ponto ao cluster mais próximo
        for ponto in pontos:
            distancias = [math.sqrt(sum((a - b) ** 2 for a, b in zip(ponto.dados, c))) for c in centróides]
            cluster_mais_proximo = distancias.index(min(distancias))
            ponto.cluster = cluster_mais_proximo
            grupos[cluster_mais_proximo].append(ponto)

        # Recalcula centróides
        novos_centróides = []
        for grupo in grupos:
            if grupo:
                novos_centróides.append(media_grupo(grupo))
            else:
                novos_centróides.append(random.choice(pontos).dados)

        # Verifica convergência
        convergiu = all(
            math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2))) < 1e-6
            for c1, c2 in zip(centróides, novos_centróides)
        )
        if convergiu:
            break

        centróides = novos_centróides

    return pontos, centróides

# ========== Ponto de entrada ==========
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Uso: python kmeans.py <arquivo_dados> <numero_clusters> <maximo_iteracoes> <arquivo_saida>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    try:
        k = int(sys.argv[2])
        iMax = int(sys.argv[3])
    except ValueError:
        print("Erro: o número de clusters e iterações devem ser inteiros.")
        sys.exit(1)

    pontos = ler_dados(nome_arquivo)
    pontos_clusterizados, centróides = kmeans(pontos, k, iMax)


    arquivo_saida = f'kmeans/{sys.argv[4]}.clu'
    with open(arquivo_saida, 'w') as f:
        for ponto in pontos_clusterizados:
            f.write(f'{ponto.label}\t{ponto.cluster + 1}\n')