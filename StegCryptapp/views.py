from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from . import PasswordGenerator, Steganographie,  rsa, user_manager, data_processing, data_manager
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from datetime import datetime
from io import BytesIO
import os

UPLOAD_FOLDER = "StegCryptapp/uploads_files"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(200), nullable=False, unique=True)
    master_password = db.Column(db.String(200), nullable=False)
    rsa_public_key = db.Column(db.String(200), nullable=False)
    rsa_privet_key = db.Column(db.String(200), nullable=False)
    Mawakey = db.Column(db.String(200), nullable=False)
    vecteur_initial = db.Column(db.String(200), nullable=False)
    round = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nom, master_password, rsa_public_key, rsa_privet_key, Mawakey, vecteur_initial, round, mail):
        self.nom = nom
        self.master_password = master_password
        self.rsa_public_key = rsa_public_key
        self.rsa_privet_key = rsa_privet_key
        self.Mawakey = Mawakey
        self.vecteur_initial = vecteur_initial
        self.round = round
        self.mail = mail

class PasswordManager(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    platforme = db.Column(db.String(200), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mail = db.Column(db.String(200), nullable=True)
    round = db.Column(db.String(200), nullable=False)
    vecteur_initial = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, platforme, nom, password, mail, round, vecteur_initial):
        self.user_id = user_id
        self.platforme = platforme
        self.nom = nom
        self.password = password
        self.mail = mail
        self.round = round
        self.vecteur_initial = vecteur_initial

def t_init_db():
    db.drop_all()
    db.create_all()

#-/*/ ID-position: Pages Principaux -/*/

@app.route('/')
def acceuil():
    if "CONNECTED" in session:
        return render_template("accueil.html", connected=session['CONNECTED'], Username=session['USER_NAME'])
    return render_template("accueil.html", connected=False)

@app.route('/Sigin', methods=["GET", "POST"])
def Sigin():
    if "CONNECTED" in session:
        return redirect(url_for("acceuil"))
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]
        mail = request.form["mail"]
        data_user = user_manager.signin(username, password, mail, User, db)
        if data_user:
            session['CONNECTED'] = True
            session['USER_NAME'] = username
            session["USER_ID"] = data_user["ID"]
            session["USER_MAWA_KEY"] = data_user["CadageMawa"]
            session["USER_RSA_PRIVED_KEY"] = data_user["RSA"]["key priver"]
            session["USER_RSA_PUBLIC_KEY"] = data_user["RSA"]["key publique"]
            return redirect(url_for("acceuil"))
        else:
            flash("Nom déjà utilisé !", 'error')
            return redirect(request.url)
    return render_template('s_inscrire.html')

@app.route('/Login', methods=["GET", "POST"])
def Login():
    if "CONNECTED" in session:
        return redirect(url_for("acceuil"))
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]
        data_user = user_manager.login(username, password, User)
        if data_user:
            session['CONNECTED'] = True
            session['USER_NAME'] = username
            session["USER_ID"] = data_user["ID"]
            session["USER_MAWA_KEY"] = data_user["CadageMawa"]
            session["USER_RSA_PRIVED_KEY"] = data_user["RSA"]["key priver"]
            session["USER_RSA_PUBLIC_KEY"] = data_user["RSA"]["key publique"]
            return redirect(url_for("acceuil"))
        else:
            flash("Mot de passe ou identifiant Incorrecte !", 'error')
            return redirect(request.url)
    return render_template('authentification.html')

@app.route("/Logout")
def logout():
    if "CONNECTED" in session:
        session.pop('CONNECTED', None)
        session.pop('USER_NAME', None)
        session.pop("USER_ID", None)
        session.pop("USER_MAWA_KEY", None)
        session.pop("USER_RSA_PRIVED_KEY", None)
        session.pop("USER_RSA_PUBLIC_KEY", None)
    return redirect(url_for("acceuil"))

