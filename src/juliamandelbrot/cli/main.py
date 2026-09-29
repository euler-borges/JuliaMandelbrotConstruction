"""
Controlador de Linha de Comando (CLI) do pacote juliamandelbrot.
Orquestra o núcleo matemático (core) e a camada visual (rendering).
"""

import sys
import argparse
from juliamandelbrot.utils.parser import parse_complex
from juliamandelbrot.core import (
    calcular_grid_julia,
    calcular_grid_mandelbrot,
    calcular_julia_reverso,
    construir_circulo,
    calcular_pre_imagens_circulo,
)
from juliamandelbrot.rendering import (
    renderizar_julia_grade,
    renderizar_mandelbrot_grade,
    renderizar_julia_reverso,
    renderizar_pre_imagens_circulo,
)


def exec_julia(args: argparse.Namespace) -> int:
    print(
        f"Calculando Conjunto de Julia: d={args.degree}, c={args.c}, "
        f"resolução={args.resolution}x{args.resolution}, iterações={args.iterations}..."
    )
    matrizes = calcular_grid_julia(
        c=args.c,
        d=args.degree,
        n=args.resolution,
        n_max=args.iterations,
        side=args.side,
    )
    renderizar_julia_grade(
        matrizes_por_faixa=matrizes,
        c=args.c,
        d=args.degree,
        nome_arquivo=args.output,
        show=args.show,
    )
    return 0


def exec_mandelbrot(args: argparse.Namespace) -> int:
    print(
        f"Calculando Conjunto de Mandelbrot: d={args.degree}, "
        f"resolução={args.resolution}x{args.resolution}, iterações={args.iterations}..."
    )
    _, matrizes = calcular_grid_mandelbrot(
        d=args.degree,
        n=args.resolution,
        n_max=args.iterations,
    )
    renderizar_mandelbrot_grade(
        matrizes_por_faixa=matrizes,
        d=args.degree,
        nome_arquivo=args.output,
        show=args.show,
    )
    return 0


def exec_reverse(args: argparse.Namespace) -> int:
    print(
        f"Calculando Julia Reverso: c={args.c}, d={args.degree}, pontos={args.iterations}..."
    )
    pontos = calcular_julia_reverso(
        c=args.c,
        d=args.degree,
        n=args.iterations,
        seed=args.seed,
    )
    renderizar_julia_reverso(
        pontos=pontos,
        c=args.c,
        d=args.degree,
        nome_arquivo=args.output,
        show=args.show,
    )
    return 0


def exec_circle(args: argparse.Namespace) -> int:
    print(
        f"Calculando Pré-imagens do Círculo: grau d={args.degree}, "
        f"rodadas={args.rounds}, rang={args.rang}..."
    )
    circulo_base = construir_circulo(rang=args.rang)
    pre_imagens = calcular_pre_imagens_circulo(
        circulo_base=circulo_base,
        d=args.degree,
        n_rounds=args.rounds,
    )
    renderizar_pre_imagens_circulo(
        circulo_base=circulo_base,
        pre_imagens_por_rodada=pre_imagens,
        d=args.degree,
        nome_arquivo=args.output,
        show=args.show,
    )
    return 0


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="juliamandelbrot",
        description="Ferramenta CLI para simulação e renderização de fractais (família z^d + c).",
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando a ser executado")

    # Subcomando julia
    p_julia = subparsers.add_parser("julia", help="Conjunto de Julia por tempo de escape direto")
    p_julia.add_argument("-c", type=parse_complex, default="-0.4+0.6j", help="Parâmetro c (padrão: -0.4+0.6j)")
    p_julia.add_argument("-d", "--degree", type=int, default=2, help="Grau do polinômio d (padrão: 2)")
    p_julia.add_argument("-n", "--resolution", type=int, default=600, help="Resolução da grade nxn (padrão: 600)")
    p_julia.add_argument("-N", "--iterations", type=int, default=80, help="Iterações máximas por ponto (padrão: 80)")
    p_julia.add_argument("-s", "--side", type=float, default=2.0, help="Semilado do plano analisado (padrão: 2.0)")
    p_julia.add_argument("-o", "--output", default="images/julia_zd.png", help="Arquivo de saída (padrão: images/julia_zd.png)")
    p_julia.add_argument("--show", action="store_true", help="Abre a janela gráfica interativa do Matplotlib")
    p_julia.set_defaults(func=exec_julia)

    # Subcomando mandelbrot
    p_mandel = subparsers.add_parser("mandelbrot", help="Conjunto de Mandelbrot / Multibrot")
    p_mandel.add_argument("-d", "--degree", type=int, default=2, help="Grau d do polinômio (padrão: 2)")
    p_mandel.add_argument("-n", "--resolution", type=int, default=600, help="Resolução da grade nxn (padrão: 600)")
    p_mandel.add_argument("-N", "--iterations", type=int, default=80, help="Iterações máximas de escape (padrão: 80)")
    p_mandel.add_argument("-o", "--output", default="images/mandelbrot_zd.png", help="Arquivo de saída (padrão: images/mandelbrot_zd.png)")
    p_mandel.add_argument("--show", action="store_true", help="Abre a janela gráfica interativa do Matplotlib")
    p_mandel.set_defaults(func=exec_mandelbrot)

    # Subcomando reverse
    p_rev = subparsers.add_parser("reverse", help="Conjunto de Julia por iteração reversa estocástica")
    p_rev.add_argument("-c", type=parse_complex, default="-1+0j", help="Parâmetro c (padrão: -1+0j)")
    p_rev.add_argument("-d", "--degree", type=int, default=2, help="Grau d da raiz (padrão: 2)")
    p_rev.add_argument("-n", "--iterations", type=int, default=100000, help="Número de iterações/pontos (padrão: 100000)")
    p_rev.add_argument("--seed", type=int, default=None, help="Semente pseudoaleatória para reprodutibilidade")
    p_rev.add_argument("-o", "--output", default="images/juliaReverseCompleto.png", help="Arquivo de saída")
    p_rev.add_argument("--show", action="store_true", help="Abre a janela gráfica interativa do Matplotlib")
    p_rev.set_defaults(func=exec_reverse)

    # Subcomando circle
    p_circ = subparsers.add_parser("circle", help="Pré-imagens reversas sucessivas de um círculo")
    p_circ.add_argument("-d", "--degree", type=int, default=2, help="Grau d da raiz (padrão: 2)")
    p_circ.add_argument("-n", "--rounds", type=int, default=2, help="Número de rodadas de pré-imagens (padrão: 2)")
    p_circ.add_argument("--rang", type=int, default=10000, help="Número de pontos no círculo base (padrão: 10000)")
    p_circ.add_argument("-o", "--output", default="images/iteracoesReversasCirculo.png", help="Arquivo de saída")
    p_circ.add_argument("--show", action="store_true", help="Abre a janela gráfica interativa do Matplotlib")
    p_circ.set_defaults(func=exec_circle)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = criar_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
