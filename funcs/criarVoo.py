from datetime import datetime, timedelta

def criarVoo(aeroportoDB, SQLCursor, aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao, qtdAeronaves, qtdCidades):
    """
    Não é possível a inserção não ordenada de um voo de um mesmo avião.
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
        dataVoo = datetime(year=int(ano), month=int(mes), day =int(dia), hour= int(horaPartida))

        if int(horaPartida) < 0 or int(horaPartida) > 24:
            return("Horário de partida inválido")
        elif int(duracao) <= 0:
            return("Duração de voo inválida")
        elif int(aviao) < 0 or int(aviao) > qtdAeronaves:
            return("Avião inválido")
    except ValueError:
        return("Data ou horário Inválido")
    except:
        return("Avião ou horário/duração inválido")

    SQLUltimoVooAviao = "SELECT * FROM voo WHERE idAviao = %s ORDER BY id DESC LIMIT 1"
    SQLInserirVoo = "INSERT INTO voo (idAviao,idCidadeOrigem,idCidadeDestino,ano,mes,dia,horario,duracao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    SQLValues = (aviao, )
    SQLCursor.execute(SQLUltimoVooAviao, SQLValues)
    myresult = SQLCursor.fetchall()

    if not myresult:
        #Caso não exista um voo da aeronave requisitada registrado 
        #anteriormente, o voo é registrado sem a checagem das cidades/horarios
        
        SQLValues = (aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao)
        SQLCursor.execute(SQLInserirVoo, SQLValues)
        aeroportoDB.commit() 
    else:
        #Caso exista um voo anterior da aeronave requisitada
        for x in myresult:
            _,_,_,idCidadeDestinoUltimoVoo,anoUltimoVoo,mesUltimoVoo,diaUltimoVoo,horarioUltimoVoo,duracaoUltimoVoo = x
        dataUltimoVoo = datetime(year = anoUltimoVoo, month= mesUltimoVoo, day= diaUltimoVoo, hour= horarioUltimoVoo) + timedelta(hours=duracaoUltimoVoo)
        if dataVoo >= dataUltimoVoo and int(idCidadeOrigem) == idCidadeDestinoUltimoVoo:
            values = (aviao, idCidadeOrigem, idCidadeDestino, ano, mes, dia, horaPartida, duracao)
            SQLCursor.execute(SQLInserirVoo, values)
            aeroportoDB.commit()
        elif dataVoo >= dataUltimoVoo and int(idCidadeOrigem) != idCidadeDestinoUltimoVoo:
            return("Voo impossível, pois o avião não estará na cidade de origem do voo")
        elif dataVoo < dataUltimoVoo and int(idCidadeOrigem) == idCidadeDestinoUltimoVoo:
            return("Voo impossivel, pois o aviao não estará disponível nesta data nem hora")
        else:
            return("Voo impossível, pois o avião não estará disponível nesta data, horário nem localização")

    if SQLCursor.rowcount == 1:
        return("Voo inserido")
    else:
        return("Erro ao inserir voo")