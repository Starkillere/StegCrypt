#-*- coding:utf-8- -*-

import numpy as np
from PIL import Image
from random import SystemRandom

class Steganographie:
    def __init__(self):
        self.sr = SystemRandom()
    
    def __resize_image(self, image:Image, hote:Image):
        Tableimage = np.array(image)
        Tablehote = np.array(hote)
        sizeImage = (len(Tableimage[0]), len(Tableimage))
        sizeHote = (len(Tablehote[0]), len(Tablehote))

        if sizeImage == sizeHote:
            return (Tableimage, Tablehote)
        else:
            hote = hote.resize(sizeImage)
            Tablehote = np.array(hote)
            return (Tableimage, Tablehote)
            
    def encodeImageByImage(self, image:str, hote:str, folder="/"):
        imageName = image.split("/")[-1]
        image = Image.open(image)
        hote = Image.open(hote)
        Tableimage,TableHote = self.__resize_image(image, hote)
        for i in range(len(TableHote)):
            for j in range(len(TableHote[0])):
                for p in range(3):
                    valeur_rgb_hote_bin = bin(TableHote[i][j][p])[2:]
                    valeur_rgb_image_bin = bin(Tableimage[i][j][p])[2:]
                    while len(valeur_rgb_hote_bin) < 8:
                        valeur_rgb_hote_bin = '0'+valeur_rgb_hote_bin
                    while len(valeur_rgb_image_bin) < 8:
                        valeur_rgb_image_bin = '0'+valeur_rgb_image_bin
                    new_value_bin = valeur_rgb_hote_bin[:4] + valeur_rgb_image_bin[:4]
                    Tableimage[i][j][p] = int(new_value_bin,2)
        cacher_image = Image.fromarray(Tableimage)
        cacher_image.save(folder+"/"+imageName)
        return folder+"/"+imageName

    def decodeImageByImage(self, image:str, folder="/"):
        imageName = image.split("/")[-1]
        image = Image.open(image)
        Tableimage = np.array(image)
        for i in range(len(Tableimage)):
            for j in range(len(Tableimage[0])):
                for p in range(3):
                    valeur_rgb_image_bin = bin(Tableimage[i][j][p])[2:]
                    while len(valeur_rgb_image_bin) < 8:
                        valeur_rgb_image_bin = '0'+valeur_rgb_image_bin
                    new_value_bin = valeur_rgb_image_bin[3:] + '0000'
                    Tableimage[i][j][p] = int(new_value_bin,2)
        cacher_image = Image.fromarray(Tableimage)
        cacher_image.save(folder+"/"+imageName)
        return folder+"/"+imageName

    def hideTextInImage(self, text:str, image:str, folder="/"):
        im = Image.open(image)
        x , y = im.size
        r , g , b = im.split()
        r = list( r.getdata() )
        u = len(text)
        v = bin( len(text) )[2:].rjust(8,"0")
        ascii = [ bin(ord(x))[2:].rjust(8,"0") for x in text ]
        a = ''.join(ascii)
        for j in range(8):
            r[j] = 2 * int( r[j] // 2 ) + int( v[j] )
        
        for i in range(8*u):
            r[i+8] = 2 * int( r[i+8] // 2 ) + int( a[i] )

             
        nr = Image.new("L",(16*x,16*y))
        nr = Image.new("L",(x,y))
        nr.putdata(r)
        
        imgnew = Image.merge('RGB',(nr,g,b))
        new_name_img = folder + "/" + image.split("/")[-1]
        imgnew.save(new_name_img)
        return new_name_img
    
    def findText(self, image:str):
        im = Image.open(image)
        r , g , b = im.split()
        r = list( r.getdata() )

        p = [ str(x%2) for x in r[0:8] ]
        q = "".join(p)
        q = int(q,2)

        n = [ str(x%2) for x in r[8:8*(q+1)] ]
        b = "".join(n)
        message = ""
        for k in range(0,q):
            l = b[8*k:8*k+8]
            message += chr(int(l,2))

        return message

    def cipherImage(self, masterkey:str, encrypteSystem:str, modOption={}):
        pass

    def decryptionImage(self, masterkey:str, encrypteSystem:str, modOption={}):
        pass