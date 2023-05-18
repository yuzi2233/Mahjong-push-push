class Mahjong:
    def __init__(self,form,num):
        self.status = 0

        self.form = form
        self.num = num

    def changeStatus(self):
        if self.status == 0:
            self.status = 1
        else:
            self.status = 0
