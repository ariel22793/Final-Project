class Sleep():
    def __init__(self, time):
        self.time = time

    def getDict(self):
        return {'time':str(self.time)}

    @classmethod
    def getExtra(cls, extra):
        return Sleep(extra['time'])

    def changeSleepTime(sv,Lb2,currentScript):
        index = Lb2.curselection()[0]
        currentScript.functions[index].extra.time = int(sv.get())
        currentScript.functions[index].name = "Sleep"
        Lb2.delete(index)
        Lb2.insert(index,
                   currentScript.functions[index].name + '({})'.format(currentScript.functions[index].extra.time))
        Lb2.selection_set(index)
        return True