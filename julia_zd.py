

import math 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

lado = 2


def orbita(z, c, d, n_max):
    ponto = z
    for i in range(n_max+1):
        ponto = ponto**d + c
        #ponto = ponto**6
        if abs(ponto) > 5:  # Limitar a magnitude para evitar overflow
            return (z, i)
    return (z, n_max)

def visualizar_conjunto_julia(c, n, d, N):
    #quantas iteradas serão calculadas na o´rbita dos pontos
    iteradasOrbita = N
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', "black"]  # Lista de cores para cada ponto
    matrizRed = []
    matrizOrange = []
    matrizYellow = []
    matrizGreen = []
    matrizBlue = []
    matrizIndigo = []
    matrizViolet = []
    matrizBlack = []


    for i, x in enumerate(np.linspace(-lado, lado, n)):
        for j, y in enumerate(np.linspace(-lado, lado, n)):
            ponto, iteradas = orbita(complex(x, y), c,d, iteradasOrbita)  # Limitar o número de iterações
            aux = math.floor(iteradas * (len(colors)-1) /iteradasOrbita)
            if (aux) == 0:
                matrizRed.append(ponto)
            elif (aux) == 1:
                matrizOrange.append(ponto)
            elif (aux) == 2:
                matrizYellow.append(ponto)
            elif (aux) == 3:
                matrizGreen.append(ponto)
            elif (aux) == 4:
                matrizBlue.append(ponto)
            elif (aux) == 5:
                matrizIndigo.append(ponto)
            elif (aux) == 6:
                matrizViolet.append(ponto)
            else:
                matrizBlack.append(ponto)


    plt.plot(np.real(matrizRed), np.imag(matrizRed), 'o', markersize = 0.1, color = colors[0])            
    plt.plot(np.real(matrizOrange), np.imag(matrizOrange), 'o', markersize = 0.1, color = colors[1])            
    plt.plot(np.real(matrizYellow), np.imag(matrizYellow), 'o', markersize = 0.1, color = colors[2])            
    plt.plot(np.real(matrizGreen), np.imag(matrizGreen), 'o', markersize = 0.1, color = colors[3])            
    plt.plot(np.real(matrizBlue), np.imag(matrizBlue), 'o', markersize = 0.1, color = colors[4])            
    plt.plot(np.real(matrizIndigo), np.imag(matrizIndigo), 'o', markersize = 0.1, color = colors[5])            
    plt.plot(np.real(matrizViolet), np.imag(matrizViolet), 'o', markersize = 0.1, color = colors[6])            
    plt.plot(np.real(matrizBlack), np.imag(matrizBlack), 'o', markersize = 0.1, color = colors[7])            

    plt.title(f"Conjunto de Julia para d = {d} e c = {c}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    plt.show()

#visualizar_conjunto_julia(a, b, c)
# Exemplo: Visualizar o conjunto de Julia para c = a, lado do grid indo de -c a c e dividindo o grid em b^2 pontos a serem analisados

if __name__ == "__main__":
    # entre com o número de divisões que quer fazer, qual d quer plotar e quantas iteradas para cada ponto
    print("Forneca números inteiros para os questionamentos a seguir")
    d = int(input("Qual o 'd' do conjunto que deseja plotar? "))
    c = complex(input("Qual o 'c' do conjunto que deseja plotar? "))
    n = int(input("Quer dividir os eixos em quantas partes?(recomenda-se um número alto)  "))

    N = int(input("Quantas iteradas deseja fazer para cada ponto?(números altos implicam em maior precisão, entretanto podem sobrecarregar seu computador, recomenda-se algo entre 50 e 100) "))
    visualizar_conjunto_julia(c, n, d, N)



