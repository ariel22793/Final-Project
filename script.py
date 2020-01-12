import os

class Script():
    def __init__(self,name,functions,created_time,path = os.path.dirname(os.path.realpath(__file__)) + "\\Scripts\\"):
        self.name = name
        self.functions = functions
        self.path = path + name + '\\'
        self.created_time = created_time

        if(os.path.isdir(self.path) == False):
            try:
                os.mkdir(self.path)
                open(self.path + "functions.txt","w+")
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)


    def getFunctions(scriptPath):
        path = scriptPath + "functions.txt"
        functionsFile = open(scriptPath + "functions.txt","r")
        functions = functionsFile.read()

