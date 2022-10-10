#-*- conding:utf-8 -*-
from CodageMawa import CodageMawa
from user_manager import traitement_de_donnees
from creatTable import database
import sqlite3

def save_data_from_form(platform:str, pseudo:str, password:str, mail:str, user_id:int,  masterkey:str):
    my_pass = CodageMawa()
    Chiffred_password, vecteur_initial, Round = my_pass.mawaEncode(password, masterkey)
    cipher_Round = traitement_de_donnees(Round)
    cipher_vecteur_initial = traitement_de_donnees(vecteur_initial, mode="text")
    with sqlite3.connect(database['name']) as connection:
        cursor = connection.cursor()
        requete = f"insert into gestionnaire ({database['Table'][1]['keys'][0]}, {database['Table'][1]['keys'][1]}, {database['Table'][1]['keys'][2]}, {database['Table'][1]['keys'][3]}, {database['Table'][1]['keys'][4]}, {database['Table'][1]['keys'][5]}, {database['Table'][1]['keys'][6]}) values (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(requete, [(user_id), (platform.capitalize()), (pseudo), (Chiffred_password), (mail), (cipher_Round), (cipher_vecteur_initial)])     
        connection.commit()
        return True

def change_data(user_id:int, data_liste:list, platforme:str, masterkey:str):
    with sqlite3.connect(database['name']) as connection:
            cursor = connection.cursor()
            requete = f"DELETE FROM gestionnaire WHERE {database['Table'][1]['keys'][0]} = ? AND {database['Table'][1]['keys'][1]} = ?"
            cursor.execute(requete, [(user_id), (platforme)])
            connection.commit()
    
    for data in data_liste:
        save_data_from_form(platforme, data[0], data[1], data[2], user_id, masterkey)
    return True

def delt_all(user_id:int, platforme:str):
    with sqlite3.connect(database['name']) as connection:
            cursor = connection.cursor()
            requete = f"DELETE FROM gestionnaire WHERE {database['Table'][1]['keys'][0]} = ? AND {database['Table'][1]['keys'][1]} = ?"
            cursor.execute(requete, [(user_id), (platforme)])
            connection.commit()
    return True

def delt_user_data(user_id:int):
    with sqlite3.connect(database['name']) as connection:
            cursor = connection.cursor()
            requete = f"DELETE FROM gestionnaire WHERE {database['Table'][1]['keys'][0]} = ?"
            cursor.execute(requete, [(user_id)])
            connection.commit()
    return True