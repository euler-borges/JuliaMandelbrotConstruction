# Guia Técnico de Refatoração e Código

Este documento serve como referência de engenharia para desenvolvedores que desejam estender, refatorar ou auditar o código do **JuliaMandelbrotConstruction**.

---

## 🧩 1. Padrão de Parsing Seguro para Números Complexos

No terminal, usuários podem passar números complexos em diferentes formatações:
- `-0.4+0.6j`
- `0.285 + 0.01j` (com espaços)
- `-1` ou `2.5` (números reais puros)
- `1j` ou `-0.5j` (imaginários puros)
- `-0.4+0.6i` (usando `i` em vez da convenção Python `j`)

Para garantir que a CLI seja tolerante a essas variações, o conversor técnico recomendado é:

```python
import argparse

def parse_complex(valor_str: str) -> complex:
    """
    Converte uma string para o tipo complex nativo do Python,
    tratando variações comuns (espaços em branco e uso de 'i' no lugar de 'j').
    """
    s = valor_str.strip().replace(" ", "").replace("i", "j").replace("I", "J")
    try:
        return complex(s)
    except ValueError as err:
        raise argparse.ArgumentTypeError(
            f"Valor complexo inválido: '{valor_str}'. "
            f"Exemplos válidos: '-0.4+0.6j', '0.285-0.01j', '-1+0j'"
        ) from err
```

---

## ⚡ 2. Comparativo Técnico: Loops vs. Vetorização NumPy

### O Algoritmo Original (Loops em Python):
```python
# Ineficiente para resoluções médias/altas (O(n² * N) no interpretador Python)
for x in np.linspace(-lado, lado, n):
    for y in np.linspace(-lado, lado, n):
        ponto, iteradas = orbita(complex(x, y), c, d, iteradasOrbita)
        # Classificação condicional de cores e append em listas...
```

### O Algoritmo Vetorizado Proposto (NumPy Array Ops):
```python
import numpy as np

def compute_julia_matrix(c: complex, n: int, d: int, n_max: int, side: float = 2.0) -> np.ndarray:
    """
    Calcula a matriz de tempos de escape para o conjunto de Julia de forma 100% vetorizada.
    
    Retorna:
        Matriz 2D de inteiros (n x n) contendo o número de iterações até o escape
        ou n_max caso pertença ao conjunto.
    """
    # 1. Criação do grid complexo contíguo na memória
    x = np.linspace(-side, side, n, dtype=np.float64)
    y = np.linspace(-side, side, n, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # 2. Inicialização das matrizes de iteração e máscara de pontos ativos
    escape_time = np.full(Z.shape, n_max, dtype=np.int32)
    active_mask = np.ones(Z.shape, dtype=bool)
    
    # 3. Raio de escape baseado no grau d
    escape_radius_sq = max(4.0, abs(c) + 2.0)**2
    
    for i in range(n_max):
        if not np.any(active_mask):
            break
            
        # Itera apenas os pontos que ainda não escaparam
        Z[active_mask] = Z[active_mask]**d + c
        
        # Identifica pontos que ultrapassaram o raio de escape nesta iteração
        escaped_now = (np.real(Z)**2 + np.imag(Z)**2 > escape_radius_sq) & active_mask
        escape_time[escaped_now] = i
        active_mask[escaped_now] = False
        
    return escape_time
```

### Renderização Otimizada com `plt.imshow`:
Substituindo as 8 chamadas lentas de `plt.plot()` por uma renderização matricial única:

```python
import matplotlib.pyplot as plt

def render_escape_matrix(matrix: np.ndarray, side: float, title: str, output_file: str, show: bool = False):
    plt.figure(figsize=(8, 8))
    # 'imshow' renderiza a matriz inteira em milissegundos
    plt.imshow(
        matrix,
        extent=[-side, side, -side, side],
        origin='lower',
        cmap='inferno'
    )
    plt.colorbar(label="Iterações até o escape")
    plt.title(title)
    plt.xlabel("Re(z)")
    plt.ylabel("Im(z)")
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"Imagem gerada e salva com sucesso em: {output_file}")
        
    if show:
        plt.show()
    plt.close()
```

---

## 🖥️ 3. Boas Práticas para Matplotlib em Ambientes de Linha de Comando

Ao rodar ferramentas de computação científica estritamente por linha de comando em servidores ou agentes de automação, alguns cuidados devem ser tomados para evitar avisos ou erros de backend:

1. **Seleção de backend headless:**
   ```python
   import matplotlib
   # Se o usuário não solicitou explicitamente exibir janela interativa,
   # define o backend 'Agg' antes de importar pyplot:
   matplotlib.use("Agg")
   import matplotlib.pyplot as plt
   ```
2. **Criação e isolamento do cache:**
   Em alguns sistemas onde o diretório `~/.config` possui restrições de permissão, o Matplotlib emite avisos de cache. A solução limpa é direcionar `MPLCONFIGDIR`:
   ```bash
   export MPLCONFIGDIR=/tmp/matplotlib-cache
   ```
3. **Sempre fechar as figuras:**
   Chamar explicitamente `plt.close()` após salvar ou exibir a imagem para liberar memória do processo, prevenindo vazamentos de recursos em scripts em lote (batch processing).

---

## 🧪 4. Exemplo de Teste Unitário com `pytest`

Para assegurar que o cálculo de $z^d + c$ produza resultados matemáticos corretos:

```python
# tests/test_dynamics.py
import numpy as np
import pytest

def test_mandelbrot_origin_stable():
    """Para d=2 e c=0, z_0 = 0 -> z_1 = 0 -> nunca escapa."""
    from cli import compute_mandelbrot_point # ou módulo core
    c = 0j
    _, iteradas = orbitaM_zd(c, d=2, n_max=50)
    assert iteradas == 50

def test_mandelbrot_outside_diverges():
    """Pontos com magnitude grande devem escapar quase imediatamente."""
    c = complex(5.0, 5.0)
    _, iteradas = orbitaM_zd(c, d=2, n_max=50)
    assert iteradas < 5
```
