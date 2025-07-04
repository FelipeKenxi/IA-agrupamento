from sklearn.metrics import adjusted_rand_score
import sys


def ler_particao(arquivo):
    """
    Lê um arquivo de partição no formato: <rótulo>\t<cluster>
    Retorna um dicionário: {rótulo: cluster}
    """
    particao = {}
    with open(arquivo, 'r') as f:
        for linha in f:
            partes = linha.strip().split('\t')
            if len(partes) == 2:
                rotulo, cluster = partes
                particao[rotulo] = int(cluster)
    return particao

def calcular_ari(arquivo_real, arquivo_predito):
    real = ler_particao(arquivo_real)
    predito = ler_particao(arquivo_predito)

    # Interseção dos rótulos presentes em ambas as partições
    rotulos_comuns = sorted(set(real.keys()) & set(predito.keys()))

    y_true = [real[r] for r in rotulos_comuns]
    y_pred = [predito[r] for r in rotulos_comuns]

    ari = adjusted_rand_score(y_true, y_pred)
    return ari

# ======= Exemplo de uso ========
if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Uso: python ARI.PY <particao_real> <particao_criada>")
        sys.exit(1)
    real = sys.argv[1]
    predito = sys.argv[2]

    ari = calcular_ari(real, predito)
    print(f'Adjusted Rand Index (ARI): {ari:.4f}')
