# SO 2017.1

### Utilização de threads e processos.

  #### Questão 1
  Queremos um programa que mantém duas janelas de texto abertas e o usuário, ao selecionar uma delas, pode digitar um texto que será ecoado na outra.
  
  * _Item A_ - Escreva esse programa no qual um processo pai cria dois processos filhos com comunicação bidirecional entre eles utilizando pipes. Cada processo filho abre uma janela de texto com um prompt no qual o usuário pode digitar um texto que será recebido e ecoado na outra janela, via pipe, pelo outro processo filho.
  
  * _Item B_ - Repita o exercício utilizando threads que se comunicam utilizando variáveis compartilhadas. A variável deve ter exclusão mútua no acesso.
  
  #### Questão 2
   Programação com threads ou processos podem ser utilizados para estruturar aplicações como pipelines. Neste exercício você vai mostrar estatísticas dos pacotes que entram e saem da placa de rede no seu computador utilizando um pipeline de threads.
   
   Escreva esse programa no qual um processo pai cria três processos (threads, T1, T2 e T3) filhos com camunicação entre eles utilizando memória compartilhada. T1 se comunica com T2 através de um buffer B12 compartilhado e T2 se comunica com T3 através de outro buffer B23 compartilhado. T1 é responsável por ler os pacotes da placa de rede, examinar quantos bytes tem o pacote e se o protocolo é TCP, UDP ou SMTP, e colocar as duas informações no buffer B12 . T2 é responsável por ler o buffer B12 e calcular o número, o tamanho médio e a variância dos pacotes UDP, TCP e SMTP a cada 30 s e colocar estas seis informações no buffer B23. T3 é responsável por ler o buffer B23 e mostrar e atualizar a cada 30 s uma figura na tela com seis gráficos, mostrando a evolução de cada uma destas seis variáveis. Os buffers B12 e B23 devem ser buffers circulares. 
   
   * _Questão 2.1_ - Utilizando threads
   * _Questão 2.2_ - Utilizando Processos
