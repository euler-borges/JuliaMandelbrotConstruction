"""
Módulo de cálculo matemático para conjuntos de Julia diretos (órbita para frente).
Contém apenas lógica matemática pura sem dependência de bibliotecas de plotagem.
"""

import math
import numpy as np


def calcular_orbita_julia(
    z: complex, c: complex, d: int, n_max: int, escape_radius: float = 5.0
) -> tuple[complex, int]:
    """
    Calcula o tempo de escape da órbita de z sob a iteração P_{d,c}(z) = z^d + c.

    Args:
        z: Ponto inicial no plano complexo.
        c: Parâmetro complexo do polinômio.
        d: Grau do polinômio (d >= 1).
        n_max: Número máximo de iterações.
        escape_radius: Raio a partir do qual a órbita é considerada divergente.

    Returns:
        Tupla (z, iteradas) onde iteradas é o número de passos até escapar ou n_max.
    """
    ponto = z
    for i in range(n_max + 1):
        ponto = ponto**d + c
        if abs(ponto) > escape_radius:
            return (z, i)
    return (z, n_max)


def calcular_grid_julia(
    c: complex,
    d: int,
    n: int,
    n_max: int,
    side: float = 2.0,
    num_faixas: int = 8,
    escape_radius: float = 5.0,
) -> dict[int, list[complex]]:
    """
    Gera uma grade [-side, side] x [-side, side] com n x n pontos
    e classifica cada ponto na faixa de iteração correspondente.

    Args:
        c: Parâmetro complexo do polinômio.
        d: Grau do polinômio.
        n: Resolução por eixo (n x n pontos totais).
        n_max: Máximo de iterações por ponto.
        side: Semilado do quadrado analisado no plano complexo.
        num_faixas: Quantidade de faixas para agrupamento de cores.
        escape_radius: Limite de magnitude para escape.

    Returns:
        Dicionário mapeando cada índice de faixa (0 a num_faixas - 1)
        à lista de coordenadas complexas correspondentes.
    """
    matrizes = {i: [] for i in range(num_faixas)}

    for x in np.linspace(-side, side, n):
        for y in np.linspace(-side, side, n):
            z = complex(x, y)
            _, iteradas = calcular_orbita_julia(z, c, d, n_max, escape_radius=escape_radius)
            idx_faixa = min(math.floor(iteradas * (num_faixas - 1) / n_max), num_faixas - 1)
            matrizes[idx_faixa].append(z)

    return matrizes
