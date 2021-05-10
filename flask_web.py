from flask import Flask, Response, render_template,redirect,request,url_for,flash,session
import wtforms
from flask_mysqldb import MySQL

class RegisterForm(wtforms.Form):
    name = wtforms.StringField("İsim",validators=[wtforms.validators.DataRequired()])

    username = wtforms.StringField("Kullanıcı Adı",validators=[wtforms.validators.DataRequired(),wtforms.validators.Length(min=6,max=25)])

    email = wtforms.StringField("Email",validators=[wtforms.validators.Email(),wtforms.validators.DataRequired()])

    password = wtforms.PasswordField("Parola",validators=[wtforms.validators.DataRequired()])


class LoginForm(wtforms.Form):
    username = wtforms.StringField("Kullanıcı Adı",validators=[wtforms.validators.DataRequired(),wtforms.validators.Length(min=6,max=25)])

    password = wtforms.PasswordField("Parola",validators=[wtforms.validators.DataRequired()])
    
class butonlar(wtforms.Form):
    ileri = wtforms.RadioField("")


app = Flask(__name__)

app.secret_key = "kamera"

mysql = MySQL(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "kamera"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

yon = 0


@app.route("/", methods=["GET","POST"])
def anasayfa():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        usernameLogin = form.username.data
        passwordLogin = form.password.data
        
        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM users WHERE username = %s"
        result = cursor.execute(sorgu,(usernameLogin,))
        if result > 0:
            data = cursor.fetchone()
            password = data["password"]
            if passwordLogin == password:
                session["logged_in"] = True
                session["username"] = usernameLogin
                flash("Giriş Başarılı","success")
                return redirect(url_for("kullanıcı"))

            else:
                flash("Şifre Hatalı!","danger")
                return render_template("anasayfa.html",form =form)
        else:
            flash("Kullanıcı Adı Hatalı!","danger")
            return redirect(url_for("anasayfa"))

    else:
        return render_template("anasayfa.html",form =form)


@app.route("/cam")
def cam():
    return Response()


@app.route("/kullanıcı", methods= ["GET","POST"])
def kullanıcı():
    if session["logged_in"] == True:
        return render_template("kullanıcı.html")
    else:
        return redirect(url_for("anasayfa"))

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        usernme = form.username.data
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        kayit = "INSERT INTO users(name,username,email,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(kayit,(name,usernme,email,password))
        mysql.connection.commit()
        cursor.close()
        flash("kayıt İşlemi Başarılı","success")
        return redirect(url_for("anasayfa"))
    else:
        return render_template("register.html", form=form)


@app.route("/ileri")
def ileri():
    global yon
    yon = 1   
    return render_template("kullanıcı.html")
    

@app.route("/sol")
def sol():
    global yon
    yon = 2
    return render_template("kullanıcı.html")
@app.route("/sağ")
def sağ():
    global yon
    yon = 3
    return render_template("kullanıcı.html")
@app.route("/dur")
def dur():
    global yon
    yon = 0
    return render_template("kullanıcı.html")

@app.route("/move")
def move():
    global yon
    print(yon)
    return render_template("move.html",yon = yon)

if __name__ == "__main__":
    app.run(debug=True)
    