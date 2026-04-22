import os
import numpy as np
import matplotlib.pyplot as plt
import random as rd


def exibir_ou_salvar(nome_arquivo="images/juliaReverseCompleto.png"):
    backend = plt.get_backend().lower()
    if "agg" in backend:
        pasta_saida = os.path.dirname(nome_arquivo)
        if pasta_saida:
            os.makedirs(pasta_saida, exist_ok=True)
        plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
        print(f"Backend nao interativo detectado ({backend}). Figura salva em {nome_arquivo}.")
    else:
        plt.show()

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
    exibir_ou_salvar()

# Exemplo: Visualizar o conjunto de Julia para c = -1
if __name__ =="__main__":
    c = complex(input("Qual o 'c' do conjunto que deseja plotar? "))
    n = int(input("Quantas iterações deseja realizar? "))
    d = int(input("Qual o 'd' desejado? "))
    visualizar_conjunto_julia(c, n, d)

