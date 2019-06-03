class SPLClassifier:
    
    def __init__(self,added=[],removed=[]):
        self.added = added
        self.removed = removed
    
    def setAdded(self,lista):
        self.added = lista
    
    def setRemoved(self,lista):
        self.removed = lista
    
    def classify(self):
        removed = self.removed
        added = self.added
        result = []

        #Classificação caso só haja remoções no arquivo
        if(len(removed) > 0 and len(added) == 0):
            return self.verifyClass(removed,'Removed')

        #Classificação caso só haja adições no arquivo
        elif(len(added) > 0 and len(removed) == 0):
            return self.verifyClass(added,'Added')

        #Clasificação caso haja possíveis modificações
        else:
            correctLines = 0
            newAdded = []
            newRemoved = []
            newModified = []
            tam,listaLonga,listaCurta = (len(added)-1,added,removed) if len(added) > len(removed) else (len(removed)-1,removed,added)
            for i in range(tam+1):
                j = i
                currentLongo = listaLonga[i]
                foundModify = False
                while(j < len(listaCurta) and not foundModify):
                    currentCurto = listaCurta[j]
                    if(currentCurto[0]+correctLines == currentLongo[0]+correctLines):
                        value = self.verifyClass(currentCurto,'Modify')
                        if(value not in newModified):
                            newModified.append(value)
                        foundModify = True
                    j += 1
                if(not foundModify):
                    if(listaLonga == added):
                        value = self.verifyClass(currentLongo,'Added')
                        if(value not in newAdded):
                            newAdded.append(value)
                        correctLines += 1
                            
                    else:
                        value = self.verifyClass(currentLongo,'Removed')
                        if(value not in newRemoved):
                            newRemoved.append(value)
                        correctLines -= 1
            newAdded.extend(newRemoved)
            newAdded.extend(newModified)
            result = newAdded
            return result
                        

    def verifyClass(self,item, check):
        if(type(item) != list):
            if(check == "Removed"):
                if("menu" in item[1]):
                    return ("Remove","Menu")
                elif("config" in item[1]):
                    return ("Remove","Feature")
                elif("depends" in item[1]):
                    return ("Remove","Depends")
                elif("default" in item[1]):
                    return ("Remove","Default")
                elif("select" in item[1]):
                    return ("Remove","Select")
            elif(check == "Added"):
                if("menu" in item[1]):
                    return ("Added","Menu")
                elif("config" in item[1]):
                    return ("Added","Feature")
                elif("depends" in item[1]):
                    return ("Added","Depends")
                elif("default" in item[1]):
                    return ("Added","Default")
                elif("select" in item[1]):
                    return ("Added","Select")
            else:
                if("menu" in item[1]):
                    return ("Modify","Menu")
                elif("config" in item[1]):
                    return ("Modify","Feature")
                elif("depends" in item[1]):
                    return ("Modify","Depends")
                elif("default" in item[1]):
                    return ("Modify","Default")
                elif("select" in item[1]):
                    return ("Modify","Select")
                
        else:
            result = []
            if(check == 'Added'):
                for line in item:
                    if("menu" in line[1]):
                        partial = ("Added","Menu")
                        if(partial not in result):
                            result.append(partial)
                    elif("config" in line[1]):
                        partial = ("Added","Feature")
                        if(partial not in result):
                            result.append(partial)
                    elif('bool' in line[1] or 'option' in line[1] or 'prompt' in line[1]):
                        partial = ("Modify","Feature")
                        if(partial not in result):
                            result.append(partial)
                    elif("depends" in line[1]):
                        partial = ("Added","Depends")
                        if(partial not in result):
                            result.append(partial)
                    elif("default" in line[1]):
                        partial = ("Added","Default")
                        if(partial not in result):
                            result.append(partial)
                    elif("select" in line[1]):
                        partial = ("Added","Select")
                        if(partial not in result):
                            result.append(partial)
            else:
                for line in item:
                    if("menu" in line[1]):
                        partial = ("Remove","Menu")
                        if(partial not in result):
                            result.append(partial)
                    elif("config" in line[1]):
                        partial = ("Remove","Feature")
                        if(partial not in result):
                            result.append(partial)
                    elif(line[1] in ['bool','option','prompt']):
                        partial = ("Modify","Feature")
                        if(partial not in result):
                            result.append(partial)
                    elif("depends" in line[1]):
                        partial = ("Remove","Depends")
                        if(partial not in result):
                            result.append(partial)
                    elif("default" in line[1]):
                        partial = ("Remove","Default")
                        if(partial not in result):
                            result.append(partial)
                    elif("select" in line[1]):
                        partial = ("Remove","Select")
                        if(partial not in result):
                            result.append(partial)
            return result
                
