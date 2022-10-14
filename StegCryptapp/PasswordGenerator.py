# -*- coding:utf-8 -*-

from random import SystemRandom

RandomSys = SystemRandom()

def PasswordGenerator(length=32):
    numbers = [RandomSys.randint(48, 57) for i in range(57-48)]
    minletter = [RandomSys.randint(97, 122) for i in range(122-97)]
    majletter = [RandomSys.randint(65, 90) for i in range(90-65)]
    otherElemt = [i for i in range(128) if i in [g for g in range(32, 48)] or i in [p for p in range(58,65)] or i in [h for h in range(91,97)] or i in [t for t in range(123,128)]]
    elmtList = [numbers, minletter, majletter, otherElemt]
    chaine = []
    for i in range(len(elmtList)):
        for j in range(length//len(elmtList)):
            chaine.append(RandomSys.choice(elmtList[i]))
    chaine = "".join([chr(RandomSys.choice(chaine)) for i in range(length)])
    return chaine

if __name__ == "__main__":
    print(PasswordGenerator())