#TODO
#Nomes das cidades e do aviao na tela de criacao de voo

import mysql.connector
from datetime import datetime, timedelta
import PySimpleGUI as sg
import os


def make_win1(): 
    menu_layout = [['Voos', ['Cadastrar novo voo', 'Planilha de voos']],['Informações', ['Avioes', 'Cidades']]]
    
    column = [[sg.Text('Ordernar por', justification='left', size=(10, 1))],      
              [sg.Combo(['ID', 'ID Avião', 'ID Cidade Origem', 'ID Cidade Destino', 'Ano', 'Mês', 'Dia', 'Horario', 'Duração']
                , key='-COMBO-', enable_events=True, default_value='ID'),]
             ]

    layout = [[sg.Menu(menu_layout)],
              [sg.Table(values=listboxContents, headings=headings, max_col_width=25,
                auto_size_columns=True,
                justification='middle',
                num_rows=20,
                alternating_row_color='lightblue',
                key='-TABLE-',
                row_height=35),
                #tooltip='This is a table'),
                sg.Column(column)],
                [sg.Radio('Ordenação Padrão', "-RADIO1-", default=True, size=(15,1), enable_events=True), sg.Radio('Ordenação Reversa', "-RADIO1-", enable_events=True)]
             ]

    return sg.Window("Sistema do aeroporto", layout, finalize=True)
    
def make_win2():
    layout = [[sg.Text('Selecione o dia, mês e ano do voo')],
              [sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(1,32)], key='-DIA-'), 
              sg.Combo([' '+str(num) if num<10 else ' '+str(num) for num in range(1,13)], key='-MES-'),
              sg.Combo([num for num in range(2020, 2030)], key='-ANO-') ],
              [sg.Text('Selecione o ID da aeronave')],
              [sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(1,10)], key='-AERONAVE-')],
              [sg.Text('Selecione o ID da cidade de origem e destino')],
              [sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(1,5)], key='-CIDADEORI-'),
              sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(1,5)], key='-CIDADEDEST-')],
              [sg.Text('Selecione o horário do voo e sua duracao')],
              [sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(24)], key='-HORA-'),
              sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(1,24)], key='-DURACAO-')],
              [sg.Button('Sair'), sg.Button('Criar Voo')]]
    return sg.Window("Marcar Voo", layout, finalize=True)

def criarVoo(aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao):
    """
    Não é possível a inserção não ordenada de um voo.
    Exemplo:

    ___________________________________________________
    | ID  Aviao  CidOri CidDest   Data    Hora Duracao|
    |_________________________________________________|
    | 1     1      1       2   01/01/2020   9    2    |
    | 2     1      2       3   03/01/2020   9    2    |
    |                                                 |
    |_________________________________________________|

    Caso o usuário desejasse inserir um voo no dia 02/01/2020, seria encontrado um problema lógico:
    ->De onde que o usuário iria e pra onde ele iria?
    Se o voo saísse da cidade 2 e fosse para qualquer outra cidade, ele impossibilitaria o voo de ID 2, que precisa do avião na cidade 2 para poder voar.
    Porém não pode haver um voo da mesma cidade para a mesma cidade, então não é possível a inserção não ordenada de voos 
    """
    sql = "SELECT * FROM voo WHERE idAviao = %s ORDER BY id DESC LIMIT 1"
    values = (aviao, )
    mycursor.execute(sql, values)
    myresult = mycursor.fetchall()
    if not myresult:
        #Caso não exista um voo da aeronave requisitada registrado anteriormente, o voo é registrado sem checagens a mais.
        sql = "INSERT INTO voo (idAviao,idCidadeOrigem,idCidadeDestino,ano,mes,dia,horario,duracao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao)
        mycursor.execute(sql, values)
        mydb.commit()
        return(mycursor.rowcount, "Voo inserido.")
    else:
        #Caso exista um voo anterior da aeronave requisitada
        for x in myresult:
            _,_,_,idCidadeDestinoUltimoVoo,anoUltimoVoo,mesUltimoVoo,diaUltimoVoo,horarioUltimoVoo,duracaoUltimoVoo = x
        
        try:
            dataVoo = datetime(year=int(ano), month=int(mes), day =int(dia), hour= int(horaPartida))
        except ValueError:
            return("Data Inválida")

        dataUltimoVoo = datetime(year = anoUltimoVoo, month= mesUltimoVoo, day= diaUltimoVoo, hour= horarioUltimoVoo) + timedelta(hours=duracaoUltimoVoo)

        if dataVoo >= dataUltimoVoo and int(idCidadeOrigem) == idCidadeDestinoUltimoVoo:
            sql = "INSERT INTO voo (idAviao,idCidadeOrigem,idCidadeDestino,ano,mes,dia,horario,duracao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao)
            mycursor.execute(sql, values)
            mydb.commit()
            return("Voo inserido")
        elif dataVoo >= dataUltimoVoo and int(idCidadeOrigem) != idCidadeDestinoUltimoVoo:
            return("Voo impossível, pois o avião não estará na cidade de origem do voo")
        elif dataVoo < dataUltimoVoo and int(idCidadeOrigem) == idCidadeDestinoUltimoVoo:
            return("Voo impossivel, pois o aviao não estará disponível nesta data nem hora")
        else:
            return("Voo impossível, pois o avião não estará disponível nesta data, horário nem localização")

