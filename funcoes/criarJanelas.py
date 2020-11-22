import PySimpleGUI as sg

def make_win1(tabelaVoosInicial, cabecalhos): 
    menu_layout = [['Voos', ['Cadastrar novo voo', 'Planilha de voos', 'Cancelar voo']],['Informações', ['Avioes', 'Cidades']]]
    
    column = [[sg.Text('Ordernar por', justification='left', size=(10, 1))],      
              [sg.Combo(['ID', 'ID Avião', 'ID Cidade Origem', 'ID Cidade Destino', 'Ano', 'Mês', 'Dia', 'Horario', 'Duração']
                , key='-COMBO-', default_value='ID'),]
             ]

    layout = [ [sg.Menu(menu_layout)],
               [sg.Table(values=tabelaVoosInicial, headings=cabecalhos, max_col_width=25,
                    auto_size_columns=True,
                    justification='middle',
                    num_rows=20,
                    alternating_row_color='#5ea0d1',
                    key='-TABLE-',
                    row_height=35),
                    sg.Column(column)],
                [sg.Radio('Ordenação Padrão', "-RADIO1-", default=True, size=(15,1)), sg.Radio('Ordenação Reversa', "-RADIO1-", enable_events=True)],
                [sg.Button('Aplicar Filtro'), sg.Button('Sair')]
             ]

    return sg.Window("Sistema do aeroporto", layout, finalize=True)
    
def make_win2(SQLCursor):
    SQLAvioesTotais = 'SELECT nome FROM aviao'
    SQLCursor.execute(SQLAvioesTotais)
    avioesTotais = SQLCursor.fetchall()
    avioesTotais = [f'{i} - {nome[0]}' for i,nome in enumerate(avioesTotais, start=1)]
    SQLCidadesTotais = 'SELECT nome FROM cidade'
    SQLCursor.execute(SQLCidadesTotais)
    cidadesTotais = SQLCursor.fetchall()
    cidadesTotais = [f'{i} - {nome[0]}' for i,nome in enumerate(cidadesTotais, start=1)]
    print(cidadesTotais)
    layout = [[sg.Text('Selecione o dia, mês e ano do voo')],
              [sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(1,32)], key='-DIA-'), 
              sg.Combo([' '+str(num) if num<10 else ' '+str(num) for num in range(1,13)], key='-MES-'),
              sg.Combo([num for num in range(2020, 2030)], key='-ANO-') ],
              [sg.Text('Selecione o ID da aeronave')],
              [sg.Combo([aviao for aviao in avioesTotais], key='-AERONAVE-')],
              [sg.Text('Selecione o ID da cidade de origem e destino')],
              [sg.Combo([cidade for cidade in cidadesTotais], key='-CIDADEORI-'),
              sg.Combo([cidade for cidade in cidadesTotais], key='-CIDADEDEST-')],
              [sg.Text('Selecione o horário do voo e sua duracao')],
              [sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(24)], key='-HORA-'),
              sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in range(1,24)], key='-DURACAO-')],
              [sg.Button('Sair'), sg.Button('Criar Voo')]]
    return sg.Window("Marcar Voo", layout, finalize=True)

def make_win3(qtdVoos):
    layout = [[sg.Text('Selecione o ID do voo a ser cancelado')],
              [sg.Combo(['  '+str(num) if num<10 else ' '+str(num) for num in qtdVoos], key = '-IDCANCELA-')],
              [sg.Button('Sair'), sg.Button('Cancelar Voo')]]
    return sg.Window("Cancelar Voo", layout, finalize=True)