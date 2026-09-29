# Manual de Uso por Linha de Comando (CLI)

Este documento especifica e orienta o uso do projeto **JuliaMandelbrotConstruction** inteiramente através do terminal via **Interface de Linha de Comando (CLI)**.

O objetivo principal desta melhoria é eliminar a necessidade de intervenção interativa (`input()`), permitindo:
- Execução direta com flags e parâmetros configuráveis;
- Automação via scripts Bash (geração em lote, animações, estudos de parâmetros);
- Execução limpa em servidores remotos (via SSH sem encaminhamento X11) e pipelines de CI/CD;
- Opção explícita entre abrir a janela gráfica (`--show`) ou salvar diretamente o arquivo de imagem (`--no-show` ou `-o`).

---

## 🛠️ 1. Preparação do Ambiente

Antes de executar qualquer comando Python no projeto, ative o ambiente virtual:

```bash
source env/bin/activate
```

> **Dica de ambiente headless:** Em servidores sem interface gráfica ou em containers, defina o backend do Matplotlib para `Agg` e configure um diretório de cache gravável:
> ```bash
> export MPLBACKEND=Agg
> export MPLCONFIGDIR=/tmp/matplotlib-cache
> ```

---

## 💻 2. Formas de Execução

O projeto disponibiliza duas formas equivalentes de uso via terminal:

1. **CLI Unificada (`cli.py`):** Ponto de entrada central com subcomandos (`julia`, `mandelbrot`, `reverse`, `circle`).
2. **Scripts Individuais:** Execução direta de cada script passando os mesmos parâmetros via argumentos de linha de comando.

---

## 🚀 3. CLI Unificada (`cli.py`)

A CLI unificada reúne todas as funcionalidades em uma única interface padronizada.

### Sintaxe Geral:
```bash
python cli.py <subcomando> [opções]
```

Para consultar a ajuda geral ou de um subcomando específico:
```bash
python cli.py --help
python cli.py julia --help
python cli.py mandelbrot --help
python cli.py reverse --help
python cli.py circle --help
```

---

### 3.1. Subcomando `julia` (Conjunto de Julia Direto)

Calcula e plota o conjunto de Julia para $P_{d,c}(z) = z^d + c$ através do tempo de escape de cada ponto na grade complexa.

#### Parâmetros:
| Flag | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `-c`, `--c` | `complex` | `-0.4+0.6j` | Parâmetro complexo $c$ (ex: `-0.4+0.6j`, `0.285+0.01j`, `-0.8+0j`) |
| `-d`, `--degree` | `int` | `2` | Grau do polinômio $d$ |
| `-n`, `--resolution` | `int` | `600` | Resolução do grid por eixo ($n \times n$ pontos) |
| `-N`, `--iterations` | `int` | `80` | Número máximo de iterações por ponto |
| `-s`, `--side` | `float` | `2.0` | Semilado do plano complexo analisado $[-s, s]$ |
| `-o`, `--output` | `str` | `images/julia_zd.png` | Caminho do arquivo de saída da imagem |
| `--no-show` | `flag` | Ativo por padrão se `-o` for especificado | Não abre a janela do Matplotlib |
| `--show` | `flag` | `False` | Força a exibição da janela gráfica interativa |

#### Exemplos de uso:
```bash
# Execução padrão (salva em images/julia_zd.png)
python cli.py julia

# Conjunto com c customizado e resolução de 1000x1000
python cli.py julia -c "-0.8+0.156j" -d 2 -n 1000 -N 120 -o images/dendrite.png --no-show

# Grau d = 3 (cúbico)
python cli.py julia -d 3 -c "-0.4+0.6j" -n 800 -o images/julia_cubico.png --no-show
```

---

### 3.2. Subcomando `mandelbrot` (Conjunto de Mandelbrot)

Analisa a órbita do ponto crítico para a família $z^d + c$ variando o valor de $c$ no plano complexo.

#### Parâmetros:
| Flag | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `-d`, `--degree` | `int` | `2` | Grau da família $z^d + c$ |
| `-n`, `--resolution` | `int` | `600` | Resolução por eixo ($n \times n$) |
| `-N`, `--iterations` | `int` | `80` | Máximo de iterações de teste |
| `-o`, `--output` | `str` | `images/mandelbrot_zd.png` | Caminho do arquivo de saída |
| `--no-show` | `flag` | - | Não abre a janela gráfica |
| `--show` | `flag` | `False` | Força a exibição gráfica na tela |

#### Exemplos de uso:
```bash
# Mandelbrot clássico (d=2)
python cli.py mandelbrot -d 2 -n 800 -N 100 -o images/mandelbrot_classico.png --no-show

# Multibrot (d=3)
python cli.py mandelbrot -d 3 -n 800 -N 100 -o images/multibrot_d3.png --no-show

# Multibrot de ordem superior (d=5) em alta definição
python cli.py mandelbrot -d 5 -n 1200 -N 150 -o images/multibrot_d5.png --no-show
```

---

### 3.3. Subcomando `reverse` (Julia via Iteração Reversa Aleatória)

Gera a aproximação do conjunto de Julia escolhendo estocasticamente ramos da raiz $d$-ésima inversa em cada passo.

