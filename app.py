from flask import Flask,redirect,url_for,render_template,request,flash,session,g
#import libraries
# from flask import *
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import datetime

app=Flask(__name__)

#Sessions
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = datetime.timedelta(minutes=10)

#Executes before session activity (USED MIDDLEWARE)
@app.before_request
def before_request():
    g.user = None
 
    if 'user' in session:
        g.user = session['user']

#code for connection
app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = ''#password
#in my case password is null so i am keeping emptycd .venv
app.config['MYSQL_DB'] = 'blockchain'#database name


@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/Admin')
def Admin():
    if 'admin' in session and session['admin']:
        return render_template('Admin.html')
    return render_template('adLogin.html')

# @app.route('/adLogin')
# def AdLogin():
#     return render_template('adLogin.html')

@app.route('/Registration')
def Registrationpythom ():
    return render_template('Registration.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/Transaction')
def Transaction():
    return render_template('Transaction.html')

@app.route('/ethTrasaction')#eth transactions page...
def EthTransaction():
    if g.user or 'admin' in session and session['admin']:
        return render_template('eth_transactions.html')
    return render_template('Login.html')

@app.route('/addAccounts')#adding accounts in blockchain...
def AddAccounts():
    if 'admin' in session and session['admin']:
        return render_template('addAccounts.html')
    return render_template('adLogin.html')

@app.route('/viewGanacheAccounts')#listing ganacche accounts...
def ViewAccounts():
    if g.user or 'admin' in session and session['admin']:
        return render_template('ganache_accounts.html')
    return render_template('Login.html')

@app.route('/userDashboard')#listing ganacche accounts...
def userDashboard():
    if g.user:
        return render_template('user.html')
    return render_template('Login.html')
@app.route('/verify')#verifying accounts
def verify():
    if 'admin' in session and session['admin']:
        return render_template('account_verify.html')
    return render_template('adLogin.html')

@app.route('/dropsession')#dropping session
def dropsession():
    session.pop('user',None)
    return render_template('Login.html')
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('adLogin'))




'''@app.route('/Reg_submit',methods=['POST','GET'])
def Reg_submit():
    if request.method=='POST':'''

mysql = MySQL(app)

@app.route('/')

@app.route('/Registration',methods=['GET','POST'])
def projectreg():
    msg=''
    #applying empty validation
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'uname' in request.form and 'firstName' in request.form and 'lastName' in request.form and 'city' in request.form  and 'state' in request.form and 'zip' in request.form and 'aadhar' in request.form and 'pkey' in request.form :
        #passing HTML form data into python variable
        
        email= request.form['email']
        password = request.form['password']
        uname = request.form['uname']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']
        aadhar = request.form['aadhar']
        pkey = request.form['pkey']
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM details WHERE aadhar = % s', (aadhar,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            msg = 'Account already exists !'
            return redirect("/Login")
        else:
            #executing query to insert new data into MySQL
            cursor.execute('INSERT INTO details (firstName, lastName, email, uname, aadhar, password, city, state,zip,pkey) VALUES (% s,% s,% s,% s,% s,% s,% s,% s,% s,% s)', (firstName, lastName, email, uname, aadhar, password, city, state,zip,pkey))
            mysql.connection.commit()
            #displaying message
            msg = 'Successfully registered go to Login!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('Registration.html', msg=msg)
    if __name__ == '__main__':
        app.run(port=5000,debug=True)

@app.route('/')
@app.route('/Login',methods=['GET','POST'])
def projectlogin():
    msg=''
    #applying empty validation
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form :
        #passing HTML form data into python variable
        session.pop('user',None)
        email= request.form['email']
        password = request.form['password']
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM details WHERE email = % s', (email,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            cursor.execute('SELECT * FROM details WHERE email = % s and password=% s', (email,password))
            #fetching data from MySQL
            result1= cursor.fetchone()
            if result1:
                 msg='Successful'
                 session['user'] = request.form['email']
                 return redirect("/userDashboard")
            else:
                msg="wrong password"
        else:
            #executing query to insert new data into MySQL
            msg="register"

    return render_template('Login.html', msg=msg)
    if __name__ == '__main__':
        app.run(port=5000,debug=True)

#admin Login

@app.route('/adLogin', methods=['GET', 'POST'])
def adLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect(url_for('Admin'))
        else:
            return render_template('adLogin.html', message="Invalid credentials. Please try again.")
    else:
        return render_template('adLogin.html')

if __name__=='__main__':
    app.run(debug=True)