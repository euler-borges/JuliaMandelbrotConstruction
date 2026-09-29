#!/usr/bin/env python3
"""
Script legado: iteracoesReversasCirculo.py
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

from juliamandelbrot.core.dynamics import (
    construir_circulo,
    raiz_d_circulo,
    calcular_pre_imagens_circulo,
)
from juliamandelbrot.rendering.plotter import (
    renderizar_pre_imagens_circulo,
    exibir_ou_salvar,
)

RANG = 10000


def constroiCirculo(rang):
    """Função legada para compatibilidade de API."""
    return construir_circulo(rang=rang)


def raiz_d(circulo, d):
    """Função legada para compatibilidade de API."""
    return raiz_d_circulo(circulo, d)


def executar_simulacao_circulo(d, n, rang=10000, nome_arquivo="images/iteracoesReversasCirculo.png", show=None):
    """Função legada para compatibilidade de API."""
    circulo_base = construir_circulo(rang=rang)
    pre_imagens = calcular_pre_imagens_circulo(circulo_base=circulo_base, d=d, n_rounds=n)
    show_flag = False if show is False else (True if show is True else None)
    renderizar_pre_imagens_circulo(
        circulo_base=circulo_base,
        pre_imagens_por_rodada=pre_imagens,
        d=d,
        nome_arquivo=nome_arquivo,
        show=show_flag if show_flag is not None else False,
    )


def plotaRaizes(circulo):
    """Função legada interativa para compatibilidade de API."""
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
