#-*- coding:utf-8 -*-
import sqlite3
from typing import Iterable
from rsa import generate_keys
from hashlib import sha1
from CodageMawa import CodageMawa
from creatTable import creat, database


__all__ = ["login", "signin"]

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

def login(username:str, password:str):

    database = creat()

    with sqlite3.connect(database['name']) as connection:

        hashedPassword = sha1(password.encode()).hexdigest()

        cursor = connection.cursor()
        requete = f"select * from {database['Table'][0]['name']} WHERE {database['Table'][0]['keys'][1]} = ? AND {database['Table'][0]['keys'][2]} = ?"
        cursor.execute(requete, [(username), (hashedPassword)])
        user = cursor.fetchone()

        if user != None:
            rsa_privat_key = logtraitement_de_donnees(user[4])
            rsa_publique_key = logtraitement_de_donnees(user[3])
            Round = list(logtraitement_de_donnees(user[7]))
            initial_vecteur = logtraitement_de_donnees(user[6], mode="text")
            mawa_masterkey = CodageMawa().mawaDecode(user[5], password, initial_vecteur, Round)

            requete = f"select * from {database['Table'][0]['name']} WHERE {database['Table'][0]['keys'][1]} = ?"
            cursor.execute(requete, [(username)])
            user = cursor.fetchone()
            print(user[0])
            rsa_keys = {'key publique':rsa_publique_key, 'key priver':rsa_privat_key}
            user_data = {"ID":user[0], "RSA":rsa_keys, "CadageMawa": mawa_masterkey}
            return user_data
        return False

def signin(username:str, password:str, mail:str):

    database = creat()
    
    with sqlite3.connect(database['name']) as connection:

        cursor = connection.cursor()
        requete = f"select * from {database['Table'][0]['name']} WHERE {database['Table'][0]['keys'][1]} = ?"
        cursor.execute(requete, [(username)])
        user = cursor.fetchone()
        
        if user == None:
            mawa_masterkey = CodageMawa().master_key_generator()
            rsa_key = generate_keys()

            hashedPassword = sha1(password.encode()).hexdigest()
            cipher_mawa_masterkey, initialization_vecteur, Round = CodageMawa().mawaEncode(mawa_masterkey, password)
            cipher_rsa_privet_key = traitement_de_donnees(rsa_key["key priver"])
            cipher_public_rsa_key = traitement_de_donnees(rsa_key['key publique'])
            cipher_initialization_vecteur = traitement_de_donnees(initialization_vecteur, mode="text")
            cipher_round = traitement_de_donnees(Round)

            requete = f"insert into {database['Table'][0]['name']} ({database['Table'][0]['keys'][1]}, {database['Table'][0]['keys'][2]}, {database['Table'][0]['keys'][3]}, {database['Table'][0]['keys'][4]}, {database['Table'][0]['keys'][5]}, {database['Table'][0]['keys'][6]}, {database['Table'][0]['keys'][7]}, {database['Table'][0]['keys'][8]}) values (?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(requete, [(username), (hashedPassword), (cipher_public_rsa_key), (cipher_rsa_privet_key), (cipher_mawa_masterkey), (cipher_initialization_vecteur), (cipher_round), (mail)])
            connection.commit()

            requete = f"select * from {database['Table'][0]['name']} WHERE {database['Table'][0]['keys'][1]} = ?"
            cursor.execute(requete, [(username)])
            user = cursor.fetchone()
            user_data = {"ID":user[0], "RSA":rsa_key, "CadageMawa":mawa_masterkey}
            return user_data
        return False

def change_name_mail(user_id:int, new_user_name:str, user_name:str, mail:str):
    with sqlite3.connect(database['name']) as connection:
        cursor = connection.cursor()
        requete = f"select * from {database['Table'][0]['name']} WHERE {database['Table'][0]['keys'][1]} = ?"
        cursor.execute(requete, [(new_user_name)])
        user = cursor.fetchone()
        if user == None or user[1] == user_name:
            cursor = connection.cursor()
            requete = f"UPDATE {database['Table'][0]['name']} SET {database['Table'][0]['keys'][1]} = ?, {database['Table'][0]['keys'][8]} = ? WHERE {database['Table'][0]['keys'][0]} = ? "
            cursor.execute(requete, [(new_user_name), (mail), (user_id)])
            connection.commit()
            return True
    return False

def delt_user(user_id:int):
    with sqlite3.connect(database['name']) as connection:
        cursor = connection.cursor()
        requete = f"DELETE FROM {database['Table'][0]['name']} WHERE {database['Table'][0]['keys'][0]} = ?"
        cursor.execute(requete, [(user_id)])
        connection.commit()
    return True

def change_password(user_id:int, user_name:str,  password:str, new_password:str):
    user = login(user_name, password)
    if user:
        hashedPassword = sha1(new_password.encode()).hexdigest()
        cipher_mawa_masterkey, initialization_vecteur, Round = CodageMawa().mawaEncode(user["CadageMawa"], new_password)
        cipher_initialization_vecteur = traitement_de_donnees(initialization_vecteur, mode="text")
        cipher_round = traitement_de_donnees(Round)
        with sqlite3.connect(database['name']) as connection:
            cursor = connection.cursor()
            requete = f"UPDATE {database['Table'][0]['name']} SET {database['Table'][0]['keys'][2]} = ?, {database['Table'][0]['keys'][5]} = ?, {database['Table'][0]['keys'][6]} = ?, {database['Table'][0]['keys'][7]} = ?  WHERE {database['Table'][0]['keys'][0]} = ?"
            cursor.execute(requete, [(hashedPassword), (cipher_mawa_masterkey), (cipher_initialization_vecteur), (cipher_round), (user_id)])
            connection.commit()
        return True
    return False