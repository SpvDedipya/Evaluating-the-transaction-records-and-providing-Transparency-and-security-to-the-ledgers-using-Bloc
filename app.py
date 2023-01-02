from flask import Flask,redirect,url_for,render_template,request
#import libraries
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)

#code for connection
app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = ''#password
#in my case password is null so i am keeping empty
app.config['MYSQL_DB'] = 'blockchain'#database name


@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/Admin')
def Admin():
    return render_template('Admin.html')

@app.route('/Registration')
def Registrationpythom ():
    return render_template('Registration.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/Transaction')
def Transaction():
    return render_template('Transaction.html')

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
        else:
            #executing query to insert new data into MySQL
            cursor.execute('INSERT INTO details (firstName, lastName, email, uname, aadhar, password, city, state,zip,pkey) VALUES (% s,% s,% s,% s,% s,% s,% s,% s,% s,% s)', (firstName, lastName, email, uname, aadhar, password, city, state,zip,pkey))
            mysql.connection.commit()
            #displaying message
            msg = 'You have successfully registered !'
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
        
        email= request.form['email']
        password = request.form['password']
        #creating variable for connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM details WHERE email = % s', (email,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            msg = 'Success'
        else:
            #executing query to insert new data into MySQL
            msg="register"
    return render_template('Login.html', msg=msg)
    if __name__ == '__main__':
        app.run(port=5000,debug=True)


if __name__=='__main__':
    app.run(debug=True)