#### Parâmetros:
| Flag | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `-c`, `--c` | `complex` | `-1+0j` | Parâmetro complexo $c$ |
| `-d`, `--degree` | `int` | `2` | Grau da raiz inversa |
| `-n`, `--iterations` | `int` | `100000` | Quantidade total de pontos/iterações reversas |
| `--seed` | `int` | `None` | Semente pseudoaleatória (para reprodutibilidade) |
| `-o`, `--output` | `str` | `images/juliaReverseCompleto.png` | Caminho do arquivo de saída |
| `--no-show` | `flag` | - | Salva sem abrir janela gráfica |

#### Exemplos de uso:
```bash
# Iteração reversa rápida com 50.000 pontos
python cli.py reverse -c "-0.75+0.1j" -d 2 -n 50000 -o images/reverse_fast.png --no-show

# Alta densidade de pontos com semente fixa para reprodução exata
python cli.py reverse -c "-1+0j" -d 2 -n 200000 --seed 42 -o images/reverse_reproduzivel.png --no-show
```

---

### 3.4. Subcomando `circle` (Pré-imagens Reversas do Círculo)

Calcula as pré-imagens sucessivas da equação $z^d + c = \text{círculo}$, gerando conjuntos que convergem para a fronteira de Julia.

#### Parâmetros:
| Flag | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `-d`, `--degree` | `int` | `2` | Grau da raiz a cada etapa |
| `-n`, `--rounds` | `int` | `2` | Número de rodadas de pré-imagens aplicadas |
| `--rang` | `int` | `10000` | Número de pontos discretos na curva do círculo inicial |
| `-o`, `--output` | `str` | `images/iteracoesReversasCirculo.png` | Caminho do arquivo de saída |
| `--no-show` | `flag` | - | Salva sem abrir janela gráfica |

#### Exemplos de uso:
```bash
# Execução leve (2 rodadas de pré-imagens)
python cli.py circle -d 2 -n 2 -o images/circulo_r2.png --no-show

# 3 rodadas de pré-imagens com 15.000 pontos
python cli.py circle -d 2 -n 3 --rang 15000 -o images/circulo_r3.png --no-show
```

---

## 📜 4. Execução Direta dos Scripts Individuais

Caso prefira rodar os arquivos `.py` diretamente (como nos comandos do README original), os scripts mantêm total suporte a flags CLI e fallback inteligente:

```bash
# julia_zd.py
python julia_zd.py -c -0.4+0.6j -d 2 -n 600 -N 80 -o images/julia_zd.png --no-show

# mandelbrot_zd.py
python mandelbrot_zd.py -d 2 -n 600 -N 80 -o images/mandelbrot_zd.png --no-show

# juliaReverseCompleto.py
python juliaReverseCompleto.py -c -1+0j -d 2 -n 100000 -o images/juliaReverseCompleto.png --no-show

# iteracoesReversasCirculo.py
python iteracoesReversasCirculo.py -d 2 -n 2 --rang 10000 -o images/iteracoesReversasCirculo.png --no-show
```

> **Compatibilidade:** Se executado sem argumentos e sem flags, o script pode operar no modo interativo original solicitando os valores via `input()`, garantindo que scripts legados continuem funcionando.

---

## 🤖 5. Automação e Scripts em Lote (Batch Scripts)

Com o suporte a CLI, é possível automatizar a geração de coleções e animações diretamente no terminal com Bash.

### Exemplo 1: Explorar uma família de conjuntos de Julia variando a parte imaginária de $c$
Crie um script `sweep_julia.sh`:

```bash
#!/usr/bin/env bash
source env/bin/activate
mkdir -p images/sweep

# Varia a parte imaginária de 0.50 a 0.65 em 6 passos
for im in 0.50 0.53 0.56 0.59 0.62 0.65; do
    echo "Gerando Julia para c = -0.4 + ${im}j..."
    python cli.py julia -c "-0.4+${im}j" -d 2 -n 700 -N 90 \
        -o "images/sweep/julia_im_${im}.png" --no-show
done
echo "Concluído! Imagens salvas em images/sweep/"
```

### Exemplo 2: Gerar Multibrots para graus de 2 a 6
```bash
#!/usr/bin/env bash
source env/bin/activate
mkdir -p images/multibrots

for d in 2 3 4 5 6; do
    echo "Calculando Mandelbrot grau ${d}..."
    python cli.py mandelbrot -d "${d}" -n 800 -N 100 \
        -o "images/multibrots/mandelbrot_d${d}.png" --no-show
done
```

---

## ❓ 6. Dúvidas Frequentes e Resolução de Problemas

1. **Como passar números complexos com segurança?**
   O parser aceita formatos padrão do Python:
   - `-c "-0.4+0.6j"` (com aspas para evitar conflitos no bash com o sinal de `+` ou `-`)
   - `-c "0.285-0.01j"`
   - `-c "-1"` ou `-c "-1+0j"`

2. **Como rodar sem que o programa tente abrir janela no meu monitor?**
   Basta adicionar a flag `--no-show` ou definir a variável `export MPLBACKEND=Agg`.

3. **Como gerar imagens com maior nitidez?**
   Aumente o parâmetro `-n` (ex: `-n 1200` ou `-n 2000`) e aumente `-N` (ex: `-N 150` ou `-N 250`).
