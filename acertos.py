auto = open('automated-results.csv','r')
karine = open('resultado_manual_formatado.csv','r')

automaticos = []
manuais = []
acertos = 0

for lines in auto:
    val = lines.split(',')[2]
    automaticos.append(val.replace(' ',''))

for lines in karine:
    val = lines.split(',')[2]
    manuais.append(val.replace(' ',''))

for line in range(len(automaticos)):
    
    if(automaticos[line].strip() == manuais[line].strip()):
        acertos += 1
    else:
        if(line == 3):
            print("SOU DIFERENTE")
            print(automaticos[line].strip())
            print(manuais[line].strip())


print('Taxa de acerto: {0:.2f}%'.format(acertos/len(automaticos)*100))