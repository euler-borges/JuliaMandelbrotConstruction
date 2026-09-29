#!/usr/bin/env python3
"""
Script legado: juliaReverseCompleto.py
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

from juliamandelbrot.core.dynamics import calcular_julia_reverso
from juliamandelbrot.rendering.plotter import renderizar_julia_reverso, exibir_ou_salvar
from juliamandelbrot.utils.parser import parse_complex


def visualizar_conjunto_julia(c, n, d, nome_arquivo="images/juliaReverseCompleto.png", show=None, seed=None):
    """Função legada para compatibilidade de API."""
    pontos = calcular_julia_reverso(c=c, d=d, n=n, seed=seed)
    show_flag = False if show is False else (True if show is True else None)
    renderizar_julia_reverso(
        pontos=pontos,
        c=c,
        d=d,
        nome_arquivo=nome_arquivo,
        show=show_flag if show_flag is not None else False,
    )


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
