import json
from flask import Flask, g, request, jsonify
import fdb
from datetime import date, datetime

app = Flask(__name__)

BASE = "C:/VEEV/server/bd/SANDRO.FDB"
USUARIO_BASE = 'SYSDBA'
SENHA_BASE = 'masterkey'

con = fdb.connect(
    dsn=BASE, user=USUARIO_BASE, password=SENHA_BASE
)

con_ins = fdb.connect(
    dsn=BASE, user=USUARIO_BASE, password=SENHA_BASE
)

selectCodigo = con.cursor()
updateCodigo = con_ins.cursor()
selectProdutos = con.cursor()
selectComandaNum = con.cursor()
insertCabecalho = con.cursor()
insertProdutos = con.cursor()


@app.route('/', methods=['POST'])
def home():
    data = str(request.get_data(parse_form_data=True)
               ).replace("b'[", "[").replace("]'", "]").replace("b'{", "{").replace("}'", "}")
    select = "SELECT SEQUENCIA FROM C000000 WHERE CODIGO = '000143'"
    update = "UPDATE C000000 SET SEQUENCIA = SEQUENCIA + 1 WHERE CODIGO = '000143'"
    insert_cabecalho = "insert into C000143 (CODIGO, DATA, MESA, STATUS, CODCAIXA, CODVENDEDOR, HORA, ACRESCIMO, TOTAL, HORA_PREPARO,HORA_PRONTO, HORA_DA_ENTREGA) VALUES ("
    insert_itens = "INSERT INTO ITENS_RESTAURANTE (ID, CODIGO, ITEM, CODPRODUTO, PRODUTO, CODBARRAS, numeracao, QTDE, UNITARIO, TOTAL, ACRESCIMO, ALIQUOTA, CST, CODSUBGRUPO, PISCOFINS) VALUES (GEN_ID(GEN_TEM_RESTAURANTE, 1), "
    codigo = ""
    iu = 'u'
    comanda = json.loads(data)
    updateInsert = 'select max(codigo) from C000143 where status = 1 and mesa = ' + \
        str(comanda['MESA'])
    updateInsert2 = "select case("+updateInsert+")  when ("+updateInsert+") then (" + \
        updateInsert+") else 'insert' end as CAMPO from C000000 where CODIGO = '000001'"
    selectCodigo.execute(updateInsert2)
    for(CODIGO) in selectCodigo:
        codigo = CODIGO[0]

    if(codigo == 'insert'):
        selectCodigo.execute(select)
        for(SEQ) in selectCodigo:
            codigo = SEQ[0]
        updateCodigo.execute(update)
        con_ins.commit()
        iu = 'i'

    now = datetime.now()

    data = str(date.today()) + ' 00:00:00'
    mesa = comanda['MESA']
    status = comanda['STATUS']
    codcaixa = comanda['CODCAIXA']
    codvendedor = comanda['CODVENDEDOR']
    hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
    total = comanda['TOTAL']
    hora_preparo = ''
    hora_pronto = ''
    hora_da_entrega = ''

    # cabecalho = [codigo, data, mesa, status, codcaixa, codvendedor,
    #              hora, total, hora_preparo, hora_pronto, hora_da_entrega]

    json_itens = comanda['ITENS']

    if(comanda['DELETAR'] != []):
        itensDel = ""
        for(p) in comanda['DELETAR']:
            itensDel += str(p) + ","
        delete = "delete from ITENS_RESTAURANTE where id in (" + str(
            itensDel) + ")"
        delete = delete.replace(""",)""", """)""")
        insertProdutos.execute(delete)
        con.commit()

    for(i) in json_itens:
        if(i['CODIGO'] == ""):
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
                unitario)+","+str(totalp)+","+str(acrescimo)+","+str(aliquota)+",'"+str(cst)+"','"+str(codsubgrupo)+"','"+str(piscofins)+"'"
            item = item.replace("'null'", "null").replace("'None'", "null")
            itemi = insert_itens + item + ")"
            insertProdutos.execute(itemi)
            con.commit()

    if(iu == 'i'):
        cabecalhoIComplemento = "'"+str(codigo)+"',"+"'"+str(data)+"','"+str(mesa)+"',"+str(status)+",'"+str(codcaixa)+"',"+"'"+str(
            codvendedor)+"',"+"'"+str(hora)+"',"+str(acrescimo)+","+str(total)+","+"'"+str(hora_preparo)+"',"+"'"+str(hora_pronto)+"',"+"'"+str(hora_da_entrega)+"'"
        cabecalhoIComplemento = cabecalhoIComplemento.replace(
            "'null'", "null").replace("'None'", "null")
        cabecalhoI = insert_cabecalho + cabecalhoIComplemento + ")"
        insertCabecalho.execute(cabecalhoI)
        con.commit()
    else:
        select = """
        select sum(I.QTDE * I.UNITARIO)
        from ITENS_RESTAURANTE I
        where I.CODIGO = (select max(C.CODIGO)
                        from C000143 C
                        where C.STATUS = 1 and
                                C.MESA = """ + str(mesa)+")"
        selectProdutos.execute(select)
        for(TOTAL) in selectProdutos:
            total = TOTAL
        updateCab = "UPDATE C000143 SET MESA = '"+str(mesa)+"',DATA = '"+str(
            data)+"',HORA = '"+str(hora)+"',TOTAL = "+str(round(total[0], 2))+" WHERE (CODIGO = '"+str(codigo)+"')"
        insertCabecalho.execute(updateCab)
        con.commit()

    return jsonify(mesa)


