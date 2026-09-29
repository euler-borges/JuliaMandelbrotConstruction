"""
Utilitários de conversão e validação de parâmetros.
"""

import argparse


def parse_complex(valor: str) -> complex:
    """
    Converte uma string para o tipo complex nativo do Python,
    aceitando 'j' ou 'i', com ou sem espaços.
    
    Exemplos aceitos:
        "-0.4+0.6j", "-0.4 + 0.6i", "-1", "2.5", "1j", "-0.5i"
    """
    if isinstance(valor, complex):
        return valor
    if isinstance(valor, (int, float)):
        return complex(valor, 0.0)

    s = valor.strip().replace(" ", "").replace("i", "j").replace("I", "J")
    try:
        return complex(s)
    except ValueError as err:
        raise argparse.ArgumentTypeError(
            f"Valor complexo inválido: '{valor}'. "
            f"Exemplos válidos: '-0.4+0.6j', '0.285-0.01j', '-1+0j'"
        ) from err


def validar_inteiro_positivo(valor: int, nome: str = "parâmetro") -> int:
    """Valida se o valor é um inteiro positivo >= 1."""
    if valor < 1:
        raise ValueError(f"O {nome} deve ser um inteiro maior ou igual a 1. Recebido: {valor}")
    return valor
