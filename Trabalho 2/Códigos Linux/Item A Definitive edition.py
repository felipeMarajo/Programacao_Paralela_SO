from tkinter import *
import multiprocessing, os, time
from multiprocessing import Pipe

""" O programa mantém duas janelas abertas e o usuário pode digitar um texto em uma das janela que será ecoado
    na outra janela. O programa cria dois processos (utilizando a biblioteca OS)
    com comunicação bidirecional, utilizando pipes"""

def loop(pipe, lb, janela, ed):
    msg = ed.get("1.0",'end-1c')    # msg recebe texto do campo de digitação. "1.0",'end-1c' pega do prim ao ultimo caracter
    pipe.send(msg)                  # O conteúdo de msg é enviado pelo pipe
    if msg =="kill":
        os.waitpid(os.getpid())     # mata o processo ao digitar kill

    msg2 = pipe.recv()              # msg2 recebe o conteúdo que vem por meio de pipe
    if msg2 =="kill":
        os.waitpid(os.getpid())
    lb.config(text=msg2)            # O campo texto de lb é substituido por msg2

    janela.after(100, loop, pipe, lb, janela, ed)   # loop na função (loop)

# Recebe um nome para janela, um pipe que pode ser pipe_in ou pipe_out e as dimensões da janela
def screen(nome, dimensao, pipe):
    print("Process Filho Id: "+str(os.getpid()))  # Mostra os ID's dos processos
    janela = Tk()               # Inicia uma janela
    janela.title(nome)          # Tituo da janela
    janela.geometry(dimensao)   # Dimensões

    titulo = Label(janela, text="DIGITE")   # Label que indinca onde digita
    titulo.pack(side="top")

    ed = Text(janela, width=48, height=3)   # Cria um campo de digitação na janela
    ed.place(x=3, y=20)                     # Posiciona o campo de digitação

    lb = Label(janela, text="", borderwidth=4, relief="ridge")  # Cria um espaço para aparecer os textos
    lb.place(x=5, y=77)         # Posição do label na janela
    lb["height"] = 4            # Altura do label
    lb["width"] = 41            # Largura do label
    lb.config(wraplength=300)   # Margem do texto no label

    # Faz o processo dormir por 0.1 segundos para iniciar o outro
    time.sleep(0.1)
    loop(pipe, lb, janela, ed)  # Chama função loop

    janela.mainloop()   # Loop na janela gráfica

if __name__=="__main__":
    # Pid do Pai
    print("Process Pai Id: " + str(os.getpid()))
    time.sleep(2)

    # Pipes criados
    # True é para habilitar a comunicação bidirecional
    pipe_out, pipe_in = multiprocessing.Pipe(True)

    p1 = os.fork()      # Cria processo filho 1
    if (p1 == 0):
        screen("Processo 1", "350x150+200+200", pipe_in)

    p2 = os.fork()      # Cria processo filho 2
    if (p2 == 0):
        screen("Processo 2", "350x150+600+200", pipe_out)