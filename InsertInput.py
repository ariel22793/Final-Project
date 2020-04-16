class InsertInput():
    def __init__(self, text):
        self.text = text

    def getDict(self):
        return {'text':self.text}

    @classmethod
    def getExtra(cls, extra):
        return InsertInput(extra['text'])

    def changeInsertInputText(sv,Lb2,currentScript):
        try:
            index = Lb2.curselection()[0]
        except:
            print('need to mark the function that you want to change')
        currentScript.functions[index].extra.text = sv.get()
        currentScript.functions[index].name = "Insert-Input"
        Lb2.delete(index)
        shift = ' ' * currentScript.functions[index].indention * 5
        Lb2.insert(index,
                   shift + currentScript.functions[index].name + '("{}")'.format(currentScript.functions[index].extra.text))
        Lb2.selection_set(index)
        return True