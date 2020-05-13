import math
dicts = []

for c in range(123):
    temp = {
        "LETRA": chr(c),
        "SEQUENCIA": c,
    }
    dicts.append(temp)
texto = "pao com salame e feijoada"
texto = "python is the best langs2"
textLen = len(texto)
index = 0
listTexto = []
listEncode = []
while(index < textLen):
    temp = texto[index]
    listTexto.append(temp)
    index += 1
for(LETRA) in listTexto:
    indexListTexto = 0
    for(LETRADICT) in dicts:
        temp = LETRADICT['LETRA']
        if(LETRA == temp):
            seq = indexListTexto
            if(seq > 32):
                seq = seq-32
            listEncode.append(dicts[seq]["SEQUENCIA"])
        indexListTexto += 1
tamMatriz = 5
qtd = len(listEncode)
qtdN = math.floor(qtd/tamMatriz)
resto = qtd - (qtdN*tamMatriz)
soma = 0
matrizA = []
while(qtdN > 0):
    itens = []
    seqList = 0
    while(seqList < tamMatriz):
        itens.append(listEncode[seqList+soma])
        seqList += 1
    soma += tamMatriz
    qtdN -= 1
    matrizA.append(itens)
print(matrizA)
matrizA = [[67, 43, 43, 32, 69],
           [32, 77, 85, 73, 84],
           [79, 32, 70, 73, 76],
           [72, 65, 32, 68, 65],
           [32, 80, 85, 84, 65]]

print(matrizA)
matrizB = [[1, 0, 1, 3, 2],
           [-1, 3, 1, 2, 0],
           [0, 1, 1, 1, 1],
           [0, 1, 1, 0, 1],
           [0, 1, 1, 3, 2]]
inversoMatrizB = [[2, 1, -5, 3, -1],
                  [1, 1, -5, 3, 0],
                  [-1, -1, 8, -4, -1],
                  [0, 0, 1, -1, 0],
                  [0, 0, -3, 2, 1]]
result = [[0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0]]
result2 = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]
for i in range(len(matrizA)):
    for j in range(len(matrizB[0])):
        for k in range(len(matrizB)):
            result[i][j] += matrizA[i][k] * matrizB[k][j]
for i in range(len(result)):
    for j in range(len(inversoMatrizB[0])):
        for k in range(len(inversoMatrizB)):
            result2[i][j] += result[i][k] * inversoMatrizB[k][j]
print("")
print("Mensagem codificada: ")
for r in result:
    print(r)
print("")
print("Mensagem decodificada: ")
for r in result2:
    print(r)
listaFinal = []
for(i) in result2:
    for(i2) in i:
        listaFinal.append(i2)
stringFinal = ""
print(listaFinal)
for(LETRA) in listaFinal:
    if(LETRA > 32):
        stringFinal += dicts[LETRA+32]["LETRA"]
    else:
        stringFinal += dicts[LETRA]["LETRA"]
print("")
print("Mensagem decodificada: ")
print(stringFinal)