@app.route("/User", methods=["GET", "POST"])
def user():
    if "CONNECTED" in session:
        if request.method == "POST":
            mode = request.form["mode"]
            if mode == "DECONNEXION":
                return redirect(url_for("logout"))
            elif mode == "MODIFIER":
                username = request.form["username"]
                mail = request.form["mail"]
                changed = user_manager.change_name_mail(session["USER_ID"], username,  mail, User, db)
                if changed:
                    session['USER_NAME'] = username
                    return redirect(url_for("user"))
                else:
                    return render_template("user.html", connected=session['CONNECTED'], Username=session['USER_NAME'], text="désolé nom déjà utiliser")
            elif mode == "DELT":
                user_manager.delt_user(session["USER_ID"], User, db)
                data_manager.delt_user_data(session["USER_ID"], PasswordManager, db)
                return redirect(url_for("logout"))
            elif mode == "CHANGE_PASSWORD":
                return redirect(url_for("change_password"))
        return render_template("user.html", connected=session['CONNECTED'], Username=session['USER_NAME'], mail=data_processing.render_email(session["USER_ID"], User))
    return redirect(url_for("acceuil"))

@app.route("/Change_password", methods=["GET", "POST"])
def change_password():
    if "CONNECTED" in session:
        if request.method == "POST":
            password = request.form["password"]
            new_password = request.form["new_password"]
            changed = user_manager.change_password(session["USER_ID"], session["USER_NAME"], password, new_password, User, db)
            if changed:
                return redirect(url_for("acceuil"))
            else:
                flash("Mot de passe incorrect!", 'error')
                return redirect(request.url)
        return render_template("change_password.html", connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))



#-/*/ ID-position: StegCrypt -/*/

@app.route('/Tableau-de-bord', methods=["GET", "POST"])
def tableauDeBord():
    if "CONNECTED" in session:
        if request.method == "POST":
            platforme = request.form["input"]
            datas, number = data_processing.render_data(session["USER_MAWA_KEY"], session["USER_ID"], platforme, PasswordManager)
            return render_template('print.html', data=datas, platform=platforme, connected=session['CONNECTED'], Username=session['USER_NAME'], length=number)
        return render_template("tableau-de-bord.html", add=data_processing.render_data__section(session["USER_ID"], PasswordManager), connected=session['CONNECTED'], Username=session['USER_NAME'],)
    return redirect(url_for("acceuil"))

@app.route('/Print', methods=["GET", "POST"])
def printer():
    if "CONNECTED" in session:
        if request.method == "POST":
            length = int(request.form["len"])
            platforme = request.form["hidden"]
            mode = request.form["mode"]
            new_user_data = []
            if mode == "MODIFIER":
                for i in range(length):
                    if request.form[f"inputTable1{i}"]:
                        new_user_data.append([request.form[f"inputTable0{i}"], request.form[f"inputTable1{i}"], request.form[f"inputTable2{i}"]])
                data_manager.change_data(session["USER_ID"], new_user_data, platforme, session["USER_MAWA_KEY"], PasswordManager, db)
                return redirect(url_for("tableauDeBord"))
            elif mode == "ADD":
                return render_template('add_password.html', connected=session['CONNECTED'], Username=session['USER_NAME'], platforme=platforme, mail=data_processing.render_email(session["USER_ID"], User), password_th=PasswordGenerator.PasswordGenerator(32))
            else:
                data_manager.delt_all(session["USER_ID"], platforme, PasswordManager, db)
            return redirect(url_for("tableauDeBord"))
    return redirect(url_for("acceuil"))

@app.route('/Add_password', methods=["GET", "POST"])
def add_password():
    if "CONNECTED" in session:
        if request.method == "POST":
            platforme = request.form["platform"]
            pseudo = request.form["pseudo"]
            password = request.form["password"]
            mail = request.form["mail"]
            if not os.path.exists("StegCryptapp/static/images/logo/"+platforme.capitalize()+".png") and request.files["logoplatform"]:
                file = request.files["logoplatform"]
                if data_manager.allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]):
                    file.save("StegCryptapp/static/images/logo/"+platforme.capitalize()+".png")
            data_manager.save_data_from_form(platforme, pseudo, password, mail, session["USER_ID"], session["USER_MAWA_KEY"], PasswordManager, db)
            return redirect(url_for("tableauDeBord"))
        return render_template("add_password.html", connected=session['CONNECTED'], Username=session['USER_NAME'], mail=data_processing.render_email(session["USER_ID"], User), password_th=PasswordGenerator.PasswordGenerator(32))
    return redirect(url_for("acceuil"))

