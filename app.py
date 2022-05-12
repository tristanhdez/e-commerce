from flask import Flask, redirect, render_template, request, session, url_for
import mysql.connector
from functools import wraps
from datetime import timedelta
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key:)'
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='Password123*'
app.config['MYSQL_DATABASE_DB']='ecommerce'
mysql.init_app(app)
connection = mysql.connect()
cursor=connection.cursor()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and 'username' in session:
            return f(*args, **kwargs)
        else:
           return "Incorrect"
    return wrap

@app.route('/index')
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
@app.route('/my_profile')
def my_profile():
    connection = mysql.connect()
    cursor = connection.cursor()
    username= session['username']
    cursor.execute('SELECT id from user where username=%s', (username))
    id_user = cursor.fetchone()
    print(id_user)

    sql = "SELECT * from user where id=%s";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, id_user)
    data = cursor.fetchall()
    connection.commit()
    return render_template("my_profile.html",data=data, id_user=id_user)


@login_required
@app.route('/edit-profile/<int:id_user>')
def edit_profile(id_user):
    sql = "SELECT * from user where id=%s";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, id_user)
    data = cursor.fetchall()
    connection.commit()
    return render_template("edit_profile.html", data=data)

@login_required
@app.route('/editing_profile',methods=['POST'])
def editing_profile():
    if request.method == 'POST':
        id_user = request.form.get("id_user")
        username=request.form['username']
        name=request.form['name']
        last_name=request.form['last_name']
        gmail=request.form['gmail']
        password=request.form['password']
        age = request.form['age']
        birthday = request.form['birthday']
        id_gender = request.form.get("id_gender", False)
        adress=request.form['adress']
        tel=request.form['tel']
        mobile_number = request.form.get("mobile_number")
        

        sql = "UPDATE `user` SET `username` = (%s), `name` = (%s), `last_name` = (%s), `email` = (%s), `password` = (%s), `birthday` = (%s), `id_gender` = (%s), `address` = (%s), `tel` = (%s), `mobile_number` = (%s) WHERE `user`.`id` = (%s);"
        data =(
            username,name,last_name,
            gmail,password,age,birthday,
            id_gender,adress,tel,
            mobile_number,id_user,
        )
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute(sql,data)
        connection.commit()
        cursor.fetchone()
        msg = "Profile Edited"
    return render_template("profile_edited.html", msg=msg)

@login_required
@app.route('/delete-account/<int:id_user>/')
def delete_acount(id_user):
    sql = "DELETE FROM user WHERE `user`.`id` =%s";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, id_user)
    cursor.fetchall()
    connection.commit()
    msg = "Account Deleted"
    session.pop('leggedin',None)
    session.pop('username',None)
    session.permanent = False
    session.clear()
    return render_template("account_deleted.html", msg=msg)

@login_required
@app.route('/electronic')
def electronic():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO `electronic_view` (`id`,`view`) VALUES (NULL,1);"
    cursor.execute(sql)
    connection.commit()

    sql = "SELECT * FROM product WHERE id_category=1";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()
    
    return render_template("electronic.html", data=data)


@login_required
@app.route('/item_pets')
def item_pets():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO `item_pets_view` (`id`,`view`) VALUES (NULL,1);"
    cursor.execute(sql)
    connection.commit()

    sql = "SELECT * FROM product WHERE id_category=3";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()
    return render_template("item_pets.html", data=data)


@login_required
@app.route('/my_cart')
def my_cart():
    connection = mysql.connect()
    cursor = connection.cursor()
    username= session['username']
    cursor.execute('SELECT id from user where username=%s', (username))
    id_user = cursor.fetchone()
    print(id_user)

    sql = "SELECT * from cart where id_user=%s";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, id_user)
    data = cursor.fetchall()
    connection.commit()
    return render_template("my_cart.html", data=data)


@login_required
@app.route('/womens_fashion')
def womens_fashion():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO `womens_fashion_view` (`id`,`view`) VALUES (NULL,1);"
    cursor.execute(sql)
    connection.commit()


    sql = "SELECT * FROM product WHERE id_category=5";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()
    return render_template("womens_fashion.html", data=data)


@login_required
@app.route('/mens_fashion')
def mens_fashion():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO `mens_fashion_view` (`id`,`view`) VALUES (NULL,1);"
    cursor.execute(sql)
    connection.commit()

    sql = "SELECT * FROM product WHERE id_category=6";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()

    return render_template("mens_fashion.html",data=data)


@login_required
@app.route('/videogames')
def videogames():
    sql = "SELECT * FROM product WHERE id_category=4";
    connection= mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.commit()

    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO `videogames_view` (`id`,`view`) VALUES (NULL,1);"
    cursor.execute(sql)
    connection.commit()
    return render_template("videogames.html", data=data)

@login_required
@app.route('/add-to-cart/<int:id_product>/')
def add_to_cart(id_product):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        username= session['username']
        cursor.execute('SELECT id from user where username=%s', (username))
        id_user = cursor.fetchone()
        print(id_user)

        connection = mysql.connect()
        cursor = connection.cursor()
        sql = "INSERT INTO `cart` (`id`,`id_user`, `id_product`, `date`) VALUES (NULL, %s, %s, NULL);"
        data = (id_user, id_product)
        cursor.execute(sql,data)
        connection.commit()
        return render_template('added_cart.html', data = data)
    except KeyError as e:
        print(e)


@login_required
@app.route('/home')
def home():
    return render_template('home.html', username= session['username'])


@app.route('/new-user',methods=['POST'])
def new_user():
    if request.method == 'POST':
        username=request.form['username']
        name=request.form['name']
        last_name=request.form['last_name']
        email=request.form['email']
        password=request.form['password']
        password_verify=request.form['password_verify']
        age = request.form['age']
        id_gender=request.form['id_gender']
        birthday = request.form.get("birthday")
        adress=request.form['adress']
        tel=request.form['tel']
        mobile_number=request.form['mobile_number']
        if password == password_verify:
            connection = mysql.connect()
            cursor= connection.cursor()
            sql = "INSERT INTO `user` (`id`, `username`, `name`, `last_name`, `email`, `password`, `age`, `birthday`, `id_gender`, `address`, `tel`, `mobile_number`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            data = (username, name, last_name, email, password, age, birthday, id_gender, adress, tel, mobile_number)
            cursor.execute(sql,data)
            connection.commit()
            cursor.close()
            connection.close()
            return render_template('signin_sucess.html')
        else:
            msg="Password doesn't match please, try again"
            return render_template('signin.html', msg=msg)
    return

@app.route('/verify',methods=['GET','POST'])
def verify():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        connection = mysql.connect()
        cursor=connection.cursor()
        cursor.execute("SELECT `user`.`username` FROM `user` WHERE `user`.`username`='"+username+"'")
        connection.commit()
        data = cursor.fetchall()
        result = " ".join(str(x) for x in data)
        result = result.replace("(","").replace(")","").replace(","," ").replace(" ","").replace("'","")
        print(result)
        if result == username:
            connection = mysql.connect()
            cursor=connection.cursor()
            cursor.execute("SELECT `user`.`password` FROM `user` WHERE `user`.`username`='"+username+"'")
            connection.commit()
            data = cursor.fetchall()
            result2 = " ".join(str(x) for x in data)
            result2 = result2.replace("(","").replace(")","").replace(","," ").replace(" ","").replace("'","")
            print(result2)
            if result2 == password:
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
                return redirect(url_for('home'))
    msg="Username or Password Incorrect. \nTry Again"
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('leggedin',None)
    session.pop('username',None)
    session.clear()
    session.permanent = False
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True) 
