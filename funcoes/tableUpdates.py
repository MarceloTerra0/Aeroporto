def tableUpdate(SQLCursor,SQLQuery, window):
    SQLCursor.execute(SQLQuery, )
    resultado = SQLCursor.fetchall()
    window.Element('-TABLE-').update(resultado)

def tableUpdateFiltro(SQLCursor, filtrosInterfaceUsuario, SQLColumns, values1, janelaPrincipal):
    index = filtrosInterfaceUsuario.index(values1['-COMBO-'])
    """
    por mais que utilizar uma f string esteja expondo o programa a SQLInjection,
    %s insere aspas simples em strings, impossibilitando a leitura dos dados,
    então a linha abaixo só será executada com comandos válidos (Usando a lista SQLColumns).
    """
    SQLOrderFiltro = (f"SELECT {', '.join(SQLColumns)} FROM voo "
            "JOIN aviao ON voo.idAviao = aviao.id "
            "JOIN cidade as c1 ON voo.idCidadeOrigem = c1.id "
            "JOIN cidade as c2 ON voo.idCidadeDestino = c2.id "
            f"ORDER BY {SQLColumns[index]} {'ASC' if values1[1]==True else 'DESC' }")
    tableUpdate(SQLCursor=SQLCursor, SQLQuery=SQLOrderFiltro, window=janelaPrincipal)
