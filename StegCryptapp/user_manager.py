#-*- coding:utf-8 -*-
from typing import Iterable
from .rsa import generate_keys
from hashlib import sha1
from .CodageMawa import CodageMawa

def min_chiffrement(text:str):
    return chr((ord(text)+8)%CodageMawa().max)

def min_dechiffrement(text:str):
    return chr((ord(text)-8)%CodageMawa().max)

def traitement_de_donnees(data:Iterable, mode="n-s"):
    bloChaine = ""
    if mode == "text":
        for i in range(len(data)):
            bloChaine += min_chiffrement(data[i])
    else:
        data = list(data)
        for i in range(len(data)):
            data[i] = str(data[i])
            minChaine = ""
            for j in range(len(data[i])):
                cipher = min_chiffrement(data[i][j])
                if j < (len(data[i])-1):
                    minChaine += cipher+","
                else:
                    minChaine += cipher
            if j == (len(data[i])-1) and i == (len(data)-1):
                bloChaine += minChaine
            else:
                bloChaine += minChaine+"!"
    return bloChaine

def logtraitement_de_donnees(data:str, mode="n-s"):
    if mode == "text":
        bloChaine = ""
        for i in range(len(data)):
            bloChaine += min_dechiffrement(data[i])
        return bloChaine
    else:
        data = [sect.split(",") for sect in data.split("!")]
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] =  min_dechiffrement(data[i][j])
        data[i] = int(''.join(data[i]))
    return tuple(data)

def login(username:str, password:str, table):

    hashedPassword = sha1(password.encode()).hexdigest()
    user = table.query.filter_by(nom=username).first()
    if user != None and user.master_password == hashedPassword:
        rsa_privat_key = logtraitement_de_donnees(user.rsa_privet_key)
        rsa_publique_key = logtraitement_de_donnees(user.rsa_public_key)
        Round = list(logtraitement_de_donnees(user.round))
        initial_vecteur = logtraitement_de_donnees(user.vecteur_initial, mode="text")
        mawa_masterkey = CodageMawa().mawaDecode(user.Mawakey, password, initial_vecteur, Round)

        rsa_keys = {'key publique':rsa_publique_key, 'key priver':rsa_privat_key}
        user_data = {"ID":user.id, "RSA":rsa_keys, "CadageMawa": mawa_masterkey}
        return user_data

    return False

def signin(username:str, password:str, mail:str, table, db):

        user_mail =  table.query.filter_by(mail=mail).first()
        user_name = table.query.filter_by(nom=username).first()
        if user_mail is None and user_name is None:
            mawa_masterkey = CodageMawa().master_key_generator()
            rsa_key = generate_keys()

            hashedPassword = sha1(password.encode()).hexdigest()
            cipher_mawa_masterkey, initialization_vecteur, Round = CodageMawa().mawaEncode(mawa_masterkey, password)
            cipher_rsa_privet_key = traitement_de_donnees(rsa_key["key priver"])
            cipher_public_rsa_key = traitement_de_donnees(rsa_key['key publique'])
            cipher_initialization_vecteur = traitement_de_donnees(initialization_vecteur, mode="text")
            cipher_round = traitement_de_donnees(Round)
            
            user = table(nom=username, master_password=hashedPassword, rsa_public_key=cipher_public_rsa_key, rsa_privet_key=cipher_rsa_privet_key, Mawakey=cipher_mawa_masterkey, vecteur_initial=cipher_initialization_vecteur, round=cipher_round, mail=mail)
            db.session.add(user)
            db.session.commit()

            new_user = table.query.filter_by(nom=username).first()
            user_data = {"ID":new_user.id, "RSA":rsa_key, "CadageMawa":new_user.Mawakey}
            return user_data
        return False

def change_name_mail(user_id:int, new_user_name:str, mail:str, table, db):
    user = table.query.get(user_id)
    user.nom = new_user_name
    user.mail = mail
    db.session.commit()
    return True

def delt_user(user_id:int, table, db):
   user = table.query.get(user_id)
   db.session.delete(user)
   db.session.commit()
   return True

def change_password(user_id:int, user_name:str,  password:str, new_password:str, table, db):
    user = login(user_name, password, table)
    if user:
        user = table.query.get(user_id)
        hashedPassword = sha1(new_password.encode()).hexdigest()
        cipher_mawa_masterkey, initialization_vecteur, Round = CodageMawa().mawaEncode(user.Mawakey, new_password)
        cipher_initialization_vecteur = traitement_de_donnees(initialization_vecteur, mode="text")
        cipher_round = traitement_de_donnees(Round)

        
        user.master_password = hashedPassword
        user.Mawakey = cipher_mawa_masterkey
        user.vecteur_initial = cipher_initialization_vecteur
        user.round = cipher_round
        db.session.commit()

        return True
    return False