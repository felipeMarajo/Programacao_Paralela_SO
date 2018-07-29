import os, time, math
from threading import Thread, Semaphore
from collections import deque
# Para instalar o matplotlib: sudo apt-get install python3-matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""Este programa vai mostrar estatísticas dos pacotes que entram e saem da placa de rede no seu computador 
    utilizando um pipeline de threads.  um processo pai cria três processos (threads, T1, T2 e T3) filhos com 
    camunicação entre eles utilizando memória compartilhada. T1 se comunica com T2 através de um buffer B12 
    compartilhado e T2 se comunica com T3 através de outro buffer B23 compartilhado. T1 é responsável por ler os pacotes
     da placa de rede, examinar quantos bytes tem o pacote e se o protocolo é TCP, UDP ou SMTP, e colocar as duas informações 
     no buffer B12 . T2 é responsável por ler o buffer B12 e calcular o número, o tamanho médio e a variância dos 
     pacotes UDP, TCP e SMTP a cada 30 s e colocar estas seis informações no buffer B23. T3 é responsável por ler o 
     buffer B23 e mostrar e atualizar a cada 30 s uma figura na tela com seis gráficos, mostrando a evolução de cada 
     uma destas seis variáveis."""

# Para não precisar de senha com o uso do sudo
# No terminal digita sudo visudo, e altera #Allow membres of group sudo...
# Antes %sudo ALL=(ALL:ALL) ALL, depois %sudo ALL=(ALL:ALL)NOPASSWD:ALL
# Para salvar, ctrl+o e (não salve no arquivo .tmp. salvar em /etc/sudoers)
# Ctrl + x para sair

def thread1(buffer12, semaforo):
    while True:
        pacotes = os.popen("sudo tcpdump -i any -c 1 -v|grep proto").read()
        #print(pacotes)
        if pacotes != "":
            dados = pacotes[pacotes.index("proto"):].split(" ")[1] + " " + pacotes[pacotes.index("proto"):].split(" ")[
                                                                               4][:-2]
            if ("TCP " in dados) or ("UDP" in dados) or ("SMTP" in dados):
                print(dados)
                semaforo.acquire()
                buffer12.append(dados) # add dados em buffer12
                semaforo.release()


# passa uma lista de pacotes como parametro e calcula a média
# sum() soma todos os numeros de uma lista
def medias(lista):
    if len(lista) > 0:
        return sum(lista) / len(lista)
    else:
        #   print("Nenhum pacote")
        return 0


# passa uma lista de pacotes e calcula a variância
# pow(num, expoente)
def variancias(lista):
    somatorio = 0
    media = medias(lista)
    if len(lista) > 0:
        for x in lista:
            somatorio += pow((x - media), 2)
        variancia = somatorio / float(len(lista))
        return variancia
    return 0


def thread2(buffer12, buffer23, semaforo, semaforo2):
    udp = []
    tcp = []  # vetor para guardar tam dos pacotes
    smtp = []

    time.sleep(30)
    while True:
        while len(buffer23) != 0:
            semaforo2.acquire()
            buffer23.popleft()  # esvazia bbuffer23 se n vazio
            semaforo2.release()

        vetor_aux = []
        # vetor recebe dados de buffer12
        while len(buffer12) != 0:
            semaforo.acquire()
            vetor_aux.append(buffer12.popleft())
            semaforo.release()


        # Add apenas o tamanho do pacote em uma lista
        n = 0
        while n < len(vetor_aux):
            aux = vetor_aux[n]
            if "UDP" in aux:
                udp.append(sum([int(x) for x in aux.split(" ")[1:]]))
            elif "TCP" in aux:
                tcp.append(sum([int(x) for x in aux.split(" ")[1:]]))
            elif "SMTP" in aux:
                smtp.append(sum([int(x) for x in aux.split(" ")[1:]]))
            n += 1

        # Adiciona os dados em buffer23
        semaforo2.acquire()
        # Num. Media e variancia de UDP
        buffer23.append(int(len(udp)))
        buffer23.append(int(medias(udp)))
        buffer23.append(int(variancias(udp)))
        # Num. Media e variancia de TCP
        buffer23.append(int(len(tcp)))
        buffer23.append(int(medias(tcp)))
        buffer23.append(int(variancias(tcp)))
        # Num. Media e variancia de SMTP
        buffer23.append(int(len(smtp)))
        buffer23.append(int(medias(smtp)))
        buffer23.append(int(variancias(smtp)))

        semaforo2.release()
        #print(buffer23)

        # Limpa vetores, resultados mais exatos
        udp.clear()
        tcp.clear()
        smtp.clear()


def thread3(buffer23, semaforo2):
    fig = plt.figure()  # inicia uma janela

    # Cria três gráficos
    ax1 = fig.add_subplot(221, axisbg='grey')
    ax2 = fig.add_subplot(222, axisbg='grey')
    ax3 = fig.add_subplot(223, axisbg='grey')

    time.sleep(30)

    y1 = [[0], [0], [0]]
    x1 = [[0], [0], [0]]
    y2 = [[0], [0], [0]]    #lista a serem plotadas
    y3 = [[0], [0], [0]]

    def animate(i):

        teste = []

        while len(buffer23) != 0:
            semaforo2.acquire()
            teste.append(str(buffer23.popleft()))  #conteúdo de buffer está em teste
            semaforo2.release()

        # separar as informações
        num = [teste[0], teste[3], teste[6]]
        med = [teste[1], teste[4], teste[7]]
        var = [teste[2], teste[5], teste[8]]

        print(num)
        print(med)
        print(var)

        # Adicionar as lista de plot e ao mesmo tempo faz um cast para int
        if len(teste) != 0:
            for i in range(3):
                x1[i].append(len(x1[i]))
                y1[i].append(num[i])
                y2[i].append(med[i])
                y3[i].append(var[i])

        ax1.clear()
        ax2.clear()
        ax3.clear()

        #plota os dados nos gráficos
        for j in range(3):
            ax1.plot(x1[j], y1[j], marker="^")
            ax2.plot(x1[j], y2[j], marker="o")
            ax3.plot(x1[j], y3[j], marker="p")

        # Legendas para as informações
        ax1.legend(["num udp", "num tcp", "num smtp"], loc="upper left")
        ax1.set_xlabel("tempo")
        ax1.set_ylabel("Quantidade")

        ax2.legend(["media udp", "media tcp", "media smtp"], loc="upper left")
        ax2.set_xlabel("tempo")
        ax2.set_ylabel("Quantidade")

        ax3.legend(["var udp", "var tcp", "var smtp"], loc="upper left")
        ax3.set_xlabel("tempo")
        ax3.set_ylabel("Quantidade")

    anim = animation.FuncAnimation(fig, animate, interval=30000)
    plt.show()


if __name__ == "__main__":
    # inicia dois buffer circulares tam: 30 e 9
    buffer12 = deque(maxlen=30)
    buffer23 = deque(maxlen=9)

    # semaforos
    smf = Semaphore()
    smf2 = Semaphore()

    print("==============================Antes de iniciar o thread 1==========================================")
    t1 = Thread(target=thread1, args=(buffer12, smf,))
    t1.start()

    time.sleep(20)
    print("===============================Antes de iniciar o thread 2=========================================")
    t2 = Thread(target=thread2, args=(buffer12, buffer23, smf, smf2,))
    t2.start()

    time.sleep(3)
    print("================================Antes de iiciar o thread 3==========================================")
    t3 = Thread(target=thread3, args=(buffer23, smf2,))
    t3.start()