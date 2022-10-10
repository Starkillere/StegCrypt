#-*- coding:utf-8 -*-
import sqlite3
from creatTable import database
from CodageMawa import CodageMawa
from user_manager import logtraitement_de_donnees
import os

def render_data__section(user_id:int):
    with sqlite3.connect(database['name']) as connection:
        cursor = connection.cursor()
        requete = f"select * from {database['Table'][1]['name']} WHERE {database['Table'][1]['keys'][0]} = ?"
        cursor.execute(requete, [(user_id)])
        user_data = cursor.fetchall()
    
    liste_user_platform = []
    for i in range(len(user_data)):
        if not user_data[i][1] in liste_user_platform:
            liste_user_platform.append(user_data[i][1])
    return liste_user_platform

def render_data(mawakey:str, user_id:str, motif:str):
    with sqlite3.connect(database['name']) as connection:
        cursor = connection.cursor()
        requete = f"select * from {database['Table'][1]['name']} WHERE {database['Table'][1]['keys'][0]} = ? AND {database['Table'][1]['keys'][1]} = ?"
        cursor.execute(requete, [(user_id), (motif)])
        user_data = cursor.fetchall() 

    data = []
    for i in range(len(user_data)):
        Round = list(logtraitement_de_donnees(user_data[i][5]))
        initial_vecteur = logtraitement_de_donnees(user_data[i][6], mode="text")
        password = CodageMawa().mawaDecode(user_data[i][3], mawakey, initial_vecteur, Round)

        data.append([i, user_data[i][2], password, user_data[i][4]])
    
    return (data, len(user_data))

def return_dir_elmt(dir):
    elmts = os.listdir(dir)
    for i in range(len(elmts)):
        elmts[i] = (elmts[i].split(".png"))[0]+","
    elmts = ''.join(elmts)
    return elmts

def render_email(id:int):
    with sqlite3.connect(database['name']) as connection:
        cursor = connection.cursor()
        requete = f"select * from {database['Table'][0]['name']} WHERE {database['Table'][0]['keys'][0]} = ? "
        cursor.execute(requete, [(id)])
        user = cursor.fetchone()
    return user[8]
        