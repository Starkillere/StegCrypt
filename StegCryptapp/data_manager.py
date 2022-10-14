#-*- conding:utf-8 -*-
from .CodageMawa import CodageMawa
from PIL import Image
from .user_manager import traitement_de_donnees
import os

def save_data_from_form(platform:str, pseudo:str, password:str, mail:str, user_id:int,  masterkey:str, table, db):
    my_pass = CodageMawa()
    Chiffred_password, vecteur_initial, Round = my_pass.mawaEncode(password, masterkey)
    cipher_Round = traitement_de_donnees(Round)
    cipher_vecteur_initial = traitement_de_donnees(vecteur_initial, mode="text")

    data = table(user_id=user_id, platforme=platform.capitalize(), nom=pseudo, password=Chiffred_password, mail=mail, round=cipher_Round, vecteur_initial=cipher_vecteur_initial)
    db.session.add(data)
    db.session.commit()
    return True
        

def change_data(user_id:int, data_liste:list, platforme:str, masterkey:str, table, db):
    datas = table.query.filter_by(user_id=user_id, platforme=platforme).all()
    for data in datas:
        db.session.delete(data)
    db.session.commit()
    
    for data in data_liste:
        save_data_from_form(platforme, data[0], data[1], data[2], user_id, masterkey, table, db)
    return True

def delt_all(user_id:int, platforme:str, table, db):
    datas = table.query.filter_by(user_id=user_id, platforme=platforme).all()
    for data in datas:
        db.session.delete(data)
    db.session.commit()
    return True

def delt_user_data(user_id:int, table, db):
    datas = table.query.filter_by(user_id=user_id).all()
    for data in datas:
        db.session.delete(data)
    db.session.commit()
    return True

def allowed_file(filename, allwed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allwed_extensions

def is_image(filename:str):
    try:
        image = Image.open(filename)
        image.verify()
    except:
        print("la")
        return False
    return True

def this_type_to_png_image(filename:str):
    img = Image.open(filename)
    new_filename = ('.'.join(filename.split('.')[:-1]))+".png"
    img.save(new_filename)
    os.remove(filename)
    return new_filename