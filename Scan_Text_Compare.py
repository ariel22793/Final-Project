
class Scan_Text_Compare():
    def __init__(self, text):
        self.text = text

    def getDict(self):
        return {'text':self.text}

    @classmethod
    def getExtra(cls, extra):
        return Scan_Text_Compare(extra['text'])

    def changeScan_Text_Compare(sv,Lb2,currentScript):
        try:
            index = currentScript.lastClickOnLb2
        except:
            print('need to mark the function that you want to change')
        if (currentScript.functions[index].name == 'Scan Text & Compare'):
            currentScript.functions[index].extra.text = sv.get()
            # currentScript.functions[index].name = "Insert-Input"

            Lb2.delete(index)
            shift = ' ' * currentScript.functions[index].indention * 5
            Lb2.insert(index,
                       shift + currentScript.functions[index].name + '("{}")'.format(currentScript.functions[index].extra.text))
            Lb2.itemconfig(index, foreground='white')
            Lb2.selection_set(index)
            return True