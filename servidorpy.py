import json
from flask import Flask, g, request, jsonify
import fdb
from datetime import date, datetime

app = Flask(__name__)

bancoDB = ""
pularLinha = """
"""
lineBanco = """[BANCO]
"""
lista = []
banco = []

with open("C:/VEEV/server/ini/com.ini") as file:
    rep = 0
    for line in file:
        lista.append(line)
        if line == lineBanco:
            banco.append(rep+1)
        rep += 1
    bancoDB = str(lista[banco[0]]).replace(pularLinha, "")[8:]


# BASE = "C:/VEEV/server/bd/SANDRO.FDB"
BASE = bancoDB
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
    insert_cabecalho = "insert into COMANDA_CABECALHO (CODIGO, DATA, MESA, STATUS, CODCAIXA, CODVENDEDOR, HORA, ACRESCIMO, TOTAL, HORA_PREPARO,HORA_PRONTO, HORA_DA_ENTREGA) VALUES ("
    insert_itens = "INSERT INTO COMANDA_ITENS (ID, CODIGO, ITEM, CODPRODUTO, PRODUTO, CODBARRAS, numeracao, QTDE, UNITARIO, TOTAL, ACRESCIMO, ALIQUOTA, CST, CODSUBGRUPO, CODGRUPO, PISCOFINS) VALUES ("
    codigo = ""
    iu = 'u'
    comanda = json.loads(data)
    updateInsert = '''select max(codigo) from comanda_cabecalho where
        status = 1 and mesa = ''' + str(comanda['MESA'])
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
    json_itens = comanda['ITENS']
    deletar = comanda['DELETAR']
    itensDel = ""
    for(i) in deletar:
        if(i is not None):
            itensDel += str(i) + ","
    delete = "delete from comanda_itens where id in (" + str(itensDel) + ")"
    delete = delete.replace(""",)""", """)""")
    if(delete != 'delete from comanda_itens where id in ()'):
        insertProdutos.execute(delete)
        con.commit()

    for(i) in json_itens:
        if(i['CODIGO'] == ""):
            # "ITEM CAMPOS"
            idProd = ""
            insertProdutos.execute(
                "select GEN_ID(GEN_TEM_RESTAURANTE, 1) from RDB$DATABASE")
            for (idP) in insertProdutos:
                idProd = idP
            idProd = idProd[0]
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
            adicionaisList = i['ADICIONAIS']
            ingredientesList = i['INGREDIENTES']
            item = str(idProd)+",'"+str(codigo)+"','"+str(item)+"','"+str(codproduto)+"','"+str(produto)+"','"+str(codbarras)+"',"+str(numeracao)+","+str(qtde)+","+str(
                unitario)+","+str(totalp)+","+str(acrescimo)+","+str(aliquota)+",'"+str(cst)+"','"+str(codsubgrupo)+"','"+str(codgrupo)+"','"+str(piscofins)+"'"
            item = item.replace("'null'", "null").replace("'None'", "null")
            itemi = insert_itens + item + ")"
            insertProdutos.execute(itemi)
            con.commit()
            clearING = "DELETE FROM C000147 WHERE ID_ITEM  = " + str(idProd)
            clearADC = "DELETE FROM C000146 WHERE ID_ITEM  = " + str(idProd)
            addING = "INSERT INTO C000147 (CODPEDIDO, ID_ITEM) VALUES ('"
            addADC = "INSERT INTO C000146 (CODADICIONAIS, ID_ITEM) VALUES ('"
            insertProdutos.execute(clearING)
            insertProdutos.execute(clearADC)
            con.commit()
            for(a) in adicionaisList:
                temp = addADC + str(a)+"',"+str(idProd)+")"
                insertProdutos.execute(temp)
                con.commit()
            for(i) in ingredientesList:
                temp = addING + str(i)+"',"+str(idProd)+")"
                insertProdutos.execute(temp)
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
        from COMANDA_ITENS I
        where I.CODIGO = (select max(C.CODIGO)
                        from COMANDA_CABECALHO C
                        where C.STATUS = 1 and
                                C.MESA = """ + str(mesa)+")"
        selectProdutos.execute(select)
        for(TOTAL) in selectProdutos:
            total = TOTAL
        updateCab = "UPDATE COMANDA_CABECALHO SET MESA = '"+str(mesa)+"',DATA = '"+str(
            data)+"',HORA = '"+str(hora)+"',TOTAL = "+str(round(total[0], 2))+" WHERE (CODIGO = '"+str(codigo)+"')"
        insertCabecalho.execute(updateCab)
        con.commit()

    return jsonify(mesa)


@app.route('/user/<usuario>')
def user(usuario):
    g.usuario = usuario
    select = """select C.SENHA, C.CODIGO, C.NOME, C.FUNCAO
            from C000008 C
            where upper(C.NOME) = upper('"""+str(usuario)+"')"
    selectCodigo.execute(select)
    senha = {"SENHA": ""}
    for(SENHA, CODIGO, NOME, FUNCAO) in selectCodigo:
        senha = {
            'SENHA': str(SENHA),
            'CODIGO': CODIGO[0],
            'NOME': NOME[0],
        }
    senha = json.dumps(senha)
    return senha


@app.route('/comandasabertas')
def comandasabertas():
    select = """select C.CODIGO, C.DATA, C.MESA, C.STATUS, C.TOTAL
    from COMANDA_CABECALHO C
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
    selectCOD = '(select max(codigo) from comanda_cabecalho where status = 1 and mesa = ' + str(comanda)+')'
    selectProdComandas = 'select C.ID, C.CODIGO, C.ITEM, C.CODPRODUTO, C.PRODUTO, C.QTDE, C.UNITARIO, C.TOTAL from COMANDA_ITENS C where C.CODIGO = ' + selectCOD
    selectProdutos.execute(selectProdComandas)
    selectProdComandas = '''select C.ID, C.CODIGO, C.ITEM, C.CODPRODUTO,
        C.PRODUTO, C.QTDE, C.UNITARIO, C.TOTAL,(select list(A.CODADICIONAIS,
        ",")from C000146 A where A.ITEM = C.ID) as ADICIONAIS,(select list(
        I.CODINGREDIENTE, ",") from C000147 I where I.ITEM = C.ID)
        as INGREDIENTES from COMANDA_ITENS C where C.CODIGO = ''' + selectCOD

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
    select = 'select codigo,mesa,(select max(item) from comanda_itens where codigo = ' + \
        selectCOD+') from comanda_cabecalho where codigo = ' + selectCOD
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


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
