#!/usr/bin/env python3
"""
Script legado: mandelbrot_zd.py
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

from juliamandelbrot.core.mandelbrot import calcular_orbita_mandelbrot, calcular_grid_mandelbrot
from juliamandelbrot.rendering.plotter import renderizar_mandelbrot_grade, exibir_ou_salvar


def orbitaM_zd(c, d, n_max):
    """Função legada para compatibilidade de API."""
    return calcular_orbita_mandelbrot(c, d, n_max)


def visualizar_conjunto_mandel_zd(n, d, N, nome_arquivo="images/mandelbrot_zd.png", show=None):
    """Função legada para compatibilidade de API."""
    lado, matrizes = calcular_grid_mandelbrot(d=d, n=n, n_max=N)
    show_flag = False if show is False else (True if show is True else None)
    renderizar_mandelbrot_grade(
        matrizes_por_faixa=matrizes,
        d=d,
        nome_arquivo=nome_arquivo,
        show=show_flag if show_flag is not None else False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conjunto de Mandelbrot / Multibrot.")
    parser.add_argument("-d", "--degree", type=int, help="Grau d do polinômio")
    parser.add_argument("-n", "--resolution", type=int, help="Resolução da grade nxn")
    parser.add_argument("-N", "--iterations", type=int, help="Número de iterações máximas")
    parser.add_argument("-o", "--output", default="images/mandelbrot_zd.png", help="Arquivo de saída (padrão: images/mandelbrot_zd.png)")
    parser.add_argument("--no-show", action="store_true", help="Não abre a janela gráfica do Matplotlib")
    parser.add_argument("--show", action="store_true", help="Força a exibição da janela gráfica")

    if len(sys.argv) > 1:
        args = parser.parse_args()
        d_val = args.degree if args.degree is not None else 2
        n_val = args.resolution if args.resolution is not None else 600
        N_val = args.iterations if args.iterations is not None else 80
        show_flag = False if args.no_show else (True if args.show else None)
        visualizar_conjunto_mandel_zd(n_val, d_val, N_val, nome_arquivo=args.output, show=show_flag)
    else:
        print("Forneca números inteiros para os questionamentos a seguir (ou use flags CLI via --help):")
        n_val = int(input("Quer dividir os eixos em quantas partes?(recomenda-se um número alto)  "))
        d_val = int(input("Qual o conjunto que deseja plotar?(especifique o d)  "))
        N_val = int(input("Quantas iteradas deseja fazer para cada c?(números altos implicam em maior precisão, entretanto podem sobrecarregar seu computador, recomenda-se algo entre 50 e 100) "))
        visualizar_conjunto_mandel_zd(n_val, d_val, N_val)