import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import math

RANG = 10000


def exibir_ou_salvar(nome_arquivo="images/iteracoesReversasCirculo.png", show=None):
    backend = plt.get_backend().lower()
    pasta_saida = os.path.dirname(nome_arquivo)
    if pasta_saida:
        os.makedirs(pasta_saida, exist_ok=True)
    plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
    print(f"Figura salva em {nome_arquivo}.")
    if show is True or (show is None and "agg" not in backend):
        plt.show()
    plt.close()


def raiz_d(circulo, d):
    raiz_proxima = []
    for i in range(len(circulo)):
        p = 0
        raiz_calculada = np.power(circulo[i]-3, 1/d) 
        while p < d:
            raiz_proxima.append(raiz_calculada*np.exp(1j*2*math.pi*p/d))
            p += 1
    return raiz_proxima


def constroiCirculo(RANG):
    circulo = []
    for i in range(RANG):
        circulo.append((math.cos(2*math.pi*i/RANG)+ 1j*math.sin(2*math.pi*i/RANG))*3)
    return circulo


def executar_simulacao_circulo(d, n, rang=10000, nome_arquivo="images/iteracoesReversasCirculo.png", show=None):
    circulo = constroiCirculo(rang)

    plt.figure(figsize=(8, 8))
    plt.title("Raiz do círculo")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    plt.plot(np.real(circulo), np.imag(circulo), 'o', markersize=1, color="black")

    if n > 0:
        raiz = raiz_d(circulo, d)
        plt.plot(np.real(raiz), np.imag(raiz), 'o', markersize=1, color="black")
        for _ in range(n - 1):
            raiz = raiz_d(raiz, d)
            plt.plot(np.real(raiz), np.imag(raiz), 'o', markersize=1, color="black")

    exibir_ou_salvar(nome_arquivo=nome_arquivo, show=show)


def plotaRaizes(circulo):
    d = int(input("Raiz de que grau? "))
    n = int(input("Quantas iteradas? "))
    executar_simulacao_circulo(d, n, rang=len(circulo))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pré-imagens reversas sucessivas de um círculo.")
    parser.add_argument("-d", "--degree", type=int, help="Grau d da raiz")
    parser.add_argument("-n", "--rounds", type=int, help="Número de rodadas de pré-imagens")
    parser.add_argument("--rang", type=int, default=10000, help="Número de pontos no círculo base (padrão: 10000)")
    parser.add_argument("-o", "--output", default="images/iteracoesReversasCirculo.png", help="Arquivo de saída")
    parser.add_argument("--no-show", action="store_true", help="Não abre a janela gráfica do Matplotlib")
    parser.add_argument("--show", action="store_true", help="Força a exibição da janela gráfica")

    if len(sys.argv) > 1:
        args = parser.parse_args()
        d_val = args.degree if args.degree is not None else 2
        n_val = args.rounds if args.rounds is not None else 2
        show_flag = False if args.no_show else (True if args.show else None)
        executar_simulacao_circulo(d_val, n_val, rang=args.rang, nome_arquivo=args.output, show=show_flag)
    else:
        print("Forneca números para os questionamentos a seguir (ou use flags CLI via --help):")
        circulo_base = constroiCirculo(RANG)
        plotaRaizes(circulo_base)
