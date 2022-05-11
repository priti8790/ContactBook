from flask import Flask,render_template,request,session,redirect,flash,url_for
import sqlite3


app = Flask(__name__,static_url_path='/static')
app.secret_key = 'priti123'
con = sqlite3.connect("ContactBook.db")
con.execute("create table if not exists register(rid integer primary key,name text,address text,contact integer, mail text,password text)")


@app.route("/",methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        con = sqlite3.connect("ContactBook.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from register where mail=? and password=?", (mail, password))
        data = cur.fetchone()
        global id
        if data:
            session["mail"] = data["mail"]
            session["password"] = data["password"]
            session["name"] = data["name"]
            id = data["rid"]
            return redirect("dashboard")
    return redirect(url_for("dashboard"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            address = request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            password = request.form['password']
            con = sqlite3.connect("ContactBook.db")
            cur = con.cursor()
            cur.execute("insert into register(name,address,contact,mail,password)values(?,?,?,?,?)",
                        (name, address, contact, mail, password))
            con.commit()

        except Exception as e:
            print(e)
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('registration.html')


@app.route('/dashboard',methods = ['POST','GET'])
def dashboard():
    try:
        rows = None
        con = sqlite3.connect("ContactBook.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("Select * from usercontact")
        rows = cur.fetchall()

    except Exception as e:
        print(e)
    finally:
        return render_template("dashboard.html", rows=rows)
        con.close()
    #return render_template("dashboard.html")

@app.route('/new')
def new():
    return render_template("new.html")

@app.route('/add', methods=["GET", "POST"])
def add():
    try:
        con = sqlite3.connect("ContactBook.db")
        cur = con.cursor()
        command = "Create table if not exists usercontact(uid integer primary key, fullname text, relationship text,contact integer, address text,email text,rid integer not null, foreign key(rid) references register(rid) ) "
        cur.execute(command)
        con.commit()

        if request.method == 'POST':
            fname = request.form['fullname']
            rel = request.form['relationship']
            contact = request.form['contact']
            address = request.form['address']
            email = request.form['email']

            cur.execute("insert into usercontact(fullname,relationship,contact,address,email,rid)values(?,?,?,?,?,?)",
                        (fname, rel, contact, address, email, id))
            msg='Record saved successfully'
            con.commit()
            #return render_template('dashboard.html',msg)
    except Exception as e:
        con.rollback()
        msg = 'Error In Record saved'
    finally:
        #return render_template('dashboard.html',msg=msg)
        return redirect(url_for("dashboard"))
        con.close()

@app.route('/<int:uid>/edit',methods=["GET"])
def edit(uid):
    try:
        data=None
        con = sqlite3.connect("ContactBook.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from usercontact where uid=?",(uid,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        return render_template("edit.html",data=data)

@app.route('/<int:uid>/update', methods=["GET","POST"])
def update(uid):
    try:
        con = sqlite3.connect("ContactBook.db")
        cur = con.cursor()
        if request.method == 'POST':
            fname = request.form['fullname']
            rel = request.form['relationship']
            contact = request.form['contact']
            address = request.form['address']
            email = request.form['email']
            id = int(uid)
            print(id)
            cur.execute("update usercontact set fullname=?,relationship=?,contact=?,address=?,email=? where uid=?",
                    (fname, rel, contact, address, email, id,))
        msg = 'Record Updated successfully'
        con.commit()
    except Exception as e:
        con.rollback()
        msg = 'Error In Record saved'
    finally:
        return redirect(url_for("dashboard"))
        con.close()


@app.route('/<int:id>/delete',methods=["GET"])
def delete(id):
    con = sqlite3.connect("ContactBook.db")
    cur = con.cursor()
    cur.execute("Delete from usercontact where uid=?",(id,))
    con.commit()
    return redirect(url_for("dashboard"))

if __name__ == '__main__':
    app.run(debug=True)
