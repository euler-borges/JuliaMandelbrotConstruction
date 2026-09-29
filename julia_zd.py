#!/usr/bin/env python3
"""
Script legado: julia_zd.py
Refatorado na Fase 2 para integrar com a arquitetura modular juliamandelbrot,
preservando 100% de compatibilidade com chamadas de função e uso via CLI/interativo.
"""

import os
import sys
import argparse
from pathlib import Path

src_path = str(Path(__file__).resolve().parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from juliamandelbrot.core.julia import calcular_orbita_julia, calcular_grid_julia
from juliamandelbrot.rendering.plotter import renderizar_julia_grade, exibir_ou_salvar
from juliamandelbrot.utils.parser import parse_complex

lado = 2.0


def orbita(z, c, d, n_max):
    """Função legada para compatibilidade de API."""
    return calcular_orbita_julia(z, c, d, n_max)


def visualizar_conjunto_julia(c, n, d, N, nome_arquivo="images/julia_zd.png", show=None):
    """Função legada para compatibilidade de API."""
    matrizes = calcular_grid_julia(c=c, d=d, n=n, n_max=N, side=lado)
    show_flag = False if show is False else (True if show is True else None)
    renderizar_julia_grade(
        matrizes_por_faixa=matrizes,
        c=c,
        d=d,
        nome_arquivo=nome_arquivo,
        show=show_flag if show_flag is not None else False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conjunto de Julia por tempo de escape direto.")
    parser.add_argument("-d", "--degree", type=int, help="Grau d do polinômio")
    parser.add_argument("-c", "--c", type=parse_complex, help="Parâmetro complexo c (ex: -0.4+0.6j)")
    parser.add_argument("-n", "--resolution", type=int, help="Resolução da grade nxn")
    parser.add_argument("-N", "--iterations", type=int, help="Número de iterações máximas")
    parser.add_argument("-o", "--output", default="images/julia_zd.png", help="Arquivo de saída (padrão: images/julia_zd.png)")
    parser.add_argument("--no-show", action="store_true", help="Não abre a janela gráfica do Matplotlib")
    parser.add_argument("--show", action="store_true", help="Força a exibição da janela gráfica")

    if len(sys.argv) > 1:
        args = parser.parse_args()
        d_val = args.degree if args.degree is not None else 2
        c_val = args.c if args.c is not None else -0.4 + 0.6j
        n_val = args.resolution if args.resolution is not None else 600
        N_val = args.iterations if args.iterations is not None else 80
        show_flag = False if args.no_show else (True if args.show else None)
        visualizar_conjunto_julia(c_val, n_val, d_val, N_val, nome_arquivo=args.output, show=show_flag)
    else:
        print("Forneca números para os questionamentos a seguir (ou use flags CLI via --help):")
        d_val = int(input("Qual o 'd' do conjunto que deseja plotar? "))
        c_val = parse_complex(input("Qual o 'c' do conjunto que deseja plotar? "))
        n_val = int(input("Quer dividir os eixos em quantas partes?(recomenda-se um número alto)  "))
        N_val = int(input("Quantas iteradas deseja fazer para cada ponto?(números altos implicam em maior precisão, entretanto podem sobrecarregar seu computador, recomenda-se algo entre 50 e 100) "))
        visualizar_conjunto_julia(c_val, n_val, d_val, N_val)
