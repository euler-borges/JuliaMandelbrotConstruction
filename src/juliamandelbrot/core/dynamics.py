"""
Módulo de dinâmica reversa estocástica e cálculo de pré-imagens de curvas.
Contém apenas lógica matemática pura sem dependência de bibliotecas de plotagem.
"""

import math
import random
import numpy as np


def calcular_julia_reverso(
    c: complex,
    d: int,
    n: int,
    ponto_inicial: complex = 0.5 + 0.5j,
    seed: int | None = None,
) -> np.ndarray:
    """
    Gera a aproximação da fronteira de Julia através de iterações reversas estocásticas.
    A cada passo, uma das d raízes de (z - c) é selecionada aleatoriamente.

    Args:
        c: Parâmetro complexo do conjunto.
        d: Grau da raiz d-ésima (d >= 2).
        n: Número total de iterações/pontos.
        ponto_inicial: Ponto semente no plano complexo.
        seed: Semente para o gerador pseudoaleatório (opcional).

    Returns:
        Array NumPy de tipo complex128 com n pontos da órbita reversa.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    matriz = np.zeros(n, dtype=np.complex128)
    ponto = complex(ponto_inicial)

    for i in range(n):
        ramo = random.randrange(d)
        ponto = np.power((ponto - c), 1.0 / d) * np.exp((2.0 * np.pi * 1j * ramo) / d)
        matriz[i] = ponto

    return matriz


def construir_circulo(rang: int = 10000, raio: float = 3.0) -> list[complex]:
    """
    Constrói os pontos discretizados de uma circunferência centrada na origem.

    Args:
        rang: Número de divisões na circunferência.
        raio: Raio do círculo no plano complexo.

    Returns:
        Lista de coordenadas complexas ao longo do círculo.
    """
    return [
        (math.cos(2.0 * math.pi * i / rang) + 1j * math.sin(2.0 * math.pi * i / rang)) * raio
        for i in range(rang)
    ]


def raiz_d_circulo(pontos: list[complex], d: int, deslocamento: float = 3.0) -> list[complex]:
    """
    Calcula as d pré-imagens de cada ponto sob a transformação inversa w -> (w - deslocamento)^(1/d).

    Args:
        pontos: Lista de pontos complexos da etapa anterior.
        d: Grau da raiz.
        deslocamento: Constante subtraída antes da radiciação (padrão histórico do projeto: 3.0).

    Returns:
        Nova lista contendo len(pontos) * d pontos complexos pré-imagem.
    """
    raizes = []
    for pt in pontos:
        base = np.power(pt - deslocamento, 1.0 / d)
        for p in range(d):
            raizes.append(base * np.exp(2.0 * math.pi * 1j * p / d))
    return raizes


def calcular_pre_imagens_circulo(
    circulo_base: list[complex],
    d: int,
    n_rounds: int,
    deslocamento: float = 3.0,
) -> list[list[complex]]:
    """
    Calcula sucessivas rodadas de pré-imagens a partir do círculo inicial.

    Args:
        circulo_base: Pontos da circunferência inicial.
        d: Grau da raiz.
        n_rounds: Quantidade de rodadas de pré-imagens.
        deslocamento: Constante subtraída antes da radiciação.

    Returns:
        Lista com as pré-imagens calculadas para cada rodada [rodada_1, rodada_2, ...].
    """
    historico = []
    atual = circulo_base
    for _ in range(n_rounds):
        atual = raiz_d_circulo(atual, d, deslocamento=deslocamento)
        historico.append(atual)
    return historico
