auto = open('automated-results.csv','r')
karine = open('resultado_manual_formatado.csv','r')

def separaClassificações(lista):
    retorno = []
    itemMontado = ''
    for i in range(len(lista)):
        if(lista[i] != '[' and lista[i] != ']'):
            if(lista[i] == '|'):
                retorno.append(itemMontado)
                itemMontado = ''
            else:
                itemMontado += lista[i]
    retorno.append(itemMontado)
    return retorno



automaticos = []
manuais = []

for lines in auto:
    val = lines.split(',')[2]
    automaticos.append(val.replace(' ',''))

for lines in karine:
    val = lines.split(',')[2]
    manuais.append(val.replace(' ',''))


# COMPARAÇÃO DA STRING COMPLETA
acertos = 0
for line in range(len(automaticos)):
    if(automaticos[line].strip() == manuais[line].strip()):
        acertos += 1

stringCompleta = acertos/len(automaticos)*100

# COMPARAÇÃO POR SUBCONJUNTO (MANUAIS CONTIDOS EM AUTOMATICOS)
acertos = 0
totalTags = 0
for line in range(len(automaticos)):
    itensAuto = automaticos[line].strip()
    itensManual = manuais[line].strip()
    for i in range(len(itensManual)):
        for j in range(len(itensAuto)):
            if(i == j):
                acertos += 1
        totalTags += 1


print('Taxa de acerto por comparação total: {0:.2f}%'.format(stringCompleta))
print('Taxa de acerto por subconjuntos: {0:.2f}%'.format(acertos/totalTags*100))