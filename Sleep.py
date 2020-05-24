class Sleep():
    def __init__(self, time):
        self.time = time

    def getDict(self):
        return {'time':str(self.time)}

    @classmethod
    def getExtra(cls, extra):
        return Sleep(extra['time'])

    def changeSleepTime(sv,Lb2,currentScript):
        try:
            index = currentScript.lastClickOnLb2
        except:
            print('need to mark the function that you want to change')
        if(currentScript.functions[index].name == 'Sleep'):
            if (sv.get() == ''):
                currentScript.functions[index].extra.time = '?'
            else:
                currentScript.functions[index].extra.time = int(sv.get())
            # currentScript.functions[index].name = "Sleep"
            Lb2.delete(index)
            shift = ' ' * currentScript.functions[index].indention * 5
            Lb2.insert(index,
                       shift + currentScript.functions[index].name + '({})'.format(currentScript.functions[index].extra.time))
            Lb2.itemconfig(index, foreground='#57ff7f')
            Lb2.selection_set(index)
            return True