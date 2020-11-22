import mysql.connector
import PySimpleGUI as sg
from funcs.criarVoo import criarVoo
from funcs.criarJanelas import make_win1, make_win2, make_win3
from funcs.tableUpdates import tableUpdate, tableUpdateFiltro

def main():
    janelaPrincipal = make_win1(listaVoos, cabecalhos)
    janelaCriacaoVoos = janelaCancelamentoVoos = None

    while True:
        event1, values1 = janelaPrincipal.read(timeout=100)
        if event1 == sg.WIN_CLOSED or event1 == 'Sair':
            break
        if event1 == 'Aplicar Filtro':
            tableUpdateFiltro(SQLCursor=SQLCursor, filtrosInterfaceUsuario=filtrosInterfaceUsuario,
                SQLColumns=SQLColumns, values1=values1, janelaPrincipal=janelaPrincipal)
        if values1[0] == 'Cadastrar novo voo':
            if not janelaCancelamentoVoos:
                tableUpdate(SQLCursor=SQLCursor, SQLQuery=SQLInicial, window=janelaPrincipal)
                janelaCriacaoVoos = make_win2(SQLCursor)
            else:
                sg.popup_no_wait('Feche a janela de cancelamento de voos primeiro')
        if values1[0] == 'Avioes':
            tableUpdate(SQLCursor=SQLCursor, SQLQuery='SELECT * FROM aviao', window=janelaPrincipal)
        if values1[0] == 'Cidades':
            tableUpdate(SQLCursor=SQLCursor, SQLQuery='SELECT * FROM cidade', window=janelaPrincipal)
        if values1[0] == 'Planilha de voos':
            tableUpdate(SQLCursor=SQLCursor, SQLQuery=SQLInicial, window=janelaPrincipal)
        if values1[0] == 'Cancelar voo':
            if not janelaCriacaoVoos:
                tableUpdate(SQLCursor=SQLCursor, SQLQuery=SQLInicial, window=janelaPrincipal)
                SQLCursor.execute('SELECT id FROM voo')
                idsVoos = SQLCursor.fetchall()
                janelaCancelamentoVoos = make_win3([num[0] for num in idsVoos])
            else:
                sg.popup_no_wait('Feche a janela de criação de voos primeiro')

        if janelaCriacaoVoos:
            event2, values2 = janelaCriacaoVoos.read(timeout=100)
            if event2 == sg.WIN_CLOSED or event2 == 'Sair':
                janelaCriacaoVoos.close()
                janelaCriacaoVoos = None
                continue
            if event2 == 'Criar Voo':
                if '' in values2.values():
                    sg.popup_no_wait('Dados Faltando')
                elif values2['-CIDADEORI-'] == values2['-CIDADEDEST-']:
                    sg.popup_no_wait('Rota inválida')
                else:
                    resultadoCriarVoo = str(criarVoo(aeroportoDB, SQLCursor, values2['-AERONAVE-'].split(' ')[0],values2['-CIDADEORI-'].split(' ')[0],
                                    values2['-CIDADEDEST-'].split(' ')[0],values2['-ANO-'],values2['-MES-'],
                                    values2['-DIA-'],values2['-HORA-'],values2['-DURACAO-'], qtdAeronaves, qtdCidades))
                    if resultadoCriarVoo:
                        sg.popup_no_wait(resultadoCriarVoo)
                        if resultadoCriarVoo == 'Voo inserido':
                            janelaCriacaoVoos.close()
                            janelaCriacaoVoos = None
                            tableUpdateFiltro(SQLCursor=SQLCursor, filtrosInterfaceUsuario=filtrosInterfaceUsuario,
                                SQLColumns=SQLColumns, values1=values1, janelaPrincipal=janelaPrincipal)
                continue
        if janelaCancelamentoVoos:
            event3, values3 = janelaCancelamentoVoos.read(timeout=100)
            if event3 == sg.WIN_CLOSED or event3 == 'Sair':
                janelaCancelamentoVoos.close()
                janelaCancelamentoVoos = None
                continue
            if event3 == 'Cancelar Voo':
                if '' in values3.values():
                    sg.popup_no_wait('Dados Faltando')
                else:
                    SQLDeletaVoo = 'DELETE FROM voo WHERE id = %s'
                    vooDeletado = (values3['-IDCANCELA-'], )
                    SQLCursor.execute(SQLDeletaVoo, vooDeletado, )
                    aeroportoDB.commit()
                    if SQLCursor.rowcount == 1:
                        sg.popup_no_wait('Voo cancelado com sucesso!')
                        janelaCancelamentoVoos.close()
                        janelaCancelamentoVoos = None
                        tableUpdateFiltro(SQLCursor=SQLCursor, filtrosInterfaceUsuario=filtrosInterfaceUsuario,
                            SQLColumns=SQLColumns, values1=values1, janelaPrincipal=janelaPrincipal)
                    else:
                        sg.popup_no_wait('Voo inexistente!')


if __name__ == '__main__':
    with open('password.txt') as arq:
        password = str(arq.readline())

    aeroportoDB = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='aeroporto'
    )
#Setup inicial
    SQLCursor = aeroportoDB.cursor()
    sg.theme('Reddit')
    #SQL Queries & Informações da UI
    SQLColumns =             ['voo.id', 'aviao.nome', 'c1.nome'         , 'c2.nome'          , 'voo.ano', 'voo.mes', 'voo.dia', 'voo.horario', 'voo.duracao']
    filtrosInterfaceUsuario= ['ID'    , 'ID Avião'  , 'ID Cidade Origem', 'ID Cidade Destino', 'Ano'    , 'Mês'    , 'Dia'    , 'Horario',     'Duração'    ]
    cabecalhos =             ['  ID  ', '  Avião  ' , ' Cidade Origem  ', ' Cidade Destino ' , ' Ano '  , ' Mês '  , ' Dia '  , 'Horario',      'Duração'   ]
    
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
    main()
    
    SQLCursor.close()
    aeroportoDB.close()