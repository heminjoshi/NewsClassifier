
class URL(object) :
    def __init__(self, base) :
        self.url = base;
    def addParam(self, param) :
        self.url +=  param
    def toString(self):
        return str(self.url);