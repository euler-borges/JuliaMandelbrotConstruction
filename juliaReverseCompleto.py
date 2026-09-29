import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import random as rd


def parse_complex(valor: str) -> complex:
    s = valor.strip().replace(" ", "").replace("i", "j").replace("I", "J")
    try:
        return complex(s)
    except ValueError as err:
        raise argparse.ArgumentTypeError(f"Número complexo inválido: '{valor}'") from err


def exibir_ou_salvar(nome_arquivo="images/juliaReverseCompleto.png", show=None):
    backend = plt.get_backend().lower()
    pasta_saida = os.path.dirname(nome_arquivo)
    if pasta_saida:
        os.makedirs(pasta_saida, exist_ok=True)
    plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
    print(f"Figura salva em {nome_arquivo}.")
    if show is True or (show is None and "agg" not in backend):
        plt.show()
    plt.close()


def visualizar_conjunto_julia(c, n, d, nome_arquivo="images/juliaReverseCompleto.png", show=None, seed=None):
    if seed is not None:
        rd.seed(seed)
        np.random.seed(seed)

    matriz = np.zeros(n, dtype=np.complex128)
    ponto = complex(0.5, 0.5)

    for i in range(n):
        aleatorio = rd.randrange(d)
        ponto = np.power((ponto - c), 1/d)*np.exp((np.pi*2*aleatorio/d)*1j)
        matriz[i] = ponto

    plt.plot(np.real(matriz), np.imag(matriz), 'o', markersize=0.3, color='blue')
    plt.title(f"Conjunto de Julia para c = {c}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    exibir_ou_salvar(nome_arquivo=nome_arquivo, show=show)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conjunto de Julia por iteração reversa estocástica.")
    parser.add_argument("-c", "--c", type=parse_complex, help="Parâmetro complexo c (ex: -1+0j)")
    parser.add_argument("-n", "--iterations", type=int, help="Número de iterações/pontos")
    parser.add_argument("-d", "--degree", type=int, help="Grau d da raiz")
    parser.add_argument("--seed", type=int, default=None, help="Semente para reprodutibilidade")
    parser.add_argument("-o", "--output", default="images/juliaReverseCompleto.png", help="Arquivo de saída")
    parser.add_argument("--no-show", action="store_true", help="Não abre a janela gráfica do Matplotlib")
    parser.add_argument("--show", action="store_true", help="Força a exibição da janela gráfica")

    if len(sys.argv) > 1:
        args = parser.parse_args()
        c_val = args.c if args.c is not None else -1+0j
        n_val = args.iterations if args.iterations is not None else 100000
        d_val = args.degree if args.degree is not None else 2
        show_flag = False if args.no_show else (True if args.show else None)
        visualizar_conjunto_julia(c_val, n_val, d_val, nome_arquivo=args.output, show=show_flag, seed=args.seed)
    else:
        print("Forneca números para os questionamentos a seguir (ou use flags CLI via --help):")
        c_val = parse_complex(input("Qual o 'c' do conjunto que deseja plotar? "))
        n_val = int(input("Quantas iterações deseja realizar? "))
        d_val = int(input("Qual o 'd' desejado? "))
        visualizar_conjunto_julia(c_val, n_val, d_val)

