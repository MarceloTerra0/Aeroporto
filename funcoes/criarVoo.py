from datetime import datetime, timedelta

def criarVoo(mydb, SQLCursor, aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao):
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
    try:
        if 0 > int(horaPartida) > 24:
            return("Horário de partida inválido")
        elif int(duracao) <= 0:
            return("Duração de voo inválida")
    except:
        return("Valor(es) de horário inválido(s)")
    sql = "SELECT * FROM voo WHERE idAviao = %s ORDER BY id DESC LIMIT 1"
    SQLValues = (aviao, )
    SQLCursor.execute(sql, SQLValues)
    myresult = SQLCursor.fetchall()
    SQLInserirVoo = "INSERT INTO voo (idAviao,idCidadeOrigem,idCidadeDestino,ano,mes,dia,horario,duracao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    if not myresult:
        #Caso não exista um voo da aeronave requisitada registrado anteriormente, o voo é registrado sem checagens a mais.
        SQLValues = (aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao)
        SQLCursor.execute(SQLInserirVoo, SQLValues)
        mydb.commit()
        return(SQLCursor.rowcount, "Voo inserido.")
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
            values = (aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao)
            SQLCursor.execute(SQLInserirVoo, values)
            mydb.commit()
            return("Voo inserido")
        elif dataVoo >= dataUltimoVoo and int(idCidadeOrigem) != idCidadeDestinoUltimoVoo:
            return("Voo impossível, pois o avião não estará na cidade de origem do voo")
        elif dataVoo < dataUltimoVoo and int(idCidadeOrigem) == idCidadeDestinoUltimoVoo:
            return("Voo impossivel, pois o aviao não estará disponível nesta data nem hora")
        else:
            return("Voo impossível, pois o avião não estará disponível nesta data, horário nem localização")