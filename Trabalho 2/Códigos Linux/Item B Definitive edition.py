from tkinter import *
import threading, os

""" O programa mantém duas janelas abertas e o usuário pode digitar um texto em uma das janela que será ecoado
    na outra janela. O programa cria dois threads com comunicação bidirecional, utilizando variáveis compartilhadas"""

# Função para encerrar os threads e o processo
def kill_threads():
    os.popen("pkill python")

# Função para receber e enviar dados para outro thread
def loop(inp, lb, janela, out, ed, smf):
    smf.acquire()                   # Entra na exclusão mútua
    inp[0] = ed.get("1.0",'end-1c') # inp recebe texto do campo de digitação
    smf.release()

    smf.acquire()
    msg = out[0]        # msg recebe o texto de out
    lb.config(text=msg) # (*) Os dados que msg contém são passados o campo de impressão de texto
    smf.release()       # Sai da exclusão mútua

    janela.after(100, loop, inp, lb, janela, out, ed, smf) # loop na função (loop), Atraso de 100ms

# Função que cria os componentes das telas de cada thread
def screen(nome,inp, out, dimension, smf):
    print(" {}".format(threading.current_thread())) # Mostra os treads criados
    janela = Tk()               # Inicia a janela
    janela.title(nome)          # Titulo da janela
    janela.geometry(dimension)  # Dimensões da janela

    titulo = Label(janela, text="DIGITE")   # Label que indinca onde digita
    titulo.pack(side="top")                 # Local do Label

    ed = Text(janela, width=48, height=3)   # Cria um campo de digitação na janela
    ed.place(x=3, y=20)                     # Posiciona o campo de digitação

    lb = Label(janela, text="", borderwidth=4, relief="ridge")  # (*) Cria um espaço para aparecer os textos
    lb.place(x=5, y=77)  # Local do espaço de texto na janela
    lb["width"] = 41     # Largura do label
    lb["height"] = 4     # Altura do label
    lb.config(wraplength=300)   # Margem do texto no label onde será impresso os textos

    # Cria um botão para matar os theads, usando a função kill_threads como comando
    button = Button(janela, text="Kill Threads", command=kill_threads)
    button.place(x=120, y=150)  # Posiciona o Botão

    loop(inp, lb, janela, out, ed, smf)    # Chamada da função

    janela.mainloop()   # Loop apena na janela gráfica

if __name__=="__main__":
    print("Process Id: " + str(os.getpid()))
    # Vetores de uma posição para comunicação entre os threads
    in_out = [""]
    out_in = [""]

    # Semaforos (Exclusão mutua)
    smf = threading.Semaphore()

    # target diz qual função quero iniciar e args são os argumentos passados para a função
    t1 = threading.Thread(target=screen, args=("Thread 1",in_out, out_in, "350x190+200+200", smf))
    t2 = threading.Thread(target=screen, args=("Thread 2",out_in, in_out, "350x190+600+200", smf))

    # Inicia os threads
    t1.start()
    t2.start()
