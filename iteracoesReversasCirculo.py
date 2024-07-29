import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import math

RANG = 200000

def raiz_d(circulo, d):
    raiz_proxima = []
    for i in range(len(circulo)):
        p = 0
        raiz_calculada = np.power(circulo[i]-3, 1/d) 
        while p < d:
            raiz_proxima.append(raiz_calculada*np.exp(1j*2*math.pi*p/d))
            p += 1
    return raiz_proxima


def constroiCirculo(RANG):
    circulo = []
    for i in range(RANG):
        circulo.append((math.cos(2*math.pi*i/RANG)+ 1j*math.sin(2*math.pi*i/RANG))*3)
    return circulo


def plotaRaizes(circulo):
    d = int(input("Raiz de que grau? "))
    n = int(input("Quantas iteradas? "))
    
    raiz = raiz_d(circulo, d)
    
    plt.plot(np.real(raiz), np.imag(raiz), 'o', markersize = 1, color = "black")
    for i in range(n-1):
        raiz = raiz_d(raiz, d)
        plt.plot(np.real(raiz), np.imag(raiz), 'o', markersize = 1, color = "black")



circulo = constroiCirculo(RANG)




plt.title("Raiz do círculo")
plt.xlabel("Parte Real")
plt.ylabel("Parte Imaginária")
plt.plot(np.real(circulo), np.imag(circulo), 'o', markersize = 1, color = "black")
plotaRaizes(circulo)
#plt.text(0.22, 0.61, "A", fontsize = 10)
#plt.text(-0.6, 0, "B", fontsize = 10)
#plt.text(0.23, -0.5, "C", fontsize = 10)
plt.show()
