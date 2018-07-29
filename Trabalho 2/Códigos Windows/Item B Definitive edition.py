from tkinter import *
import threading

""" O programa mantém duas janelas abertas e o usuário pode digitar um texto em uma das janela que será ecoado
    na outra janela. O programa cria dois threads com comunicação bidirecional, utilizando variáveis compartilhadas"""

def loop(inp, lb, janela, out, ed, smf1):
    smf1.acquire()                  # Entra na exclusão mutua
    inp[0] = ed.get("1.0",'end-1c') # inp recebe texto do campo de digitação
    smf1.release()                  # Sai da exclusão mutua

    smf1.acquire()      # entra na exclusaõ mutua
    msg = out[0]        # msg recebe o texto de out
    lb.config(text=msg) # (*) Os dados que msg contém são passados o campo de impressão de texto
    smf1.release()

    janela.after(100, loop, inp, lb, janela, out, ed, smf1) # loop na função (loop)

def screen(nome,inp, out, dimension, smf1):
    print(" {}".format(threading.current_thread())) # Mostra os treads criados
    janela = Tk()               # Inicia a janela
    janela.title(nome)          # Titulo da janela
    janela.geometry(dimension)  # Dimensões da janela

    titulo = Label(janela, text="DIGITE")   # Label que indinca onde digita
    titulo.pack(side="top")                 # Local do Label

    ed = Text(janela, width=42, height=3)   # Cria um campo de digitação na janela
    ed.place(x=3, y=20)                     # Posiciona o campo de digitação

    lb = Label(janela, text="", borderwidth=4, relief="ridge")  # (*) Cria um espaço para aparecer os textos
    lb.place(x=5, y=77)  # Local do espaço de texto na janela
    lb["width"] = 47     # Largura do label
    lb["height"] = 4     # Altura do label
    lb.config(wraplength=300)   # Margem do texto no label onde será impresso os textos

    loop(inp, lb, janela, out, ed, smf1)    # Chamada da função

    janela.mainloop()

if __name__=="__main__":
    # Vetores de uma posição para comunicação entre os threads
    in_out = [""]
    out_in = [""]

    # Semaforos (Exclusão mutua)
    smf1 = threading.Semaphore()

    # target diz qual função quero iniciar e args são os argumentos passados para a função
    # smf's são invertidos em t1 e t2, para poder fazer a exclusão mutua, entre ler e escrever
    t1 = threading.Thread(target=screen, args=("Thread 1",in_out, out_in, "350x150+200+200", smf1))
    t2 = threading.Thread(target=screen, args=("Thread 2",out_in, in_out, "350x150+600+200", smf1))

    # Inicia os threads
    t1.start()
    t2.start()