def main():
    SQLColumns =    ['voo.id', 'aviao.nome', 'c1.nome', 'c2.nome', 'voo.ano', "voo.mes", 'voo.dia', 'voo.horario', 'voo.duracao']
    #SQLColumns =    ['id', 'idAviao',  'idCidadeOrigem',   'idCidadeDestino',   'ano', "mes", 'dia', 'horario', 'duracao']
    user_interface= ['ID', 'ID Avião', 'ID Cidade Origem', 'ID Cidade Destino', 'Ano', 'Mês', 'Dia', 'Horario', 'Duração']
    sg.theme('Reddit')
    window1 = make_win1()
    window2 = None
    """
    OldEvents1/2 são variáveis necessárias dado que as janelas estão sendo executadas
    de uma forma asíncrona. Sem eles, a linha:
        'event2, values2 = window2.read(timeout=100)' (Vale o mesmo para a window1)
    Executaria todas as chegagens relacionadas a 'window2' a cada 100ms, o que não é necessário
    caso não exista uma mudança nos eventos dela.
    """
    oldEvents1 = oldEvents2 = None
    #Propósito similar às variaveis acima, só que somente para a window1
    old2Event  = old1Event = None
    while True:
        if window2:
            event2, values2 = window2.read(timeout=100)
            if event2 != oldEvents2:
                oldEvents2 = event2 
                if event2 == sg.WIN_CLOSED or event2 == 'Sair':
                    window2.close()
                    window2 = None
                    continue
                if event2 == 'Criar Voo':
                    if '' in values2.values():
                        sg.popup_no_wait('Dados Faltando')
                    elif values2['-CIDADEORI-'] == values2['-CIDADEDEST-']:
                        sg.popup_no_wait('Rota inválida')
                    else:
                        #mycursor.execute("SELECT * FROM aviao ORDER BY id")
                        #myresult = mycursor.fetchall()
                        string = criarVoo(values2['-AERONAVE-'],values2['-CIDADEORI-'],values2['-CIDADEDEST-']
                                        ,values2['-ANO-'],values2['-MES-'],values2['-DIA-'],values2['-HORA-'],values2['-DURACAO-'])
                        sg.popup_no_wait(f"{string}")
                        if string == "Voo inserido":
                            #'oldEvents1 = None' para que seja atualizada a lista de voos da window1 automaticamente
                            oldEvents1 = None
                            window2.close()
                            window2 = None
                    continue

        event, values = window1.read(timeout=100)
        if event != oldEvents1:
            oldEvents1 = event
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if old1Event:
                old2Event = event
                old1Event = None
            else:
                old1Event = event
            if values['-COMBO-'] in user_interface and old2Event!='Avioes' and old2Event!='Cidades':
                index = user_interface.index(values['-COMBO-'])
                """
                por mais que utilizar uma f string esteja expondo o programa a SQLInjection,
                %s insere aspas simples em strings, impossibilitando a leitura dos dados,
                então a linha abaixo só será executada com comandos válidos (Usando a lista SQLColumns).
                """
                sql = (f"SELECT {', '.join(SQLColumns)} FROM voo "
                        "JOIN aviao ON voo.idAviao = aviao.id "
                        "JOIN cidade as c1 ON voo.idCidadeOrigem = c1.id "
                        "JOIN cidade as c2 ON voo.idCidadeDestino = c2.id "
                        f"ORDER BY {SQLColumns[index]} {'ASC' if values[1]==True else 'DESC' }")
                print(sql)
                mycursor.execute(sql, )
                myresult = mycursor.fetchall()
                window1.Element('-TABLE-').update(myresult)
            if values[0] == 'Cadastrar novo voo':
                window2 = make_win2()
            if values[0] == 'Avioes':
                mycursor.execute(f"SELECT * FROM aviao")
                myresult = mycursor.fetchall()
                window1.Element('-TABLE-').update(myresult)
            if values[0] == 'Cidades':
                mycursor.execute(f"SELECT * FROM cidade")
                myresult = mycursor.fetchall()
                window1.Element('-TABLE-').update(myresult)
            if values[0] == 'Planilha de voos':
                mycursor.execute(f"SELECT * FROM voo ORDER BY id")
                myresult = mycursor.fetchall()
                window1.Element('-TABLE-').update(myresult)

if __name__ == '__main__':
    
    with open('password.txt') as arq:
        password = str(arq.readline())

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="aeroporto"
    )
    #Setup inicial
    mycursor = mydb.cursor()
    sql = "SELECT * FROM voo"
    mycursor.execute(sql, )
    myresult = mycursor.fetchall()
    headings = ['  ID  ', '  Avião  ', ' Cidade Origem  ', ' Cidade Destino ', ' Ano ', ' Mês ', ' Dia ', 'Horario', 'Duração']
    listboxContents = [list(lista) for lista in myresult]

    main()
    
    mycursor.close()
    mydb.close()