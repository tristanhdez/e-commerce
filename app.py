from flask import Flask, redirect, render_template, request, session, url_for
import mysql.connector
from functools import wraps
from datetime import timedelta


conn = mysql.connector.connect(
    host="bdjynruf6ziskqxualjp-mysql.services.clever-cloud.com", 
    port="3306", user="ugvjlyd2h3xtnj4v", 
    password="KFYYYo4kzDHYE2AnaZie", 
    database="bdjynruf6ziskqxualjp"
)


cursor= conn.cursor(buffered=True,dictionary=True)


app = Flask(__name__)
app.secret_key="secret key"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and 'username' in session:
            return f(*args, **kwargs)
        else:
           return "Incorrect"
    return wrap


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signin')
def signin():
    return render_template("signin.html")


@login_required
@app.route('/electronic')
def electronic():
    return render_template("electronic.html")


@login_required
@app.route('/item_pets')
def item_pets():
    return render_template("item_pets.html")


@login_required
@app.route('/womens_fashion')
def womens_fashion():
    return render_template("womens_fashion.html")


@login_required
@app.route('/mens_fashion')
def mens_fashion():
    return render_template("mens_fashion.html")


@login_required
@app.route('/videogames')
def videogames():
    return render_template("videogames.html")


@login_required
@app.route('/home')
def home():
    cursor.execute('SELECT * from Categories')
    value = cursor.fetchone()
    return render_template('home.html', value=value, username= session['username'])


@app.route('/verify',methods=['GET','POST'])
def verify():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor.execute('SELECT * from LoginUsers where User=%s and Password=%s', (username,password))
        record = cursor.fetchone()
        if record:
            session['logged_in']=True
            session['username']=username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=120)
            return redirect(url_for('home'))
        elif 'logged_in' in session:
            logout()
            session['logged_in']=True
            session['username']=username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=120)
            return redirect('home.html')
        else:
            msg="Username or Password Incorrect. \nTry Again"
            return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('leggedin',None)
    session.pop('username',None)
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True) 
