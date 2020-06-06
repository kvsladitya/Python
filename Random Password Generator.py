from random import randrange
from datetime import date,datetime


class RPG:
    def __init__(self):
        '''Initializes the variables and Statements'''
        print("\n ========================= \n")
        print("\n Random Password Generator \n")
        print("\n Enter a Keyword \n")
        print("\n ========================= \n")
        self.sp_ch = ["!","@","#","$","%","^","&","*","(",")","-","_","=","+","{","}","[","]",";",":","'",'"',"<",">",",",".","/","?","`","`"]
        self.pswd = {}
        self.keyword = input()
        if self.keyword:
            self.password_constructor()

    def password_constructor(self):
        '''Constructs a password using the given keyword'''
        for each in range(10):
            temp = randrange(33,130)
            t2 = chr(temp)
            t1 = randrange(0,len(self.sp_ch)) - 1
            if t2 in self.sp_ch:
                self.keyword = self.keyword + t2 + self.sp_ch[t1]
        return self.password_storage()

    def password_storage(self):
        '''Stores the Generated passoword in a dictionary with date as Key'''
        self.pswd.update({str(date.today()) : {datetime.now().strftime("%H:%M:%S") : self.keyword}})
        return self.pswd


if __name__ == '__main__':
    Obj = RPG()
    print("Generated Password is : {}".format(Obj.keyword))