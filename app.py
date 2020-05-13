import json
from flask import Flask, g, request, jsonify
import fdb

app = Flask(__name__)

con = fdb.connect(
    dsn="C:/VEEV/server/bd/BASE.FDB", user="SYSDBA", password="masterkey"
)

curInsert = con.cursor()


@app.route('/', methods=['POST'])
def home():
    retorno = request.get_json()
    data2 = str(request.get_data(parse_form_data=True)
                ).replace("b'[", "[").replace("]'", "]")
    lista = json.loads(data2)
    idCli = lista[0]['IDCLI']
    nomeCli = lista[0]['NOMECLI']
    seqCli = lista[0]['SEQ']
    listaInsert = [
        (idCli, nomeCli, seqCli)
    ]
    print(listaInsert[0])
    curInsert.execute("INSERT INTO C000000 (CODIGO, TABELA, SEQUENCIA) VALUES(?,?,?)",
                      listaInsert[0]
                      )
    con.commit()
    return jsonify(retorno)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
