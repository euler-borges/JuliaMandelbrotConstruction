"""
Módulo de renderização visual e manipulação de figuras com Matplotlib.
Isola todas as chamadas e dependências de plotagem do núcleo matemático.
"""

import os
import numpy as np
from juliamandelbrot.rendering.colormaps import PALETA_PADRAO_8_CORES


def configurar_backend(show: bool = False):
    """Garante o uso de backend headless (Agg) quando a exibição interativa não for solicitada."""
    import matplotlib
    if not show and "agg" not in matplotlib.get_backend().lower():
        matplotlib.use("Agg")


def exibir_ou_salvar(
    nome_arquivo: str | None = None,
    show: bool = False,
    dpi: int = 300,
):
    """
    Salva e/ou exibe a figura ativa do Matplotlib, fechando-a em seguida
    para liberar memória de forma limpa.
    """
    import matplotlib.pyplot as plt

    if nome_arquivo:
        pasta_saida = os.path.dirname(nome_arquivo)
        if pasta_saida:
            os.makedirs(pasta_saida, exist_ok=True)
        plt.savefig(nome_arquivo, dpi=dpi, bbox_inches="tight")
        print(f"Figura salva em {nome_arquivo}.")

    if show:
        plt.show()

    plt.close()


def renderizar_julia_grade(
    matrizes_por_faixa: dict[int, list[complex]],
    c: complex,
    d: int,
    nome_arquivo: str = "images/julia_zd.png",
    show: bool = False,
    colors: list[str] | None = None,
):
    """Plota os pontos do conjunto de Julia agrupados por faixas de iteração."""
    configurar_backend(show)
    import matplotlib.pyplot as plt

    if colors is None:
        colors = PALETA_PADRAO_8_CORES

    plt.figure(figsize=(8, 8))
    for i, col in enumerate(colors):
        pts = matrizes_por_faixa.get(i, [])
        if pts:
            plt.plot(np.real(pts), np.imag(pts), 'o', markersize=0.1, color=col)

    plt.title(f"Conjunto de Julia para d = {d} e c = {c}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    exibir_ou_salvar(nome_arquivo=nome_arquivo, show=show)


def renderizar_mandelbrot_grade(
    matrizes_por_faixa: dict[int, list[complex]],
    d: int,
    nome_arquivo: str = "images/mandelbrot_zd.png",
    show: bool = False,
    colors: list[str] | None = None,
):
    """Plota os pontos do conjunto de Mandelbrot agrupados por faixas de iteração."""
    configurar_backend(show)
    import matplotlib.pyplot as plt

    if colors is None:
        colors = PALETA_PADRAO_8_CORES

    plt.figure(figsize=(8, 8))
    for i, col in enumerate(colors):
        pts = matrizes_por_faixa.get(i, [])
        if pts:
            plt.plot(np.real(pts), np.imag(pts), 'o', markersize=0.1, color=col)

    plt.title(f"Conjunto de Mandelbrot para d = {d}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    exibir_ou_salvar(nome_arquivo=nome_arquivo, show=show)


def renderizar_julia_reverso(
    pontos: np.ndarray,
    c: complex,
    d: int,
    nome_arquivo: str = "images/juliaReverseCompleto.png",
    show: bool = False,
    cor: str = "blue",
    markersize: float = 0.3,
):
    """Plota a nuvem de pontos gerada por iteração reversa aleatória."""
    configurar_backend(show)
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 8))
    plt.plot(np.real(pontos), np.imag(pontos), 'o', markersize=markersize, color=cor)
    plt.title(f"Conjunto de Julia para c = {c} (d = {d})")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    exibir_ou_salvar(nome_arquivo=nome_arquivo, show=show)


def renderizar_pre_imagens_circulo(
    circulo_base: list[complex],
    pre_imagens_por_rodada: list[list[complex]],
    d: int,
    nome_arquivo: str = "images/iteracoesReversasCirculo.png",
    show: bool = False,
):
    """Plota a circunferência base e suas pré-imagens sucessivas."""
    configurar_backend(show)
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 8))
    plt.title(f"Raiz do círculo (d = {d})")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    plt.plot(np.real(circulo_base), np.imag(circulo_base), 'o', markersize=1, color="black")

    for rodada in pre_imagens_por_rodada:
        plt.plot(np.real(rodada), np.imag(rodada), 'o', markersize=1, color="black")

    exibir_ou_salvar(nome_arquivo=nome_arquivo, show=show)
