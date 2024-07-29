import numpy as np
import matplotlib.pyplot as plt
import random as rd

def visualizar_conjunto_julia(c, n, d):
    matriz = np.zeros(n, dtype=np.complex128)
    ponto = complex(0.5, 0.5)

    for i in range(n):
        aleatorio = rd.randrange(d)
        ponto = np.power((ponto - c), 1/d)*np.exp((np.pi*2*aleatorio/d)*1j)

        matriz[i] = ponto

    plt.plot(np.real(matriz), np.imag(matriz), 'o', markersize=0.3, color='blue')
    plt.title(f"Conjunto de Julia para c = {c}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    plt.show()

# Exemplo: Visualizar o conjunto de Julia para c = -1
if __name__ =="__main__":
    c = complex(input("Qual o 'c' do conjunto que deseja plotar? "))
    n = int(input("Quantas iterações deseja realizar? "))
    d = int(input("Qual o 'd' desejado? "))
    visualizar_conjunto_julia(c, n, d)

