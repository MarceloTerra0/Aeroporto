#TODO
#aspas simples ou duplas? ARRUMAR!
import mysql.connector
import PySimpleGUI as sg
from funcoes.criarVoo import criarVoo
from funcoes.criarJanelas import make_win1, make_win2, make_win3

def main():
    window1 = make_win1(tabelaVoosInicial, cabecalhos)
    window2 = window3 = None

    while True:
        event, values = window1.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'Aplicar Filtro':
            index = filtrosInterfaceUsuario.index(values['-COMBO-'])
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
            SQLCursor.execute(sql, )
            myresult = SQLCursor.fetchall()
            window1.Element('-TABLE-').update(myresult)
        if values[0] == 'Cadastrar novo voo':
            window2 = make_win2(SQLCursor)
        if values[0] == 'Avioes':
            SQLCursor.execute("SELECT * FROM aviao")
            myresult = SQLCursor.fetchall()
            window1.Element('-TABLE-').update(myresult)
        if values[0] == 'Cidades':
            SQLCursor.execute("SELECT * FROM cidade")
            myresult = SQLCursor.fetchall()
            window1.Element('-TABLE-').update(myresult)
        if values[0] == 'Planilha de voos':
            SQLCursor.execute(SQLOrderVooId)
            myresult = SQLCursor.fetchall()
            window1.Element('-TABLE-').update(myresult)
        if values[0] == 'Cancelar voo':
            SQLCursor.execute("SELECT id FROM voo")
            myresult = SQLCursor.fetchall()
            window3 = make_win3([num[0] for num in myresult])

        if window2:
            event2, values2 = window2.read(timeout=100)
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
                    string = criarVoo(mydb, SQLCursor, values2['-AERONAVE-'].split(' ')[0],values2['-CIDADEORI-'].split(' ')[0],
                                    values2['-CIDADEDEST-'].split(' ')[0],values2['-ANO-'],values2['-MES-'],
                                    values2['-DIA-'],values2['-HORA-'],values2['-DURACAO-'])
                    sg.popup_no_wait(f"{string}")
                    if string == "Voo inserido":
                        window2.close()
                        window2 = None
                continue

        if window3:
            event3, values3 = window3.read(timeout=100)
            if event3 == sg.WIN_CLOSED or event3 == 'Sair':
                window3.close()
                window3 = None
                continue
            if event3 == 'Cancelar Voo':
                if '' in values3.values():
                    sg.popup_no_wait('Dados Faltando')
                else:
                    SQLDeletaVoo = f'DELETE FROM voo WHERE id = {values3["-IDCANCELA-"]}'
                    SQLCursor.execute(SQLDeletaVoo, )
                    mydb.commit()
                    sg.popup_no_wait('Voo cancelado com sucesso!')
                    window3.close()
                    window3 = None
  
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

    #SQL Queries
    SQLColumns =             ['voo.id', 'aviao.nome', 'c1.nome'         , 'c2.nome'          , 'voo.ano', "voo.mes", 'voo.dia', 'voo.horario', 'voo.duracao']
    filtrosInterfaceUsuario= ['ID'    , 'ID Avião'  , 'ID Cidade Origem', 'ID Cidade Destino', 'Ano'    , 'Mês'    , 'Dia'    , 'Horario',     'Duração'    ]
    cabecalhos =             ['  ID  ', '  Avião  ' , ' Cidade Origem  ', ' Cidade Destino ' , ' Ano '  , ' Mês '  , ' Dia '  , 'Horario',      'Duração'   ]

    sg.theme('Reddit')
    SQLOrderVooId = (f"SELECT {', '.join(SQLColumns)} FROM voo "
                    "JOIN aviao ON voo.idAviao = aviao.id "
                    "JOIN cidade as c1 ON voo.idCidadeOrigem = c1.id "
                    "JOIN cidade as c2 ON voo.idCidadeDestino = c2.id "
                    "ORDER BY voo.id ASC")

    SQLCursor = mydb.cursor()
    SQLAvioes = 'SELECT * FROM aviao'
    SQLCursor.execute(SQLAvioes, )
    aeronavesResult = SQLCursor.fetchall()
    qtdAeronaves = len(aeronavesResult)

    sqlCidades = 'SELECT * FROM cidade'
    SQLCursor.execute(sqlCidades, )
    cidadesResult = SQLCursor.fetchall()
    qtdCidades = len(cidadesResult)

    SQLInicial = (f"SELECT {', '.join(SQLColumns)} FROM voo "
                    "JOIN aviao ON voo.idAviao = aviao.id "
                    "JOIN cidade as c1 ON voo.idCidadeOrigem = c1.id "
                    "JOIN cidade as c2 ON voo.idCidadeDestino = c2.id "
                    "ORDER BY voo.id ASC")
    SQLCursor.execute(SQLInicial, )
    listaVoos = SQLCursor.fetchall()
    tabelaVoosInicial = [list(voo) for voo in listaVoos]
    main()
    
    SQLCursor.close()
    mydb.close()