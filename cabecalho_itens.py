import json
from flask import Flask, g, request, jsonify
import fdb
from datetime import date, datetime

app = Flask(__name__)

con = fdb.connect(
    dsn="C:/VEEV/server/bd/BASE.FDB", user="SYSDBA", password="masterkey"
)

con_ins = fdb.connect(
    dsn="C:/VEEV/server/bd/BASE.FDB", user="SYSDBA", password="masterkey"
)

selectCodigo = con.cursor()
updateCodigo = con_ins.cursor()
selectProdutos = con.cursor()
insertCabecalho = con.cursor()
insertProdutos = con.cursor()


@app.route('/', methods=['POST'])
def home():
    # retorno = request.get_json()
    data = str(request.get_data(parse_form_data=True)
               ).replace("b'[", "[").replace("]'", "]").replace("b'{", "{").replace("}'", "}")

    select = "SELECT SEQUENCIA FROM C000000 WHERE CODIGO = 'COHEAD'"
    update = "UPDATE C000000 SET SEQUENCIA = SEQUENCIA + 1 WHERE CODIGO = 'COHEAD'"
    insert_cabecalho = "insert into COMANDA_CABECALHO (CODIGO, DATA, MESA, STATUS, CODCAIXA, CODVENDEDOR, HORA, ACRESCIMO, TOTAL, HORA_PREPARO,HORA_PRONTO, HORA_DA_ENTREGA) VALUES ("
    insert_itens = "INSERT INTO COMANDA_ITENS (ID, CODIGO, ITEM, CODPRODUTO, PRODUTO, CODBARRAS, numeracao, QTDE, UNITARIO, TOTAL, ACRESCIMO, ALIQUOTA, CST, CODSUBGRUPO, CODGRUPO, PISCOFINS) VALUES (GEN_ID(GEN_COMANDA_ITENS, 1), "

    selectCodigo.execute(select)

    for(SEQ) in selectCodigo:
        codigo = SEQ[0]
        print(codigo)

    updateCodigo.execute(update)
    con_ins.commit()
    comanda = json.loads(data)

    for(SEQ) in selectCodigo:
        codigo = SEQ[0]
        print(codigo)
    now = datetime.now()

    # "CABEÇALHO CAMPOS"
    # data = comanda['DATA']
    data = str(date.today()) + ' 00:00:00'
    mesa = comanda['MESA']
    status = comanda['STATUS']
    codcaixa = comanda['CODCAIXA']
    codvendedor = comanda['CODVENDEDOR']
    # hora = comanda['HORA']
    hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    total = comanda['TOTAL']
    hora_preparo = ''
    hora_pronto = ''
    hora_da_entrega = ''

    cabecalho = [codigo, data, mesa, status, codcaixa, codvendedor,
                 hora, total, hora_preparo, hora_pronto, hora_da_entrega]

    json_itens = comanda['ITENS']

    list_itens = []

    for(i) in json_itens:

        # "ITEM CAMPOS"
        item = i['ITEM']
        codproduto = i['CODPRODUTO']
        produto = i['PRODUTO']
        codbarras = i['CODBARRAS']
        numeracao = i['NUMERACAO']
        qtde = i['QTDE']
        unitario = i['UNITARIO']
        totalp = i['TOTAL']
        acrescimo = i['ACRESCIMO']
        aliquota = i['ALIQUOTA']
        cst = i['CST']
        codsubgrupo = i['CODSUBGRUPO']
        codgrupo = i['CODGRUPO']
        piscofins = i['PISCOFINS']

        item = "'"+str(codigo)+"','"+str(item)+"','"+str(codproduto)+"','"+str(produto)+"','"+str(codbarras)+"',"+str(numeracao)+","+str(qtde)+","+str(
            unitario)+","+str(totalp)+","+str(acrescimo)+","+str(aliquota)+",'"+str(cst)+"','"+str(codsubgrupo)+"','"+str(codgrupo)+"','"+str(piscofins)+"'"
        item = item.replace("'null'", "null").replace("'None'", "null")
        itemi = insert_itens + item + ")"

        insertProdutos.execute(itemi)
        con.commit()

    cabecalhoIComplemento = "'"+str(codigo)+"',"+"'"+str(data)+"','"+str(mesa)+"',"+str(status)+",'"+str(codcaixa)+"',"+"'"+str(
        codvendedor)+"',"+"'"+str(hora)+"',"+str(acrescimo)+","+str(total)+","+"'"+str(hora_preparo)+"',"+"'"+str(hora_pronto)+"',"+"'"+str(hora_da_entrega)+"'"
    cabecalhoIComplemento = cabecalhoIComplemento.replace(
        "'null'", "null").replace("'None'", "null")

    cabecalhoI = insert_cabecalho + cabecalhoIComplemento + ")"

    print(cabecalhoI)
    insertCabecalho.execute(cabecalhoI)
    con.commit()

    return jsonify(codigo)


