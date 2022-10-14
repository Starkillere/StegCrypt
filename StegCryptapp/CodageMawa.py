__all__ = [__loader__]

from random import SystemRandom 
from operator import xor

class CodageMawa:
    def __init__(self) -> None:
        self.mawaTable = (32,125)
        self.max = 55296
        self.sr = SystemRandom()
    
    def __notElement(self, text:str):
        for i in text:
            if ord(i) > self.max:
                return False
        return True
    
    def master_key_generator(self):
        master_key = ''.join([chr(self.sr.randint(self.mawaTable[0], self.mawaTable[1])) for i in range(19)])
        return master_key

    def _iv_genretor(self) -> str:
        initializationVector = ''.join([chr(self.sr.randint(self.mawaTable[0], self.mawaTable[1])) for i in range(5)])
        return initializationVector
    
    def __creat_bloc(self, text:str, nBloc=5) -> list[str]:
        listBloc = []
        bloc = []
        count = 0
        for i in range(len(text)):
            if count == nBloc:
                listBloc.append(bloc)
                bloc = []
                count = 0
            bloc.append(text[i])
            count += 1
        listBloc.append(bloc)
        return listBloc

    def __complementer_bloc(self, blocList:list[str], nBloc=5):
        Round = [nBloc-len(blocList[i]) for i in range(len(blocList))]
        randomNumber = self.sr.randint(self.mawaTable[0], self.mawaTable[1])
        for i in range(len(blocList)):
            if len(blocList[i]) < nBloc:
                for j in range(nBloc-len(blocList[i])):
                    randomNumber = self.sr.randint(self.mawaTable[0], self.mawaTable[1])
                    blocList[i].append(chr(randomNumber))
        return (blocList, Round)
    
    def __DeComplementer_bloc(self, bloc:list[int], Round:int) -> str:
        if Round == 0:
            return bloc
        return bloc[:-Round]

    def _function_not_name(self, bloc:list[int], masterkey:str) -> list[int]:

        def bitsComplementer(liste:list[str], max_len:int) -> list[str]:
            for i in range(len(liste)):
                while len(liste[i]) < max_len:
                    liste[i] = "0"+liste[i]
            return liste

        max_len =  0
        masterkey =  self.__creat_bloc(masterkey)
        masterkey:list = [[ord(j) for j in i] for i in masterkey]
        for i in range(len(bloc)):
            nb = bloc[i] + 7
            bloc[i] = bin(nb)[2:]
            if len(bloc[i]) > max_len:
                max_len = len(bloc[i])

        for i in range(len(masterkey)):
            if len(masterkey[i]) < len(bloc):
                for t in range(len(bloc)-len(masterkey[i])):
                    masterkey[i].append(0)
            for j in range(len(masterkey[i])):
                masterkey[i][j] = bin(masterkey[i][j])[2:]
                if len(masterkey[i][j]) > max_len:
                    max_len = len(masterkey[i][j])

        bloc, masterkey = bitsComplementer(bloc, max_len), [bitsComplementer(i, max_len) for i in masterkey]


        for i in range(len(masterkey)):
            for j in range(len(bloc)):
                chaine = ""
                for y in range(len(bloc[0])):
                    chaine += str(xor(int(bloc[j][y]), int(masterkey[i][j][y])))
                bloc[j] = chaine

        chiffre = [int(i,2) for i in bloc]
        return chiffre
        

    def _reciprocal_function_not_name(self, bloc:list[int], masterkey:str) -> list[int]:

        def bitsComplementer(liste:list[str], max_len:int) -> list[str]:
            for i in range(len(liste)):
                while len(liste[i]) < max_len:
                    liste[i] = "0"+liste[i]
            return liste
        
        max_len =  0
        masterkey =  self.__creat_bloc(masterkey)
        masterkey:list = [[ord(j) for j in i] for i in masterkey]
        
        for i in range(len(bloc)):
            bloc[i] = bin(bloc[i])[2:]
            if len(bloc[i]) > max_len:
                max_len = len(bloc[i])
        for i in range(len(masterkey)):
            if len(masterkey[i]) < len(bloc):
                for t in range(len(bloc)-len(masterkey[i])):
                    masterkey[i].append(0)
            for j in range(len(masterkey[i])):
                masterkey[i][j] = bin(masterkey[i][j])[2:]
                if len(masterkey[i][j]) > max_len:
                    max_len = len(masterkey[i][j])

        bloc, masterkey = bitsComplementer(bloc, max_len), [bitsComplementer(i, max_len) for i in masterkey]

        for i in range(len(masterkey)):
            for j in range(len(bloc)):
                chaine = ""
                for y in range(len(bloc[0])):
                    chaine += str(xor(int(bloc[j][y]), int(masterkey[i][j][y])))
                bloc[j] = chaine

        chiffre = [int(i,2) for i in bloc]
        clair = [p-7 for p in chiffre]
        return clair
    
    def mawaEncode(self, text:str, masterKey:str) -> tuple:

        def max_len(liste:list[str]) -> int:
            max_len = 0
            for i in range(len(liste)):
                if max_len < len(liste[i]):
                    max_len = len(liste[i])
            return max_len

        def bitsComplementer(liste:list[str], max_len:int) -> list[str]:
            for i in range(len(liste)):
                while len(liste[i]) < max_len:
                    liste[i] = "0"+liste[i]
            return liste

        if self.__notElement(text):
            bloc_list, Round = self.__complementer_bloc(self.__creat_bloc(text))
            initialization_vecteur = self._iv_genretor()
            listBolckEncode = []
            for i in range(len(bloc_list)):
                bitsBloc = [bin(ord(elmt))[2:] for elmt in bloc_list[i]]
                if i == 0:
                    BitsVector = [bin(ord(elmt))[2:] for elmt in initialization_vecteur]
                else:
                    BitsVector = [bin(ord(elmt))[2:] for elmt in listBolckEncode[i-1]]
                if len(bitsBloc) < len(BitsVector):
                    for a in range(len(BitsVector)-len(bitsBloc)):
                        bitsBloc.append('0')
                else:
                    for a in range(len(bitsBloc)-len(BitsVector)):
                        BitsVector.append('0')
                if max_len(bitsBloc) < max_len(BitsVector):
                    the_max_len = max_len(BitsVector)
                else:
                    the_max_len = max_len(bitsBloc)
                bitsBloc, BitsVector = bitsComplementer(bitsBloc, the_max_len), bitsComplementer(BitsVector, the_max_len)
                encodeBloc = []
                for z in range(len(bitsBloc)):
                    chainebloc = ""
                    for j in range(len(bitsBloc[z])):
                        chainebloc += str(xor(int(bitsBloc[z][j]), int(BitsVector[z][j])))
                    encodeBloc.append(int(chainebloc,2))
                encodeBloc = self._function_not_name(encodeBloc, masterKey)
                encodeBloc = [chr(elmt) for elmt in encodeBloc]
                listBolckEncode.append(encodeBloc)
            listBolckEncode = [''.join(bloc) for bloc in listBolckEncode]
            chiffre = ''.join(listBolckEncode)      
            return (chiffre, initialization_vecteur, Round)
        return False 
                              
    def mawaDecode(self, text:str, masterKey:str, initialization_vecteur:str, Round:list[int]):

        def max_len(liste:list[str]) -> int:
            max_len = 0
            for i in range(len(liste)):
                if max_len < len(liste[i]):
                    max_len = len(liste[i])
            return max_len

        def bitsComplementer(liste:list[str], max_len:int) -> list[str]:
            for i in range(len(liste)):
                while len(liste[i]) < max_len:
                    liste[i] = "0"+liste[i]
            return liste

        listBloc = self.__creat_bloc(text)
        decodeBloc = []
        for i in range(len(listBloc)):
            bloc = [ord(elmt) for elmt in listBloc[i]]
            bloc = self._reciprocal_function_not_name(bloc, masterKey)
            bitsBloc = [bin(elmt)[2:] for elmt in bloc]
            if i == 0:
                BitsVector = [bin(ord(elmt))[2:] for elmt in initialization_vecteur]
            else:
                BitsVector = [bin(ord(elmt))[2:] for elmt in listBloc[i-1]]
            if len(bitsBloc) < len(BitsVector):
                for a in range(len(BitsVector)-len(bitsBloc)):
                    bitsBloc.append('0')
            else:
                for a in range(len(bitsBloc)-len(BitsVector)):
                    BitsVector.append('0')
            if max_len(bitsBloc) < max_len(BitsVector):
                the_max_len = max_len(BitsVector)
            else:
                the_max_len = max_len(bitsBloc)
            bitsBloc, BitsVector = bitsComplementer(bitsBloc, the_max_len), bitsComplementer(BitsVector, the_max_len)
            encodeBloc = []
            for z in range(len(bitsBloc)):
                chainebloc = ""
                for j in range(len(bitsBloc[z])):
                    chainebloc += str(xor(int(bitsBloc[z][j]), int(BitsVector[z][j])))
                encodeBloc.append(int(chainebloc,2))
            while 0 in encodeBloc:
                    encodeBloc.remove(0)
            encodeBloc = self.__DeComplementer_bloc(encodeBloc, Round[i])
            encodeBloc = [chr(elmt) for elmt in encodeBloc]
            decodeBloc.append(encodeBloc)
        decodeBloc = [''.join(bloc) for bloc in decodeBloc]
        clair = ''.join(decodeBloc)
        return clair
        
