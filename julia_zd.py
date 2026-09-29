
import os
import sys
import math
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

lado = 2


def parse_complex(valor: str) -> complex:
    s = valor.strip().replace(" ", "").replace("i", "j").replace("I", "J")
    try:
        return complex(s)
    except ValueError as err:
        raise argparse.ArgumentTypeError(f"Número complexo inválido: '{valor}'") from err


def exibir_ou_salvar(nome_arquivo="images/julia_zd.png", show=None):
    backend = plt.get_backend().lower()
    pasta_saida = os.path.dirname(nome_arquivo)
    if pasta_saida:
        os.makedirs(pasta_saida, exist_ok=True)
    plt.savefig(nome_arquivo, dpi=300, bbox_inches="tight")
    print(f"Figura salva em {nome_arquivo}.")
    if show is True or (show is None and "agg" not in backend):
        plt.show()
    plt.close()


def orbita(z, c, d, n_max):
    ponto = z
    for i in range(n_max+1):
        ponto = ponto**d + c
        #ponto = ponto**6
        if abs(ponto) > 5:  # Limitar a magnitude para evitar overflow
            return (z, i)
    return (z, n_max)

def visualizar_conjunto_julia(c, n, d, N, nome_arquivo="images/julia_zd.png", show=None):
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
    plt.plot(np.real(matrizYellow), np.imag(matrizYellow), 'o', markersize = 0.2, color = colors[2])            
    plt.plot(np.real(matrizGreen), np.imag(matrizGreen), 'o', markersize = 0.1, color = colors[3])            
    plt.plot(np.real(matrizBlue), np.imag(matrizBlue), 'o', markersize = 0.1, color = colors[4])            
    plt.plot(np.real(matrizIndigo), np.imag(matrizIndigo), 'o', markersize = 0.1, color = colors[5])            
    plt.plot(np.real(matrizViolet), np.imag(matrizViolet), 'o', markersize = 0.1, color = colors[6])            
    plt.plot(np.real(matrizBlack), np.imag(matrizBlack), 'o', markersize = 0.1, color = colors[7])            

    plt.title(f"Conjunto de Julia para d = {d} e c = {c}")
    plt.xlabel("Parte Real")
    plt.ylabel("Parte Imaginária")
    exibir_ou_salvar(nome_arquivo=nome_arquivo, show=show)

#visualizar_conjunto_julia(a, b, c)
# Exemplo: Visualizar o conjunto de Julia para c = a, lado do grid indo de -c a c e dividindo o grid em b^2 pontos a serem analisados

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Conjunto de Julia por tempo de escape direto.")
    parser.add_argument("-d", "--degree", type=int, help="Grau d do polinômio")
    parser.add_argument("-c", "--c", type=parse_complex, help="Parâmetro complexo c (ex: -0.4+0.6j)")
    parser.add_argument("-n", "--resolution", type=int, help="Resolução da grade nxn")
    parser.add_argument("-N", "--iterations", type=int, help="Número de iterações máximas")
    parser.add_argument("-o", "--output", default="images/julia_zd.png", help="Arquivo de saída (padrão: images/julia_zd.png)")
    parser.add_argument("--no-show", action="store_true", help="Não abre a janela gráfica do Matplotlib")
    parser.add_argument("--show", action="store_true", help="Força a exibição da janela gráfica")

    if len(sys.argv) > 1:
        args = parser.parse_args()
        d_val = args.degree if args.degree is not None else 2
        c_val = args.c if args.c is not None else -0.4 + 0.6j
        n_val = args.resolution if args.resolution is not None else 600
        N_val = args.iterations if args.iterations is not None else 80
        show_flag = False if args.no_show else (True if args.show else None)
        visualizar_conjunto_julia(c_val, n_val, d_val, N_val, nome_arquivo=args.output, show=show_flag)
    else:
        print("Forneca números para os questionamentos a seguir (ou use flags CLI via --help):")
        d_val = int(input("Qual o 'd' do conjunto que deseja plotar? "))
        c_val = parse_complex(input("Qual o 'c' do conjunto que deseja plotar? "))
        n_val = int(input("Quer dividir os eixos em quantas partes?(recomenda-se um número alto)  "))
        N_val = int(input("Quantas iteradas deseja fazer para cada ponto?(números altos implicam em maior precisão, entretanto podem sobrecarregar seu computador, recomenda-se algo entre 50 e 100) "))
        visualizar_conjunto_julia(c_val, n_val, d_val, N_val)



