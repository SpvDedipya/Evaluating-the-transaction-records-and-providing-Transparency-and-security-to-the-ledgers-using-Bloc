from flask import Flask,redirect,url_for,render_template,request
app=Flask(__name__)

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


if __name__=='__main__':
    app.run(debug=True)