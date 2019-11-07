import re

class SPLClassifier:
    
    def __init__(self,added=[],removed=[],source_code=None):
        self.added = added
        self.removed = removed
        self.source_code = source_code
    
    def setAdded(self,lista):
        self.added = lista
    
    def setRemoved(self,lista):
        self.removed = lista
    
    def classify(self, file_type, features):
        removed = self.removed
        added = self.added
        # print(removed, added)
        result = []

        #Classificação caso só haja remoções no arquivo
        if(len(removed) > 0 and len(added) == 0):
            if('kconfig' in file_type):
                return self.kconfigClass(removed,'Removed')
            elif('makefile' in file_type):
                return self.classifyMakefile(removed,'Removed',features)
            else:
                return self.classifyAM(removed, 'Removed')

        #Classificação caso só haja adições no arquivo
        elif(len(added) > 0 and len(removed) == 0):
            if('kconfig' in file_type):
                return self.kconfigClass(added,'Added')
            elif('makefile' in file_type):
                return self.classifyMakefile(added,'Added',features)
            else:
                return self.classifyAM(removed, 'Added')

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
                while(j <= len(listaCurta) and not foundModify):
                    if(j < len(listaCurta)):
                        currentCurto = listaCurta[j]
                    else:
                        currentCurto = listaCurta[j-1]
                    if(((currentCurto[0]+correctLines == currentLongo[0]) or (currentCurto[1] == currentLongo[1])) and currentCurto[1] != ''):
                        if('kconfig' in file_type):
                            value = self.kconfigClass(currentCurto,'Modify', currentLongo)
                        elif('makefile' in file_type):
                            value = self.classifyMakefile(currentCurto,'Modify',features)
                        else:
                            value = self.classifyAM(currentCurto, 'Modify')
                        if(value not in newModified):
                            newModified.append(value)
                        foundModify = True
                    j += 1
                if(not foundModify and currentLongo[1] != ''):
                    if(listaLonga == added):
                        if('kconfig' in file_type):
                            value = self.kconfigClass(currentLongo,'Added')
                        elif('makefile' in file_type):
                            value = self.classifyMakefile(currentLongo,'Added',features)
                        else:
                            value = self.classifyAM(currentLongo, 'Added')
                        if(value not in newAdded):
                            newAdded.append(value)
                        correctLines += 1
                            
                    else:
                        if('kconfig' in file_type):
                            value = self.kconfigClass(currentLongo,'Removed')
                        elif('makefile' in file_type):
                            value = self.classifyMakefile(currentLongo,'Removed',features)
                        else:
                            value = self.classifyAM(currentLongo, 'Removed')
                        if(value not in newRemoved):
                            newRemoved.append(value)
                        correctLines -= 1
            newAdded.extend(newRemoved)
            newAdded.extend(newModified)
            result = newAdded
            result = [i for i in result if(i != None)]
            return result
                        

    def kconfigClass(self,item, check, before=False):
        if(type(item) != list):
            item = (item[0], item[1].strip())
            if(check == "Removed"):
                if(re.match(r'^menu \"w+\"', item[1]) != None):
                    return ("Remove","Menu")
                elif(re.match(r'^config \S+', item[1]) != None):
                    return ("Remove","Feature")
                elif((re.match(r'^bool \"w+\"', item[1]) != None) or (re.match(r'^option \"w+\"', item[1]) != None) or (re.match(r'^prompt \"w+\"', item[1]) != None)):
                    return ("Modify","Feature")
                elif(re.match(r'^depends on \S+', item[1]) != None):
                    return ("Remove","Depends")
                elif(re.match(r'^default \S', item[1]) != None):
                    return ("Remove","Default")
                elif(re.match(r'^select \S+', item[1]) != None):
                    return ("Remove","Select")
            elif(check == "Added"):
                if(re.match(r'^menu \"w+\"', item[1]) != None):
                    return ("Added","Menu")
                elif(re.match(r'^config \S+', item[1]) != None):
                    return ("Added","Feature")
                elif(re.match(r'^depends on \S+', item[1]) != None):
                    return ("New","Depends")
                elif(re.match(r'^default \S', item[1]) != None):
                    if("if" in item[1]):
                        return ("Added","Default") # Possiveis = New, Added Remove, Modify OBS: Added para "if" - New sem "if"
                    else:
                        return ("New", "Default")
                elif(re.match(r'^select \S+', item[1]) != None):
                    # Verificar se é new ou added
                    # return("New", "Select")
                    if(re.match(r'^select \S+', self.source_code[item[0]-2]) != None):
                        return ("Added","Select") # Possiveis = New, Added, Remove e Modify OBS: Added para Anterior havendo select
                                                #                                              New se não houver select antes
                    else:
                        return ("New","Select")

            else:
                # MUDAR DEFAULT PRA "\S+" E USAR STRIP DO JEITO COMO ESTÁ AQUI EM CIMA PARA REGEX FUNCIONAR
                if(re.match(r'^menu \"w+\"', item[1]) != None):
                    return ("Modify","Menu")
                elif(re.match(r'^config \S+', item[1]) != None):
                    return ("Modify","Feature")
                elif((re.match(r'^bool \"w+\"', item[1]) != None) or (re.match(r'^option \"w+\"', item[1]) != None) or (re.match(r'^prompt \"w+\"', item[1]) != None)):
                    return ("Modify","Feature")
                elif(re.match(r'^depends on \S+', item[1]) != None):
                    before = before[1].replace('\t', '')
                    if(item[1].count('&&') > before.count('&&')):
                        return ("Added","Depends") # Possiveis = New, Added, Remove e Modify OBS: Added && para junção - New sem &&
                    elif(item[1].count('&&') < before.count('&&')):
                        return("Remove", "Depends")
                    else:
                        return ("Modify","Depends")
                elif(re.match(r'^default \S', item[1]) != None):
                    return ("Modify","Default")
                elif(re.match(r'^select \S+', item[1]) != None):
                    return ("Modify","Select")
                
        else:
            result = []
            if(check == 'Added'):
                for line in item:
                    line = (line[0], line[1].strip())
                    if(re.match(r'^menu \"w+\"', line[1]) != None):
                        partial = ("Added","Menu")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^config \S+', line[1]) != None):
                        partial = ("Added","Feature")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^depends on \S+', line[1]) != None):
                        if("&&" in line[1]):
                            partial = ("Added","Depends")
                            if(partial not in result):
                                result.append(partial) # Possiveis = New, Added, Remove e Modify OBS: Added && para junção - New sem &&
                        else:
                            partial = ("New","Depends")
                            if(partial not in result):
                                result.append(partial)
                    elif(re.match(r'^default \S', line[1]) != None):
                        if("if" in line[1]):
                            partial = ("Added","Default")
                            if(partial not in result):
                                result.append(partial) # Possiveis = New, Added Remove, Modify OBS: Added para "if" - New sem "if"
                        else:
                            partial = ("New","Default")
                            if(partial not in result):
                                result.append(partial)
                    elif(re.match(r'^select \S+', line[1]) != None):
                        # Verificar se é new ou added
                        # return("New", "Select")
                        if(re.match(r'^select \S+', self.source_code[line[0]-2]) != None):
                            partial = ("Added","Select")
                            if(partial not in result):
                                result.append(partial) # Possiveis = New, Added, Remove e Modify OBS: Added para Anterior havendo select
                                                #                                              New se não houver select antes
                        else:
                            partial = ("New","Select")
                            if(partial not in result):
                                result.append(partial)
            else:
                for line in item:
                    line = (line[0], line[1].strip())
                    if(re.match(r'^menu \"w+\"', line[1]) != None):
                        partial = ("Remove","Menu")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^config \S+', line[1]) != None):
                        partial = ("Remove","Feature")
                        if(partial not in result):
                            result.append(partial)
                    elif((re.match(r'^bool \"w+\"', line[1]) != None) or (re.match(r'^option \"w+\"', line[1]) != None) or (re.match(r'^prompt \"w+\"', line[1]) != None)):
                        partial = ("Modify","Feature")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^depends on \S+', line[1]) != None):
                        partial = ("Remove","Depends")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^default \S', line[1]) != None):
                        partial = ("Remove","Default")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^default \S', line[1]) != None):
                        partial = ("Remove","Select")
                        if(partial not in result):
                            result.append(partial)
            return result

    def classifyMakefile(self, item, check, features):
        if(type(item) != list):
            item = (item[0], item[1].strip())
            if(check == "Removed"):
                res1 = re.search(r'^\S*\$\((.*)\)\S* := \S*', item[1])
                res2 = re.search(r'^\S*\$\((.*)\)\S* \+= \S*', item[1])
                if((res1 != None and res1.group(1) in features) or (res2 != None and res2.group(1) in features)):
                    return ("Remove","Mapping")
                elif(re.match(r'^ifeq \S*', item[1]) != None or re.match(r'^ifneq \S*', item[1]) != None or re.match(r'^ifdef \S*', item[1]) != None):
                    return ("Remove","ifdef")
                else:
                    return ("Remove","build")
            elif(check == "Added"):
                res1 = re.search(r'^\S*\$\((.*)\)\S* := \S*', item[1])
                res2 = re.search(r'^\S*\$\((.*)\)\S* \+= \S*', item[1])
                if((res1 != None and res1.group(1) in features) or (res2 != None and res2.group(1) in features)):
                    return ("Added","Mapping")
                elif(re.match(r'^ifeq \S*', item[1]) != None or re.match(r'^ifneq \S*', item[1]) != None or re.match(r'^ifdef \S*', item[1]) != None):
                    return ("Added","ifdef")
                else:
                    return ("Added","build")

            else:
                res1 = re.search(r'^\S*\$\((.*)\)\S* := \S*', item[1])
                res2 = re.search(r'^\S*\$\((.*)\)\S* \+= \S*', item[1])
                if((res1 != None and res1.group(1) in features) or (res2 != None and res2.group(1) in features)):
                    return ("Modify","Mapping")
                elif(re.match(r'^ifeq \S*', item[1]) != None or re.match(r'^ifneq \S*', item[1]) != None or re.match(r'^ifdef \S*', item[1]) != None):
                    return ("Modify","ifdef")
                else:
                    return ("Modify","build")
                
        else:
            result = []
            if(check == 'Added'):
                for line in item:
                    line = (line[0], line[1].strip())
                    res1 = re.search(r'^\S*\$\((.*)\)\S* := \S*', line[1])
                    res2 = re.search(r'^\S*\$\((.*)\)\S* \+= \S*', line[1])
                    if((res1 != None and res1.group(1) in features) or (res2 != None and res2.group(1) in features)):
                        partial = ("Added","Mapping")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^ifeq \S*', line[1]) != None or re.match(r'^ifneq \S*', line[1]) != None or re.match(r'^ifdef \S*', line[1]) != None):
                        partial = ("Added","ifdef")
                        if(partial not in result):
                            result.append(partial)
                    else:
                        if(line[1] != ''):
                            partial = ("Added","build")
                            if(partial not in result):
                                result.append(partial)
            else:
                for line in item:
                    line = (line[0], line[1].strip())
                    res1 = re.search(r'^\S*\$\((.*)\)\S* := \S*', line[1])
                    res2 = re.search(r'^\S*\$\((.*)\)\S* \+= \S*', line[1])
                    if((res1 != None and res1.group(1) in features) or (res2 != None and res2.group(1) in features)):
                        partial = ("Remove","Mapping")
                        if(partial not in result):
                            result.append(partial)
                    elif(re.match(r'^ifeq \S*', line[1]) != None or re.match(r'^ifneq \S*', line[1]) != None or re.match(r'^ifdef \S*', line[1]) != None):
                        partial = ("Remove","ifdef")
                        if(partial not in result):
                            result.append(partial)
                    else:
                        partial = ("Remove","build")
                        if(partial not in result):
                            result.append(partial)
            return result
    
    def classifyAM(self, item, check):
        if(type(item) != list):
            item = (item[0], item[1].strip())
            if(check == "Removed"):
                if(re.match(r'^#ifeq \S*', item[1]) != None or re.match(r'^#ifneq \S*', item[1]) != None or re.match(r'^#ifdef \S*', item[1]) != None):
                    return ("Remove","ifdef")
                    
            elif(check == "Added"):
                if(re.match(r'^#ifeq \S*', item[1]) != None or re.match(r'^#ifneq \S*', item[1]) != None or re.match(r'^#ifdef \S*', item[1]) != None):
                    return ("Added","ifdef")

            else:
                if(re.match(r'^#ifeq \S*', item[1]) != None or re.match(r'^#ifneq \S*', item[1]) != None or re.match(r'^#ifdef \S*', item[1]) != None):
                    return ("Modify","ifdef")
                
        else:
            result = []
            if(check == 'Added'):
                for line in item:
                    if(re.match(r'^#ifeq \S*', line[1]) != None or re.match(r'^#ifneq \S*', line[1]) != None or re.match(r'^#ifdef \S*', line[1]) != None):
                        partial = ("Added","ifdef")
                        if(partial not in result):
                            result.append(partial)
            else:
                for line in item:
                    if(re.match(r'^#ifeq \S*', line[1]) != None or re.match(r'^#ifneq \S*', line[1]) != None or re.match(r'^#ifdef \S*', line[1]) != None):
                        partial = ("Remove","ifdef")
                        if(partial not in result):
                            result.append(partial)
            return result

