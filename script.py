import os

class Script():
    def __init__(self,name,functions,created_time,linesFather = [],lastClickOnLb2=0,path = os.path.dirname(os.path.realpath(__file__)) + "\\Scripts\\"):
        self.name = name
        self.functions = functions
        self.path = path + name + '\\'
        self.created_time = created_time
        self.linesFather = linesFather
        self.lastClickOnLb2 = lastClickOnLb2

        if(os.path.isdir(self.path) == False):
            try:
                os.mkdir(self.path)
            except OSError:
                print("Creation of the directory %s failed" % path)


    def getFunctions(scriptPath):
        path = scriptPath + "functions.txt"
        functionsFile = open(scriptPath + "functions.txt","r")
        functions = functionsFile.read()