#-/*/* ID-position: StegCrypt other-password-manager -/*/

#-/*/ ID-position: StegCrypt other-password-manager - Steg- stéganographie -/*/

@app.route('/Steganographie', methods=["GET", "POST"])
def steganographie():
    if "CONNECTED" in session:
        return render_template('steganographie/portal-stéganographie.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Steganographie/Text', methods=['GET', 'POST'])
def stegtext():
    if "CONNECTED" in session:
        return render_template('/steganographie/portal_text.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))


@app.route('/Steganographie/Text/Cacher', methods=['GET', 'POST'])
def stegtextcacher():
    if "CONNECTED" in session:
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            text = request.form['textarea']
            print(text)
            if 'image1' not in request.files:
                flash('Aucun fichier partager !', 'error')
                return redirect(request.url)
            file = request.files["image1"]
            if file.filename == '':
                flash("Aucun fichier selectionné !", 'error')
                return redirect(request.url)
            elif data_manager.allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                file_path = app.config['UPLOAD_FOLDER']+"/"+filename
                file.save(file_path)
                if data_manager.is_image(file_path):
                    file_path = data_manager.this_type_to_png_image(file_path)
                    try:
                        img_io = BytesIO()
                        my_steg.hideTextInImage(text, file_path).save(img_io,'PNG')
                        img_io.seek(0)
                        os.remove(file_path)
                        return send_file(img_io, as_attachment=True, download_name=filename)
                    except:
                        pass
            if os.path.exists(file_path):
                os.remove(file_path)
            flash("Fichier incompatible !", 'error')
            return redirect(request.url)
        return render_template('/steganographie/hide_text.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Steganographie/Text/Retrouver', methods=['GET', 'POST'])
def stegtextfind():
    if "CONNECTED" in session:
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            if 'image1' not in request.files:
                flash('Aucun fichier partager !', 'error')
                return redirect(request.url)
            file = request.files["image1"]
            if file.filename == '':
                flash("Aucun fichier selectionné !", 'error')
                return redirect(request.url)
            elif data_manager.allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                file_path = app.config['UPLOAD_FOLDER']+"/"+filename
                file.save(file_path)
                if data_manager.is_image(file_path):
                    try:
                        text = my_steg.findText(os.path.abspath(file_path))
                        print(text)
                        os.remove(file_path)
                        return render_template('/steganographie/find_text.html', text=text, connected=session['CONNECTED'], Username=session['USER_NAME'])
                    except:
                        pass
            if os.path.exists(file_path):
                os.remove(file_path)
            flash("Fichier incompatible !", 'error')
            return redirect(request.url)
        return render_template('/steganographie/find_text.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Steganographie/Image', methods=['GET', 'POST'])
def stegimage():
    if "CONNECTED" in session:
        return render_template('/steganographie/portal_image.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Steganographie/Image/Cacher', methods=['GET', 'POST'])
def stegimagecacher():
    if "CONNECTED" in session:
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            if 'image1' not in request.files and 'image2' not in request.files:
                flash('Aucun fichier partager !', 'error')
                return redirect(request.url)
            file = request.files["image1"]
            file2 = request.files["image2"]
            if file.filename == '' or file2.filename == '':
                flash("Aucun fichier selectionné !")
                return redirect(request.url)
            elif data_manager.allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]) and data_manager.allowed_file(file2.filename, app.config["ALLOWED_EXTENSIONS"]) :
                filename = secure_filename(file.filename)
                filename2 = secure_filename(file2.filename)
                file_path = app.config['UPLOAD_FOLDER']+"/"+filename
                file_path2 = app.config['UPLOAD_FOLDER']+"/"+filename2
                file.save(file_path)
                file2.save(file_path2)
                if data_manager.is_image(file_path) and data_manager.is_image(file_path2):
                    file_path = data_manager.this_type_to_png_image(file_path)
                    file_path2 = data_manager.this_type_to_png_image(file_path2)
                    try:
                        img_io = BytesIO()
                        my_steg.encodeImageByImage(file_path2, file_path).save(img_io,'PNG')
                        img_io.seek(0)
                        os.remove(file_path)
                        os.remove(file_path2)
                        return send_file(img_io, as_attachment=True, download_name=filename)
                    except:
                        pass
            if os.path.exists(file_path):
                os.remove(file_path)

            if os.path.exists(file_path2):
                os.remove(file_path2)

            flash("Fichier incompatible !", 'error')
            return redirect(request.url)
        return render_template('/steganographie/hide_image.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Steganographie/Image/Retrouver', methods=['GET', 'POST'])