@app.route('/user', methods=['POST'])
def user():
    data = str(request.get_data(parse_form_data=True)
               ).replace("b'[", "[").replace("]'", "]").replace("b'{", "{").replace("}'", "}")
    data = json.loads(data)
    usuario = data['USER']
    senha = data['PASS']
    selectup = """select C.NOME
            from C000008 C
            where C.NOME = '"""+str(usuario)+"""' and
                  C.SENHA = '"""+str(senha)+"""'"""
    select = """select
       case("""+selectup+""")
         when ("""+selectup+""") then 'true'
         else 'false'
       end as CAMPO
    from C000000
    where CODIGO = '000001'"""
    selectCodigo.execute(select)
    for(r) in selectCodigo:
        t = r[0]
    #t = "true"
    print(t)
    return (t)


@app.route('/produtos')
def produtos():
    select = """select C.CODIGO as CODPRODUTO, C.PRODUTO, C.CODBARRA, C.PRECOVENDA as UNITARIO, C.ALIQUOTA, C.CST, C.CODSUBGRUPO,
       C.CODGRUPO, C.PISCOFINS
    from C000025 C
    """

    jsonTeste = selectProdutos.execute(select).fetchall()
    lista = []
    for (CODPRODUTO, PRODUTO, CODBARRA, UNITARIO, ALIQUOTA, CST, CODSUBGRUPO, CODGRUPO, PISCOFINS) in jsonTeste:
        temp = {
            "CODPRODUTO": CODPRODUTO,
            "PRODUTO": PRODUTO,
            "CODBARRA": CODBARRA,
            "UNITARIO": UNITARIO,
            "ALIQUOTA": ALIQUOTA,
            "CST": CST,
            "CODSUBGRUPO": CODSUBGRUPO,
            "CODGRUPO": CODGRUPO,
            "PISCOFINS": PISCOFINS
        }
        lista.append(temp)
    jsoni = json.dumps(lista)
    return str(jsonTeste)


@app.route('/comandasabertas')
def comandasabertas():
    select = """select C.CODIGO, C.DATA, C.MESA, C.STATUS, C.TOTAL
    from COMANDA_CABECALHO C
    where C.STATUS = 1
    """
    selectProdutos.execute(select)
    json = "["
    for(CODIGO, DATA, MESA, STATUS, TOTAL) in selectProdutos:
        json += '{"CODIGO":"'+str(CODIGO)+'",'
        json += '"DATA":"'+str(DATA)+'",'
        json += '"MESA":"'+str(MESA)+'",'
        json += '"STATUS":'+str(STATUS)+','
        json += '"TOTAL":'+str(TOTAL)+'},'

    json += "]"
    json = json.replace("},]", "}]").replace("None", "null")
    return json


@app.route('/consultarcomanda/<comanda>')
def comanda(comanda):
    g.comanda = comanda
    selectProdComandas = 'select C.ID, C.CODIGO, C.ITEM, C.CODPRODUTO, C.PRODUTO, C.QTDE, C.UNITARIO, C.TOTAL from COMANDA_ITENS C where C.CODIGO = ' + \
        str(comanda)
    selectProdutos.execute(selectProdComandas)
    json = "["
    for(ID, CODIGO, ITEM, CODPRODUTO, PRODUTO, QTDE, UNITARIO, TOTAL) in selectProdutos:
        json += '{"ID":"'+str(ID)+'",'
        json += '"CODIGO":"'+str(CODIGO)+'",'
        json += '"ITEM":"'+str(ITEM)+'",'
        json += '"CODPRODUTO":"'+str(CODPRODUTO)+'",'
        json += '"PRODUTO":"'+str(PRODUTO)+'",'
        json += '"QTDE":'+str(QTDE)+','
        json += '"UNITARIO":'+str(UNITARIO)+','
        json += '"TOTAL":'+str(TOTAL)+'},'
    json = json.replace("},]", "}]").replace("None", "null")
    json += "]"

    return json


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
