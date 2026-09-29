#!/usr/bin/env python3
"""
CLI Unificada para o projeto JuliaMandelbrotConstruction.
Permite executar todas as modalidades de simulação e geração de imagens
diretamente pela linha de comando, sem necessidade de prompts interativos.
"""

import os
import sys
import math
import random
import argparse
import numpy as np


def parse_complex(valor: str) -> complex:
    """Converte strings no formato complexo aceitando tanto 'j' quanto 'i'."""
    s = valor.strip().replace(" ", "").replace("i", "j").replace("I", "J")
    try:
        return complex(s)
    except ValueError as err:
        raise argparse.ArgumentTypeError(
            f"Valor complexo inválido: '{valor}'. Exemplo: '-0.4+0.6j' ou '0.285-0.01j'"
        ) from err


def salvar_ou_exibir_figura(plt, nome_arquivo: str = None, show: bool = False):
    """Auxiliar unificado para exibição e salvamento seguro de figuras."""
    if nome_arquivo:
        pasta_saida = os.path.dirname(nome_arquivo)
        if pasta_saida:
            os.makedirs(pasta_saida, exist_ok=True)
        plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
        print(f"Figura salva com sucesso em: {nome_arquivo}")

    if show:
        plt.show()
    plt.close()


def cmd_julia(args):
    """Executa o cálculo do conjunto de Julia direto."""
    if not args.show:
        import matplotlib
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    c = args.c
    d = args.degree
    n = args.resolution
    N = args.iterations
    lado = args.side

    print(f"Calculando Conjunto de Julia: d={d}, c={c}, resolução={n}x{n}, iterações={N}...")

    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', "black"]
    matrizes = [[] for _ in range(len(colors))]

    for x in np.linspace(-lado, lado, n):
        for y in np.linspace(-lado, lado, n):
            z = complex(x, y)
            ponto = z
            iteradas = N
            for i in range(N + 1):
                ponto = ponto**d + c
                if abs(ponto) > 5:
                    iteradas = i
                    break

            idx_cor = min(math.floor(iteradas * (len(colors) - 1) / N), len(colors) - 1)
            matrizes[idx_cor].append(z)

    plt.figure(figsize=(8, 8))
    for i, col in enumerate(colors):
        if matrizes[i]:
            pts = matrizes[i]
            plt.plot(np.real(pts), np.imag(pts), 'o', markersize=0.1, color=col)

    plt.title(f"Conjunto de Julia para d = {d} e c = {c}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    salvar_ou_exibir_figura(plt, args.output, args.show)


def cmd_mandelbrot(args):
    """Executa o cálculo do conjunto de Mandelbrot."""
    if not args.show:
        import matplotlib
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = args.degree
    n = args.resolution
    N = args.iterations
    lado = 2 ** (1 / (d - 1)) if d > 1 else 2.0

    print(f"Calculando Conjunto de Mandelbrot: d={d}, resolução={n}x{n}, iterações={N}...")

    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', "black"]
    matrizes = [[] for _ in range(len(colors))]

    for x in np.linspace(-lado, lado, n):
        for y in np.linspace(-lado, lado, n):
            c_val = complex(x, y)
            ponto = 0
            iteradas = N
            for i in range(N):
                ponto = ponto**d + c_val
                if abs(ponto) > 3:
                    iteradas = i
                    break

            idx_cor = min(math.floor(iteradas * (len(colors) - 1) / N), len(colors) - 1)
            matrizes[idx_cor].append(c_val)

    plt.figure(figsize=(8, 8))
    for i, col in enumerate(colors):
        if matrizes[i]:
            pts = matrizes[i]
            plt.plot(np.real(pts), np.imag(pts), 'o', markersize=0.1, color=col)

    plt.title(f"Conjunto de Mandelbrot para d = {d}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    salvar_ou_exibir_figura(plt, args.output, args.show)


def cmd_reverse(args):
    """Executa a iteração reversa estocástica de Julia."""
    if not args.show:
        import matplotlib
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    c = args.c
    n = args.iterations
    d = args.degree

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    print(f"Calculando Julia por Iteração Reversa: c={c}, d={d}, pontos={n}...")

    matriz = np.zeros(n, dtype=np.complex128)
    ponto = complex(0.5, 0.5)

    for i in range(n):
        aleatorio = random.randrange(d)
        ponto = np.power((ponto - c), 1 / d) * np.exp((np.pi * 2 * aleatorio / d) * 1j)
        matriz[i] = ponto

    plt.figure(figsize=(8, 8))
    plt.plot(np.real(matriz), np.imag(matriz), 'o', markersize=0.3, color='blue')
    plt.title(f"Conjunto de Julia Reverso para c = {c}, d = {d}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    salvar_ou_exibir_figura(plt, args.output, args.show)


def cmd_circle(args):
    """Executa o cálculo das pré-imagens reversas do círculo."""
    if not args.show:
        import matplotlib
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = args.degree
    n_rounds = args.rounds
    rang = args.rang

    print(f"Calculando Pré-imagens do Círculo: grau d={d}, rodadas={n_rounds}, rang={rang}...")

    def raiz_d(circulo, d_grau):
        raiz_proxima = []
        for pt in circulo:
            raiz_calculada = np.power(pt - 3, 1 / d_grau)
            for p in range(d_grau):
                raiz_proxima.append(raiz_calculada * np.exp(1j * 2 * math.pi * p / d_grau))
        return raiz_proxima

    # Círculo inicial
    circulo = [
        (math.cos(2 * math.pi * i / rang) + 1j * math.sin(2 * math.pi * i / rang)) * 3
        for i in range(rang)
    ]

    plt.figure(figsize=(8, 8))
    plt.plot(np.real(circulo), np.imag(circulo), 'o', markersize=1, color="black", label="Círculo base")

    raiz = circulo
    for r in range(n_rounds):
        raiz = raiz_d(raiz, d)
        plt.plot(np.real(raiz), np.imag(raiz), 'o', markersize=1, color="black")

    plt.title(f"Pré-imagens do Círculo (d={d}, {n_rounds} iterações)")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    salvar_ou_exibir_figura(plt, args.output, args.show)


def main():
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="CLI do projeto JuliaMandelbrotConstruction para simulação e geração de fractais."
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando a ser executado")

    # Subcomando julia
    p_julia = subparsers.add_parser("julia", help="Conjunto de Julia por tempo de escape direto")
    p_julia.add_argument("-c", type=parse_complex, default="-0.4+0.6j", help="Parâmetro c (padrão: -0.4+0.6j)")
    p_julia.add_argument("-d", "--degree", type=int, default=2, help="Grau do polinômio d (padrão: 2)")
    p_julia.add_argument("-n", "--resolution", type=int, default=600, help="Resolução da grade nxn (padrão: 600)")
    p_julia.add_argument("-N", "--iterations", type=int, default=80, help="Iterações máximas por ponto (padrão: 80)")
    p_julia.add_argument("-s", "--side", type=float, default=2.0, help="Semilado do plano analisado (padrão: 2.0)")
    p_julia.add_argument("-o", "--output", default="images/julia_zd.png", help="Arquivo de saída da imagem")
    p_julia.add_argument("--show", action="store_true", help="Abre a janela interativa do Matplotlib")
    p_julia.set_defaults(func=cmd_julia)

    # Subcomando mandelbrot
    p_mandel = subparsers.add_parser("mandelbrot", help="Conjunto de Mandelbrot / Multibrot")
    p_mandel.add_argument("-d", "--degree", type=int, default=2, help="Grau d do polinômio (padrão: 2)")
    p_mandel.add_argument("-n", "--resolution", type=int, default=600, help="Resolução da grade nxn (padrão: 600)")
    p_mandel.add_argument("-N", "--iterations", type=int, default=80, help="Iterações máximas de escape (padrão: 80)")
    p_mandel.add_argument("-o", "--output", default="images/mandelbrot_zd.png", help="Arquivo de saída da imagem")
    p_mandel.add_argument("--show", action="store_true", help="Abre a janela interativa do Matplotlib")
    p_mandel.set_defaults(func=cmd_mandelbrot)

    # Subcomando reverse
    p_rev = subparsers.add_parser("reverse", help="Conjunto de Julia por iteração reversa estocástica")
    p_rev.add_argument("-c", type=parse_complex, default="-1+0j", help="Parâmetro c (padrão: -1+0j)")
    p_rev.add_argument("-d", "--degree", type=int, default=2, help="Grau d da raiz (padrão: 2)")
    p_rev.add_argument("-n", "--iterations", type=int, default=100000, help="Número de iterações/pontos (padrão: 100000)")
    p_rev.add_argument("--seed", type=int, default=None, help="Semente pseudoaleatória para reprodutibilidade")
    p_rev.add_argument("-o", "--output", default="images/juliaReverseCompleto.png", help="Arquivo de saída da imagem")
    p_rev.add_argument("--show", action="store_true", help="Abre a janela interativa do Matplotlib")
    p_rev.set_defaults(func=cmd_reverse)

    # Subcomando circle
    p_circ = subparsers.add_parser("circle", help="Pré-imagens reversas sucessivas de um círculo")
    p_circ.add_argument("-d", "--degree", type=int, default=2, help="Grau d da raiz (padrão: 2)")
    p_circ.add_argument("-n", "--rounds", type=int, default=2, help="Número de rodadas de pré-imagens (padrão: 2)")
    p_circ.add_argument("--rang", type=int, default=10000, help="Número de pontos no círculo base (padrão: 10000)")
    p_circ.add_argument("-o", "--output", default="images/iteracoesReversasCirculo.png", help="Arquivo de saída")
    p_circ.add_argument("--show", action="store_true", help="Abre a janela interativa do Matplotlib")
    p_circ.set_defaults(func=cmd_circle)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
