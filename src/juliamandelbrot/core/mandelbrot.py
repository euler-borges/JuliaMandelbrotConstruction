"""
Módulo de cálculo matemático para conjuntos de Mandelbrot / Multibrot.
Contém apenas lógica matemática pura sem dependência de bibliotecas de plotagem.
"""

import math
import numpy as np


def calcular_orbita_mandelbrot(
    c: complex, d: int, n_max: int, escape_radius: float = 3.0
) -> tuple[complex, int]:
    """
    Calcula a órbita do ponto crítico z_0 = 0 sob P_{d,c}(z) = z^d + c.

    Args:
        c: Ponto analisado no plano dos parâmetros.
        d: Grau do polinômio.
        n_max: Número máximo de iterações.
        escape_radius: Critério de escape (raio limite).

    Returns:
        Tupla (c, iteradas) onde iteradas é o número de iterações até escapar ou n_max.
    """
    ponto = 0j
    for i in range(n_max):
        ponto = ponto**d + c
        if abs(ponto) > escape_radius:
            return (c, i)
    return (c, n_max)


def calcular_grid_mandelbrot(
    d: int,
    n: int,
    n_max: int,
    side: float | None = None,
    num_faixas: int = 8,
    escape_radius: float = 3.0,
) -> tuple[float, dict[int, list[complex]]]:
    """
    Calcula a grade do conjunto de Mandelbrot para a família z^d + c.

    Args:
        d: Grau da família z^d + c.
        n: Resolução por eixo (n x n pontos).
        n_max: Máximo de iterações por ponto c.
        side: Semilado do plano. Se None, é calculado teoricamente como 2^(1/(d-1)).
        num_faixas: Quantidade de faixas para agrupamento.
        escape_radius: Critério de escape.

    Returns:
        Tupla (lado, matrizes_por_faixa) contendo o semilado efetivo utilizado
        e o dicionário de pontos agrupados por faixa de iterações.
    """
    if side is not None:
        lado = side
    else:
        lado = 2.0 ** (1.0 / (d - 1.0)) if d > 1 else 2.0

    matrizes = {i: [] for i in range(num_faixas)}

    for x in np.linspace(-lado, lado, n):
        for y in np.linspace(-lado, lado, n):
            c_val = complex(x, y)
            _, iteradas = calcular_orbita_mandelbrot(c_val, d, n_max, escape_radius=escape_radius)
            idx_faixa = min(math.floor(iteradas * (num_faixas - 1) / n_max), num_faixas - 1)
            matrizes[idx_faixa].append(c_val)

    return lado, matrizes
