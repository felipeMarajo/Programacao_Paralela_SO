from tkinter import *
import multiprocessing, os
from multiprocessing import Pipe

""" O programa mantém duas janelas abertas e o usuário pode digitar um texto em uma das janela que será ecoado
    na outra janela. O programa cria dois processos com comunicação bidirecional, utilizando pipes"""

def loop(pipe, lb, janela, ed):
    msg = ed.get("1.0",'end-1c')    # msg recebe o texto do campo de digitação
    pipe.send(msg)                  # O conteúdo de msg é enviado pelo pipe

    msg2 = pipe.recv()              # msg2 recebe o conteúdo que vem por meio de pipe
    lb.config(text=msg2)            # O campo texto de lb é substituido por msg2

    janela.after(100, loop, pipe, lb, janela, ed)   # loop na função (loop)

# Recebe um nome para janela, um pipe que pode ser pipe_in ou pipe_out e as dimensões da janela
def screen(nome, pipe, ondeInicia):
    print("Process ID: " + str(os.getpid()))
    janela = Tk()               # Inicia uma janela
    janela.title(nome)          # Titulo da janela
    janela.geometry(ondeInicia) # Dimensões

    titulo = Label(janela, text="DIGITE")   # Label que indinca onde digita
    titulo.pack(side="top")

    ed = Text(janela, width=42, height=3)   # Cria um campo de digitação na janela
    ed.place(x=3, y=20)                     # Posiciona o campo de digitação

    lb = Label(janela, text="", borderwidth=4, relief="ridge")  # Cria um espaço para aparecer os textos
    lb.place(x=5, y=77)         # Posição do label na janela
    lb["height"] = 4            # Altura do label
    lb["width"] = 47            # Largura do label
    lb.config(wraplength=300)   # Margem do texto no label

    loop(pipe, lb, janela, ed)  # Chamada da função
    #janela.after(100, loop, pipe, lb, janela, ed)   # loop apenas na função (loop) [ Serve apenas para chamar a função]
    janela.mainloop()

if __name__=="__main__":
    #Pid pai
    print("Main Process ID: " + str(os.getpid()))

    # Pipes criados
    # True é para hablitar a comunicação bidirecional
    pipe_out, pipe_in = multiprocessing.Pipe(True)

    # Criando dois processos
    p1 = multiprocessing.Process(target=screen, args=("Processo 1",pipe_in,"350x150+200+200"))   #Processo 1
    p2 = multiprocessing.Process(target=screen, args=("Processo 2",pipe_out,"350x150+600+200"))  #Processo 2

    #Inicia os processos
    p1.start()
    p2.start()

    p1.join()
    p2.join()