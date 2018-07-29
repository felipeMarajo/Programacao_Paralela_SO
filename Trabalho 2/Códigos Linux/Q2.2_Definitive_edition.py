from multiprocessing import Semaphore, Queue
import time, os, multiprocessing
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

def processo1(buffer12, semaforo):
    while True:
        pacotes = os.popen("sudo tcpdump -i wlan0 -c 1 -v|grep proto").read()
        #print(pacotes)
        if pacotes != "":
            dados = pacotes[pacotes.index("proto"):].split(" ")[1] + " " + pacotes[pacotes.index("proto"):].split(" ")[
                                                                               4][:-2]
            if ("TCP " in dados) or ("UDP" in dados) or ("SMTP" in dados):
                print(dados)
                semaforo.acquire()
                buffer12.put(dados) # add dados em buffer12
                semaforo.acquire()


# sum() é a soma de todos os elementos da lista
def medias(lista):
    if len(lista) > 0:
        return sum(lista) / len(lista)
    else:
        return 0


def variancias(lista):
    med = medias(lista)
    somatorio = 0
    if len(lista) > 0:
        for valor in lista:
            somatorio += pow((valor - med), 2)
        variancia = somatorio / float(len(lista))
        return variancia
    return 0


def processo2(buffer12, buffer23, semaforo, semaforo2):
    tcp = []
    udp = []    # Lista para guardar tamnho dos pacotes
    smtp = []


    #print(buffer12)

    while True:

        time.sleep(30)
        while not buffer23.empty():
            semaforo2.acquire()     # entra na exclusão mutua
            buffer23.get()          # esvazia o buffer2
            semaforo2.release()     # sai da exclusão mutua


        vetor_aux = []
        while not buffer12.empty():
            semaforo.acquire()
            vetor_aux.append(buffer12.get())    # passa o conteúdo para vetor_aux
            print(vetor_aux)
            semaforo.release()

        for i in vetor_aux: # Separa as informações em três lista
            if "TCP" in i:
                tcp.append(sum([int(x) for x in i.split(" ")[1:]]))
            if "UDP" in i:
                udp.append(sum([int(x) for x in i.split(" ")[1:]]))
            if "SMTP" in i:
                smtp.append(sum([int(x) for x in i.split(" ")[1:]]))

        # coloca as informações no buffer23
        semaforo2.acquire()
        buffer23.put(int(len(udp)))
        buffer23.put(int(medias(udp)))
        buffer23.put(int(variancias(udp)))
        # Num. Media e variancia de TCP
        buffer23.put(int(len(tcp)))
        buffer23.put(int(medias(tcp)))
        buffer23.put(int(variancias(tcp)))
        # Num. Media e variancia de SMTP
        buffer23.put(int(len(smtp)))
        buffer23.put(int(medias(smtp)))
        buffer23.put(int(variancias(smtp)))

        semaforo2.release()

        udp.clear()
        tcp.clear() # limpa as listas, melhor resultado
        smtp.clear()


def processo3(buffer23, semaforo2):
    fig = plt.figure()  # inicia uma janela

    # inicia três graficos na janela
    ax1 = fig.add_subplot(311, axisbg='grey')
    ax2 = fig.add_subplot(312, axisbg='grey')
    ax3 = fig.add_subplot(313, axisbg='grey')

    time.sleep(30)

    y1 = [[0], [0], [0]]
    x1 = [[0], [0], [0]]
    y2 = [[0], [0], [0]]    #listas que serão plotadas
    y3 = [[0], [0], [0]]

    def animate(i): # função para atualização das informações

        auxiliar = []

        while not buffer23.empty():
            semaforo2.acquire()
            auxiliar.append(str(buffer23.get()))  # conteúdo de buffer está em teste
            semaforo2.release()

        num = [auxiliar[0], auxiliar[3], auxiliar[6]]
        med = [auxiliar[1], auxiliar[4], auxiliar[7]]
        var = [auxiliar[2], auxiliar[5], auxiliar[8]]

        print(num)
        print(med)
        print(var)

        if len(auxiliar) != 0:
            for i in range(3):
                x1[i].append(len(x1[i]))
                y1[i].append(num[i])
                y2[i].append(med[i])
                y3[i].append(var[i])

        ax1.clear()
        ax2.clear()
        ax3.clear()

        for j in range(3):  # plota as informações no gráfico
            ax1.plot(x1[j], y1[j], marker="^")
            ax2.plot(x1[j], y2[j], marker="o")
            ax3.plot(x1[j], y3[j], marker="p")

        ax1.legend(["num udp", "num tcp", "num smtp"], loc="upper left")
        ax1.set_xlabel("tempo")
        ax1.set_ylabel("Quantidade")

        ax2.legend(["media udp", "media tcp", "media smtp"], loc="upper left")
        ax2.set_xlabel("tempo")
        ax2.set_ylabel("Quantidade")

        ax3.legend(["var udp", "var tcp", "var smtp"], loc="upper left")
        ax3.set_xlabel("tempo")
        ax3.set_ylabel("Quantidade")

    # loop na função animate com delay de 30 segundos
    anim = animation.FuncAnimation(fig, animate, interval=30000)
    plt.show()


if __name__ == '__main__':
    # cria duas filas FIFO de tamanhos 30 e 9
    c12 = Queue(maxsize=30)
    c23 = Queue(maxsize=9)

    # inicia dois semaforos
    smf = Semaphore()
    smf2 = Semaphore()

    p1 = os.fork()      # Chamada fork()
    if p1 == 0:         # se p1 == 0: é filho
        processo1(c12, smf)  # código para processo filho 1

    time.sleep(10)
    p2 = os.fork()
    if p2 == 0:
        processo2(c12, c23, smf, smf2)

    p3 = os.fork()
    if p3 == 0:
        processo3(c23, smf2)

    os.waitpid(os.P_ALL, 0)
    os.popen("kill " + str(os.getpid())).close()  # Mata o processo pai