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
            for line in removed:
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
        elif(len(added) > 0 and len(removed) == 0):
            for line in added:
                if("menu" in line[1]):
                    partial = ("Added","Menu")
                    if(partial not in result):
                        result.append(partial)
                elif("config" in line[1]):
                    partial = ("Added","Feature")
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
            return result
        
        #Clasificação caso haja possíveis modificações
        else:
            print("TODO")
            # TODO
            return result