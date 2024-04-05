#imports
import numpy as np
import matplotlib.pyplot as plt
import math

#calcula a órbita de um ponto para z^d
#recebe c, d e o máximo de iterações a se realizar
#retorna c e o número de iteradas gastas para se extravasar o limite
def orbitaM_zd(c, d, n_max):
    ponto = 0
    i = 0
    for i in range(n_max):
        ponto = ponto**d + c
        if abs(ponto) > 3:  
            return (c, i)
    return (c, n_max)

#recebe o número de pontos que se dividirá cada eixo, o valor de d e o número de iteradas para cada c(N)
def visualizar_conjunto_mandel_zd(n, d, N):
    #Determinando a largura da tela baseando-se no critério de escape
    lado = 2**(1/(d-1))

    
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', "black"]  # Lista de cores a serem utilizadas para colorir cada ponto
    #listas para se colocar os pontos conforme as cores  
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
            ponto, iteradas = orbitaM_zd(complex(x, y), d, N)  
            
            aux = math.floor(iteradas * (len(colors)-1) /N)
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


    plt.show()

if __name__ == "__main__":
    # entre com o número de divisões que quer fazer, qual d quer plotar e quantas iteradas para cada ponto
    print("Forneca números inteiros para os questionamentos a seguir")
    n = int(input("Quer dividir os eixor em quantas partes?(recomenda-se um número alto)  "))
    d = int(input("Qual o conjunto que deseja plotar?(especifique o d)  "))
    N = int(input("Quantas iteradas deseja fazer para cada c?(números altos implicam em maior precisão, entretanto podem sobrecarregar seu computador, recomenda-se algo entre 50 e 100) "))
    visualizar_conjunto_mandel_zd(n, d, N)