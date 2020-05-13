import psutil
import json
from flask import Flask, g, request
import fdb

app = Flask(__name__)


@app.route("/table")
def tablehtml():
    arquivo = open("table.html", "r")
    tabela = arquivo.read
    print(tabela)
    return tabela

@app.route("/login/<usuario>")
def login(usuario):
    g.usuario = usuario
    con = fdb.connect(
        dsn="C:\CLIENTESVEEV.FDB", user="SYSDBA", password="masterkey"
    )
    curlogin = con.cursor()
    usuario = usuario.upper()
    select = "select c.senhamobile from clientesveev c where c.usuariomobile = upper('"+str(usuario)+"') and situacao = '1'"
    curlogin.execute(select)
    json = '[{"SENHAMOBILE":'
    for (SENHAMOBILE) in curlogin:
        result = str(SENHAMOBILE)
        json += result
    json += "}]"
    json = json.replace("('", '"')
    json = json.replace("',)", '"')
    json = json.replace('[{"SENHAMOBILE":}]','[{"SENHAMOBILE":null}]')
    return json,200


@app.route("/clientes")
def home():
    con = fdb.connect(
        dsn="C:/VEEV/server/bd/BASE.FDB", user="SYSDBA", password="masterkey"
    )
    cur = con.cursor()
    select = "select CODIGO, NOME, ENDERECO from C000007"
    json = "["
    cur.execute(select)

    for (CODIGO, NOME, ENDERECO) in cur:

        result = (
            '{"CODIGO":"'
            + str(CODIGO)
            + '","NOME" : "'
            + str(NOME)
            + '","ENDERECO": "'
            + str(ENDERECO)
            + '"},'
        )
        json = json + result

    json = json + "]"
    json = json.replace(",]", "]")

    return json, 200


@app.route("/vendas/<codigonota>")
def vendas(codigonota):
    g.codigonota = codigonota
    venda = codigonota
    con = fdb.connect(
        dsn="C:/VEEV/server/bd/Sandro.FDB", user="SYSDBA", password="masterkey"
    )
    curitens = con.cursor()

    if venda == "*":
        select = """select A.CODIGO, A.DATA, A.CODCLIENTE, A.OBS, A.SITUACAO, a.TOTAL,c.nome
        from C000048 A, C000007 C
        where C.CODIGO = A.CODCLIENTE      order by a.codigo desc"""
    else:
        select = (
            """select A.CODIGO, A.DATA, A.CODCLIENTE, A.OBS, A.SITUACAO, a.toTAL,c.nome
        from C000048 A, C000007 C
        where C.CODIGO = A.CODCLIENTE and   
        A.CODIGO = '"""
            + str(venda)
            + "'"
        )

    json = "["

    cur = con.cursor()

    cur.execute(select)

    for (CODIGO, DATA, CODCLIENTE, OBS, SITUACAO, TOTAL, NOME) in cur:
        DATAN = str(DATA)
        DATAN = DATAN.split("-")
        DATAANO = DATAN[0]
        DATAMES = DATAN[1]
        DATADIA = DATAN[2]
        DATADIA = DATADIA.split(" ")
        DATADIA = DATADIA[0]
        DATANOVA = DATADIA + "/" + DATAMES + "/" + DATAANO
        TOTAL = "R$%.2f" % float(TOTAL)
        TOTAL = TOTAL.replace(".",",")
        result = (
            '{"CODIGO":"'
            + str(CODIGO)
            + '","DATA": "'
            + str(DATANOVA)
            + '","CODCLIENTE" : "'
            + str(CODCLIENTE)
            + '","OBS" : "'
            + str(OBS)
            + '","NOME" : "'
            + str(NOME)
            + '","SITUACAO" : "'
            + str(SITUACAO)
            + '","TOTAL" : "'
            + str(TOTAL)
            + '",'
        )
        json = json + result

        selectitens = (
            """select A.CODIGO, A.CODPRODUTO, C.PRODUTO, A.UNITARIO, A.QTDE, A.TOTAL
            from C000032 A, C000025 C
            where A.CODNOTA = A.NUMERONOTA and
                  C.CODIGO = A.CODPRODUTO and
                  A.CODNOTA in ('"""
            + str(CODIGO)
            + """')
            """
        )
        curitens.execute(selectitens)

        json = json + '"itens" : ['
        for (CODIGO, CODPRODUTO, PRODUTO, UNITARIO, QTDE, TOTAL) in curitens:
            UNITARIO = "R$%.2f" % float(UNITARIO)
            UNITARIO = UNITARIO.replace(".",",")
            QTDE = str(QTDE)
            QTDE = QTDE.replace(".",",")
            resultitens = (
                '{ "CODIGO":"'
                + str(CODIGO)
                + '", "CODPRODUTO":"'
                + str(CODPRODUTO)
                + '", "PRODUTO":"'
                + str(PRODUTO)
                + '", "UNITARIO":"'
                + str(UNITARIO)
                + '", "QTDE":"'
                + str(QTDE)
                + '", "TOTAL":"'
                + str(TOTAL)
                + '" },'
            )
            json = json + resultitens
        json = json + "]},"

    json = json + "]"
    json = json.replace(",]", "]")
    json = json.replace("},}", "}}")
    return json


@app.route("/fluxo")
def fluxo():
    ini = request.args.get('ini', None)
    fin = request.args.get('fin', None)
    print(ini)
    print(fin)
    con = fdb.connect(
        dsn="C:/VEEV/server/bd/sandro.FDB", user="SYSDBA", password="masterkey"
    )
    cur = con.cursor()
    select = """select * from PR_FLUXOCAIXA_RESUMIDO ('"""+str(ini)+""" 00:00:00', '"""+str(fin)+""" 00:00:00')"""
    json = "["
    cur.execute(select)

    for (TIPO, HISTORICO, COMPLEMENTO, VALOR) in cur:

        VALORr = "%.2F" % float(VALOR)

        result = (
            '{"TIPO":"'
            + str(TIPO)
            + '","HISTORICO" : "'
            + str(HISTORICO)
            + '","COMPLEMENTO" : "'
            + str(COMPLEMENTO)
            + '","VALOR" : "'
            + str(VALORr)
            + '"},'
        )
        json = json + result

    json = json + "]"
    json = json.replace(",]", "]")

    return json, 200

@app.route('/acesso')
def acesso():
    cpu = psutil.cpu_percent()
    disc = psutil.disk_usage('C://').percent
    ram = psutil.virtual_memory().percent
    lista = [[cpu, disc, ram]]
    return json.dumps([{"cpu": x, "disk": y, "ram": z}
                       for x, y, z in lista], indent=4)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