if __name__ == '__main__':
    mypass = CodageMawa()
    sr = SystemRandom()
    Text = "\nQuand le ciel bas et lourd pèse comme un couvercle\nSur l'esprit gémissant en proie aux longs ennuis,\nEt que de l'horizon embrassant tout le cercle\nII nous verse un jour noir plus triste que les nuits ;\n\n\n\nQuand la terre est changée en un cachot humide,\nOù l'Espérance, comme une chauve-souris,\nS'en va battant les murs de son aile timide\nEt se cognant la tête à des plafonds pourris ;\n\n\n\nQuand la pluie étalant ses immenses traînées\nD'une vaste prison imite les barreaux,\nEt qu'un peuple muet d'infâmes araignées\nVient tendre ses filets au fond de nos cerveaux,\n\n\n\nDes cloches tout à coup sautent avec furie\nEt lancent vers le ciel un affreux hurlement,\nAinsi que des esprits errants et sans patrie\nQui se mettent à geindre opiniâtrement.\n- Et de longs corbillards, sans tambours ni musique,\nDéfilent lentement dans mon âme ; l'Espoir,\nVaincu, pleure, et l'Angoisse atroce, despotique,\nSur mon crâne incliné plante son drapeau noir.\n\n\n\n     Charles Baudelaire, Les Fleurs du mal\n"
    print(f"\nText = {Text}\n")
    master_key = mypass.master_key_generator()
    chiffre, iv, roundt = mypass.mawaEncode(Text, master_key)
    print(f"Master key = {master_key}\n")
    print(f"Vecteur Initial = {iv}\n")
    print(f"Chiffré = {chiffre}\n")
    clair = mypass.mawaDecode(chiffre,master_key,iv, roundt)
    print(f"Clair = {clair}\n")
    print("seem", Text == clair)
    print("len", len(Text) == len(clair))