#!/usr/bin/env python3
"""
Ponto de entrada unificado para a CLI do projeto JuliaMandelbrotConstruction.
Delega a execução para o pacote modular juliamandelbrot.cli.
"""

import sys
from pathlib import Path

# Adiciona o diretório 'src' ao sys.path para importação do pacote
src_path = str(Path(__file__).resolve().parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from juliamandelbrot.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