def stegimageretrouver():
    if "CONNECTED" in session:
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            if 'image1' not in request.files:
                flash('Aucun fichier partager !', 'error')
                return redirect(request.url)
            file = request.files["image1"]
            if file.filename == '':
                flash("Aucun fichier selectionné !", 'error')
                return redirect(request.url)
            elif data_manager.allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                file_path = app.config['UPLOAD_FOLDER']+"/"+filename
                file.save(file_path)
                if data_manager.is_image(file_path):
                    try:
                        img_io = BytesIO()
                        my_steg.decodeImageByImage(file_path).save(img_io,'PNG')
                        img_io.seek(0)
                        os.remove(file_path)
                        return send_file(img_io, as_attachment=True, download_name=filename)
                    except:
                        pass
            if os.path.exists(file_path):
                os.remove(file_path)
            flash("Fichier incompatible !", 'error')
            return redirect(request.url)
        return render_template('/steganographie/find_image.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

#-/*/ ID-position: StegCrypt other-password-manager - Crypt- crypthographie -/*/

@app.route('/Crypthographie', methods=["GET", "POST"])
def chiffrer():
    if "CONNECTED" in session:
        return render_template('crypthographie/portal_cryptographie.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Crypthographie/Chiffrer', methods=["GET", "POST"])
def chiffreur():
    if "CONNECTED" in session:
        if request.method == "POST":
            text = request.form['textarea']
            my_rsa = rsa.RSA()
            return render_template('crypthographie/hide_text.html',connected=session['CONNECTED'], Username=session['USER_NAME'], text=my_rsa.chiffrement(session["USER_RSA_PUBLIC_KEY"][0], session["USER_RSA_PUBLIC_KEY"][1], text))
        return render_template('crypthographie/hide_text.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Crypthographie/Dechiffrer', methods=["GET", "POST"])
def dechiffreur():
    if "CONNECTED" in session:
        if request.method == "POST":
            text = request.form['textarea']
            my_rsa = rsa.RSA()
            return render_template('crypthographie/find_text.html',connected=session['CONNECTED'], Username=session['USER_NAME'], text=my_rsa.dechiffrement(session["USER_RSA_PRIVED_KEY"][0], session["USER_RSA_PRIVED_KEY"][1], text))
        return render_template('crypthographie/find_text.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

#-/*/ ID-position: Error Manager -/*/

@app.errorhandler(404)
def page_not_found(error):
    if "CONNECTED" in session:
        return render_template('errors.html', connected=session['CONNECTED'], Username=session['USER_NAME'], erros="404", message="Service indisponible"), 404
    return render_template('errors.html', connected=False, erros="404", message="Service indisponible"), 404

@app.errorhandler(500)
def page_on(error):
    if "CONNECTED" in session:
        return render_template('errors.html', connected=session['CONNECTED'], Username=session['USER_NAME'], erros="404", message="Service indisponible"), 500
    return render_template('errors.html', connected=False, erros="500", message="Service en réparation"), 500


# Administrateur

@app.route("/show-user", methods=["GET"])
def show_user():
    if "CONNECTED" in session and session['USER_NAME'] == "Administrateur1":
        user_manager.delt_user(2, User, db)
        data_manager.delt_user_data(2, PasswordManager, db)
        users = User.query.order_by(User.date_added)
        users_template = ""
        for user in users:
            users_template += f"<br>{user.id}|{user.nom}|{user.mail}<br>"
        return users_template
    return redirect(url_for("acceuil"))
