class Photo():
    def __init__(self,x0,y0,x1,y1,imgPath):
        self.x0Cord = x0
        self.x1Cord = x1
        self.y0Cord = y0
        self.y1Cord = y1
        self.img = imgPath
    def getDict(self):
         return({'x0Cord':str(self.x0Cord), 'x1Cord':str(self.x1Cord), 'y0Cord':str(self.y0Cord), 'y1Cord':str(self.y1Cord), 'img':self.img})

    @classmethod
    def getImg(cls, img):
        return Photo(int(img['x0Cord']),int(img['y0Cord']),int(img['x1Cord']),int(img['y1Cord']),img['img'])