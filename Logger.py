from datetime import datetime
import os

class Logger():
    def __init__(self,path):
        self.path = path
        testLog = open(self.path, "w+")
        testLog.write('')


    def writeToLog(self, operation):
        testLog = open(self.path, "a") #append if already exists
        testLog.write('Time:{}, Operation:{} \n'.format(datetime.now(),operation))
        testLog.close()
    def writeExeption(self,msg):
        testLog = open(self.path, "w+")
        testLog.write('Time:{} , Exeption:{}'.format(datetime.now(),msg))
