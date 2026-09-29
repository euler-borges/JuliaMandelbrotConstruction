"""
Pacote juliamandelbrot: computação e visualização de fractais das famílias de Julia e Mandelbrot.
"""

from juliamandelbrot.core import (
    calcular_orbita_julia,
    calcular_grid_julia,
    calcular_orbita_mandelbrot,
    calcular_grid_mandelbrot,
    calcular_julia_reverso,
    construir_circulo,
    raiz_d_circulo,
    calcular_pre_imagens_circulo,
)

__version__ = "0.2.0"

__all__ = [
    "calcular_orbita_julia",
    "calcular_grid_julia",
    "calcular_orbita_mandelbrot",
    "calcular_grid_mandelbrot",
    "calcular_julia_reverso",
    "construir_circulo",
    "raiz_d_circulo",
    "calcular_pre_imagens_circulo",
]
