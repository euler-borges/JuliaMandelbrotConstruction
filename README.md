# JuliaMandelbrotConstruction

Project for plotting Julia and Mandelbrot sets for functions in the family $P_{d,c}(z) = z^d + c$, plus a reverse-iteration experiment.

## Requirements

- Linux, macOS or Windows
- Python 3.9+
- Python libraries:
  - numpy
  - matplotlib

## Installation

From the project directory, run:

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

## How To Run

All scripts are interactive (they prompt for parameters in the terminal).

### 1) Julia Set by Forward Orbit Iteration

File: julia_zd.py

Run:

python3 julia_zd.py

Requested parameters:

- d: polynomial degree in $z^d + c$ (positive integer)
- c: complex parameter
- n: number of grid divisions per axis (resolution)
- N: maximum number of iterations per point

Notes:

- Higher n and N values improve quality but increase runtime.
- For complex c, use Python complex-number format. Valid examples:
  - -0.4+0.6j
  - 0.285+0.01j
  - -0.8+0j

### 2) Mandelbrot Set for $z^d + c$

File: mandelbrot_zd.py

Run:

python3 mandelbrot_zd.py

Requested parameters:

- n: number of divisions per axis in the complex plane
- d: polynomial degree
- N: maximum number of iterations for each c value

Notes:

- The script automatically sets the plotting window to $2^{1/(d-1)}$.
- Large n and N values significantly increase computational cost.

### 3) Julia Set by Random Reverse Iteration

File: juliaReverseCompleto.py

Run:

python3 juliaReverseCompleto.py

Requested parameters:

- c: complex parameter
- n: number of reverse iterations (number of points)
- d: root degree used in reverse iteration

Notes:

- The method randomly chooses one branch of the d-th root at each step.
- Different runs may produce slightly different point clouds.

### 4) Reverse Iterations of a Circle

File: iteracoesReversasCirculo.py

Run:

python3 iteracoesReversasCirculo.py

Requested parameters:

- d: root degree to compute at each step
- n: number of reverse-iteration rounds applied to the initial set

Fixed internal code parameter:

- RANG = 200000: number of points used to build the initial circle

Notes:

- This script can consume a lot of memory because the number of points grows quickly with each iteration.

## Suggested Starter Values

To start with a lighter execution load:

- julia_zd.py: d = 2, c = -0.4+0.6j, n = 600, N = 80
- mandelbrot_zd.py: d = 2, n = 600, N = 80
- juliaReverseCompleto.py: c = -1+0j, n = 100000, d = 2
- iteracoesReversasCirculo.py: d = 2, n = 2

## Common Issues

- Module not found error:
  - Reinstall dependencies with python3 -m pip install -r requirements.txt
- Plot is too slow:
  - Reduce n and/or N in grid-based scripts (julia_zd.py and mandelbrot_zd.py)
  - Reduce n in the reverse-iteration script
- Invalid complex input:
  - Use the j suffix for the imaginary part (example: 0.2+0.3j)
