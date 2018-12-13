import os

from flask import Flask, session, render_template
from flask_session import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from wtforms import Form, TextField, BooleanField, validators, PasswordField
from wtforms.validators import Required
from passlib.hash import sha256_crpyt

from MySQLdb import espace_string as thwart

from dbconnect import connection
import gc



app = Flask(__name__)

url_key = "s1s4LkplFPL33z93QsIGQ"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("signin.html")


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=3,max=15)])
    password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match!")])
    confirm = PasswordField('Repeat Password')
    termsOS = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Private Notive</a> (Lasty Updated Dec 2018)', [validators.Required()])



@app.route("/register/", methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            exe = c.execute("SELECT * FROM users WHERE username = (%s)", (thwart(username)))

            if int(len(x)) > 0:
                flash("That username already exists. Please choose another")
                return render_template("register.html", form=form)

            else:
                c.execute("INSERT INTO users (username, password, tracking) VALUES (%s, %s, %s)", (thwart(username), thwart(password), thwart(tracking("/book-review-webpage/"))))

                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = Username

                return redirect(url_for('menu'))
        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    app.run();