@app.route('/user/<usuario>')
def user(usuario):
    g.usuario = usuario
    select = """select C.SENHA
            from C000008 C
            where C.NOME = '"""+str(usuario)+"'"
    selectCodigo.execute(select)
    senha = {"SENHA": ""}
    for(SENHA) in selectCodigo:
        senha = {
            'SENHA': SENHA[0]
        }
    senha = json.dumps(senha)
    return senha


@app.route('/comandasabertas')
def comandasabertas():
    select = """select C.CODIGO, C.DATA, C.MESA, C.STATUS, C.TOTAL
    from C000143 C
    where C.STATUS = 1
    """
    selectProdutos.execute(select)
    jsonList = []
    for(CODIGO, DATA, MESA, STATUS, TOTAL) in selectProdutos:
        jsonu = {
            "CODIGO": CODIGO,
            "DATA": str(DATA),
            "MESA": MESA,
            "STATUS": STATUS,
            "TOTAL": TOTAL
        }
        jsonList.append(jsonu)
    jsonList = json.dumps(jsonList)
    return jsonList


@app.route('/consultarcomanda/<comanda>')
def comanda(comanda):
    g.comanda = comanda
    selectCOD = '(select max(codigo) from C000143 where status = 1 and mesa = ' + str(comanda)+')'
    selectProdComandas = 'select C.ID, C.CODIGO, C.ITEM, C.CODPRODUTO, C.PRODUTO, C.QTDE, C.UNITARIO, C.TOTAL from ITENS_RESTAURANTE C where C.CODIGO = ' + selectCOD
    selectProdutos.execute(selectProdComandas)
    jsonComp = []
    jsonList = []
    for(ID, CODIGO, ITEM, CODPRODUTO, PRODUTO, QTDE, UNITARIO, TOTAL) in selectProdutos:
        jsonu = {
            "ID": ID,
            "CODIGO": CODIGO,
            "ITEM": ITEM,
            "CODPRODUTO": CODPRODUTO,
            "PRODUTO": PRODUTO,
            "QTDE": QTDE,
            "UNITARIO": UNITARIO,
            "TOTAL": TOTAL
        }
        jsonList.append(jsonu)
    select = 'select codigo,mesa,(select max(item) from ITENS_RESTAURANTE where codigo = ' + \
        selectCOD+') from C000143 where codigo = ' + selectCOD
    selectProdutos.execute(select)
    for(CODIGO, MESA, ITEM) in selectProdutos:
        jsonC = {
            "CODIGO": CODIGO,
            "MESA": MESA,
            "SEQ_ITEM": ITEM,
            "ITENS": jsonList
        }
        jsonComp.append(jsonC)
    jsonComp = json.dumps(jsonComp)
    return jsonComp


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
    return str(jsoni)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
