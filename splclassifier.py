class SPLClassifier:
    
    def __init__(self,added=[],removed=[]):
        self.added = added
        self.removed = removed
    
    def setAdded(self,lista):
        self.added = lista
    
    def setRemoved(self,lista):
        self.removed = lista
    
    def classify(self):
        removeds = self.removed
        addeds = self.added
        result = []

        #Classificação caso só haja remoções no arquivo
        if(len(removeds) > 0 and len(addeds) == 0):
            for line in removeds:
                if("menu" in line[1]):
                    partial = ("Remove","Menu")
                    if(partial not in result):
                        result.append(partial)
                elif("config" in line[1]):
                    partial = ("Remove","Feature")
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

        #Classificação caso só haja adições no arquivo
        elif(len(addeds) > 0 and len(removeds) == 0):
            # TODO
        
        #Clasificação caso haja possíveis modificações
        else:
            # TODO