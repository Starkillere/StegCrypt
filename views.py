from flask  import Flask, render_template, request, send_file, redirect, url_for, session
import os
import sys
from datetime import timedelta
#sys.path.append("../Algorithme")
import PasswordGenerator, rsa, Steganographie, user_manager, data_processing, data_manager

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(days=5)

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
        data_user = user_manager.signin(username, password, mail)
        if data_user:
            session['CONNECTED'] = True
            session['USER_NAME'] = username
            session["USER_ID"] = data_user["ID"]
            session["USER_MAWA_KEY"] = data_user["CadageMawa"]
            session["USER_RSA_PRIVED_KEY"] = data_user["RSA"]["key priver"]
            session["USER_RSA_PUBLIC_KEY"] = data_user["RSA"]["key publique"]
            return redirect(url_for("acceuil"))
        else:
            return render_template('s_inscrire.html', text="Nom déjà utilisé")
    return render_template('s_inscrire.html')

@app.route('/Login', methods=["GET", "POST"])
def Login():
    if "CONNECTED" in session:
        return redirect(url_for("acceuil"))
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]
        data_user = user_manager.login(username, password)
        if data_user:
            session['CONNECTED'] = True
            session['USER_NAME'] = username
            session["USER_ID"] = data_user["ID"]
            session["USER_MAWA_KEY"] = data_user["CadageMawa"]
            session["USER_RSA_PRIVED_KEY"] = data_user["RSA"]["key priver"]
            session["USER_RSA_PUBLIC_KEY"] = data_user["RSA"]["key publique"]
            return redirect(url_for("acceuil"))
        else:
            return render_template('authentification.html', text="Incorrecte")
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
                changed = user_manager.change_name_mail(session["USER_ID"], username, session["USER_NAME"], mail)
                if changed:
                    session['USER_NAME'] = username
                    return redirect(url_for("user"))
                else:
                    return render_template("user.html", connected=session['CONNECTED'], Username=session['USER_NAME'], text="désolé nom déjà utiliser")
            elif mode == "DELT":
                user_manager.delt_user(session["USER_ID"])
                data_manager.delt_user_data(session["USER_ID"])
                return redirect(url_for("logout"))
            elif mode == "CHANGE_PASSWORD":
                return redirect(url_for("change_password"))
        return render_template("user.html", connected=session['CONNECTED'], Username=session['USER_NAME'], mail=data_processing.render_email(session["USER_ID"]))
    return redirect(url_for("acceuil"))

@app.route("/Change_password", methods=["GET", "POST"])
def change_password():
    if "CONNECTED" in session:
        if request.method == "POST":
            password = request.form["password"]
            new_password = request.form["new_password"]
            changed = user_manager.change_password(session["USER_ID"], session["USER_NAME"], password, new_password)
            if changed:
                return redirect(url_for("acceuil"))
            else:
                return render_template("change_password.html", connected=session['CONNECTED'], Username=session['USER_NAME'], text="mot de passe incorrect")
        return render_template("change_password.html", connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))
#-/*/ ID-position: StegCrypt -/*/

@app.route('/Tableau-de-bord', methods=["GET", "POST"])
def tableauDeBord():
    if "CONNECTED" in session:
        if request.method == "POST":
            platforme = request.form["input"]
            datas, number = data_processing.render_data(session["USER_MAWA_KEY"], session["USER_ID"], platforme)
            return render_template('print.html', data=datas, platform=platforme, connected=session['CONNECTED'], Username=session['USER_NAME'], length=number)
        return render_template("tableau-de-bord.html", add=data_processing.render_data__section(session["USER_ID"]), connected=session['CONNECTED'], Username=session['USER_NAME'])
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
                data_manager.change_data(session["USER_ID"], new_user_data, platforme, session["USER_MAWA_KEY"])
                return redirect(url_for("tableauDeBord"))
            elif mode == "ADD":
                return render_template('add_password.html', connected=session['CONNECTED'], Username=session['USER_NAME'], platforme=platforme, mail=data_processing.render_email(session["USER_ID"]), password_th=PasswordGenerator.PasswordGenerator(32))
            else:
                data_manager.delt_all(session["USER_ID"], platforme)
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
            if not os.path.exists("static/images/logo/"+platforme.capitalize()+".png") and request.files["logoplatform"]:
                request.files["logoplatform"].save("static/images/logo/"+platforme.capitalize()+".png")
            data_manager.save_data_from_form(platforme, pseudo, password, mail, session["USER_ID"], session["USER_MAWA_KEY"])
            return redirect(url_for("tableauDeBord"))
        return render_template("add_password.html", connected=session['CONNECTED'], Username=session['USER_NAME'], mail=data_processing.render_email(session["USER_ID"]), password_th=PasswordGenerator.PasswordGenerator(32))
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
        if os.path.exists("Hidehote.png"):
            os.remove('Hidehote.png')
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            request.files["image1"].save("hote.png")
            text = request.form['textarea']
            my_steg.hideTextInImage(text ,'hote.png')
            if os.path.exists("hote.png"):
                os.remove('hote.png')
            return send_file("Hidehote.png", as_attachment=True)
        return render_template('/steganographie/hide_text.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Steganographie/Text/Retrouver', methods=['GET', 'POST'])
def stegtextfind():
    if "CONNECTED" in session:
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            request.files["image1"].save("hote.png")
            text = my_steg.findText('hote.png')
            if os.path.exists("hote.png"):
                os.remove('hote.png')
            return render_template('/steganographie/find_text.html', text=text, connected=session['CONNECTED'], Username=session['USER_NAME'])
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
        if os.path.exists("Hideimage.png"):
            os.remove("Hideimage.png")
        if os.path.exists("hote.png"):
            os.remove("hote.png")
        if os.path.exists("image.png"):
            os.remove("image.png")
        if os.path.exists("Clearimage.png"):
            os.remove("Clearimage.png")
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            request.files["image1"].save("hote.png")
            request.files["image2"].save("image.png")
            my_steg.encodeImageByImage("image.png","hote.png")
            if os.path.exists("hote.png"):
                os.remove("hote.png")
            if os.path.exists("Hideimage.png"):
                return send_file("Hideimage.png", as_attachment=True)
        return render_template('/steganographie/hide_image.html', connected=session['CONNECTED'], Username=session['USER_NAME'])
    return redirect(url_for("acceuil"))

@app.route('/Steganographie/Image/Retrouver', methods=['GET', 'POST'])
def stegimageretrouver():
    if "CONNECTED" in session:
        if os.path.exists("Clearimage.png"):
            os.remove("Clearimage.png")
        if request.method == "POST":
            my_steg = Steganographie.Steganographie()
            request.files["image1"].save("image.png")
            if os.path.exists("image.png"):
                my_steg.decodeImageByImage("image.png")
                os.remove("image.png")
            if os.path.exists("Clearimage.png"):
                return send_file("Clearimage.png", as_attachment=True)
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
        return render_template('404.html', connected=session['CONNECTED'], Username=session['USER_NAME']), 404
    return render_template('404.html', connected=False), 404
