#-*- coding:utf-8 -*-
from .CodageMawa import CodageMawa
from .user_manager import logtraitement_de_donnees
import os

def render_data__section(user_id:int, table):
    datas = table.query.filter_by(user_id=user_id).all()
    
    liste_user_platform = []
    for i in range(len(datas)):
        if not datas[i].platforme in liste_user_platform:
            liste_user_platform.append(datas[i].platforme)
    return liste_user_platform

def render_data(mawakey:str, user_id:str, motif:str, table):
    datas = table.query.filter_by(user_id=user_id, platforme=motif).all()

    data = []
    for i in range(len(datas)):
        Round = list(logtraitement_de_donnees(datas[i].round))
        initial_vecteur = logtraitement_de_donnees(datas[i].vecteur_initial, mode="text")
        password = CodageMawa().mawaDecode(datas[i].password, mawakey, initial_vecteur, Round)

        data.append([i, datas[i].nom, password, datas[i].mail])
    
    return (data, len(datas))

def return_dir_elmt(dir):
    elmts = os.listdir(dir)
    for i in range(len(elmts)):
        elmts[i] = (elmts[i].split(".png"))[0]+","
    elmts = ''.join(elmts)
    return elmts

def render_email(id:int, table):
    user = table.query.filter_by(id=id).first()
    return user.mail
        