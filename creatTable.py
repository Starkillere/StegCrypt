#-*-  coding:utf-8 -*-
import sqlite3

database = {'name':'database.db', 'Table':[{'name':'user', 'keys':['id', 'nom', 'master_password', 'rsa_public_key', 'rsa_privet_key', 'Mawakey', 'vecteur_initial', 'round', 'mail']}, {'name':'gestionnaire', 'keys':['id', 'platforme', 'nom', 'password', 'mail', 'round', 'vecteur_initial']}]}

"""    
       *** creattable.py ***
       Création des Table:
              - gestionnaire : contient tout les mot de passe et compte associé.
              - user : contient tout les utilisateur 
"""

def creat_gestionnaire_table():
       """
              *** creat_gestionnaire_table ***
       
              Création de la Table gestionnaire
              colonnes:
              --------
                     id: id de l'utilisateur
                     platforme: la platforme pour la quelle on souhaite enregistré notre mot de passe
                     nom: pseudo sur la platforme
                     password: notre mot de passe sur la platforme
                     mail: adresse mail utilisé sur la platforme
       """
       con = sqlite3.connect(database['name'])
       cursor = con.cursor()

       cursor.execute(f"""CREATE TABLE IF NOT EXISTS {database['Table'][1]['name']} (
                         {database['Table'][1]['keys'][0]} INTEGER NOT NULL,
                         {database['Table'][1]['keys'][1]} TEXT NOT NULL,
                         {database['Table'][1]['keys'][2]} TEXT NOT NULL,
                         {database['Table'][1]['keys'][3]} TEXT NOT NULL,
                         {database['Table'][1]['keys'][4]} TEXT,
                         {database['Table'][1]['keys'][5]} TEXT NOT NULL,
                         {database['Table'][1]['keys'][6]} TEXT NOT NULL
                  );""")
       con.commit()
       con.close() 

def creat_user_table():
       """
              *** creat_user_table ***
              Création de la Table user
              colonnes:
              ---------
                     id : position de l'utilisateur dans la table
                     nom: identifiant de l'utilisateur
                     master_password : mot de pass de l'utilisateur (hasher)
                     public_key: master key de l'utilisteur (chiffré)
                     privet_key:
       """
       con = sqlite3.connect(database['name'])
       cursor = con.cursor()
       
       cursor.execute(f"""CREATE TABLE IF NOT EXISTS {database['Table'][0]['name']} (
                         {database['Table'][0]['keys'][0]} INTEGER PRIMARY KEY AUTOINCREMENT,
                         {database['Table'][0]['keys'][1]} TEXT NOT NULL,
                         {database['Table'][0]['keys'][2]} TEXT NOT NULL,
                         {database['Table'][0]['keys'][3]} TEXT NOT NULL,
                         {database['Table'][0]['keys'][4]} TEXT NOT NULL,
                         {database['Table'][0]['keys'][5]} TEXT NOT NULL,
                         {database['Table'][0]['keys'][6]} TEXT NOT NULL,
                         {database['Table'][0]['keys'][7]} TEXT NOT NULL,
                         {database['Table'][0]['keys'][8]} TEXT NOT NULL
                  );""")
       con.commit()
       con.close()

def creat():      
       creat_gestionnaire_table()
       creat_user_table()
       return database