from flask import Flask,render_template,request,session
import ibm_db
app=Flask(__name__)
app.secret_key="kvr@3132"
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;UID=jgs74786;PWD=ZWs6bzuQG5zzrVaP;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(ibm_db.active(conn))
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        global uname
        uname=request.form['username']
        pwd=request.form['password']
        print(uname,pwd)
        sql="SELECT * FROM REGISTER WHERE USERNAME=? AND PASSWORD=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,uname)
        ibm_db.bind_param(stmt,2,pwd)
        ibm_db.execute(stmt)
        out=ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['username']=uname
            session['email']=out['EMAIL']
            #global uname
            if out['ROLE']==0:
                return render_template("adminprofile.html",username=uname,emailid=out['EMAIL'])
            elif out['ROLE']==1:
                return render_template("studentprofile.html",username=uname,emailid=out['EMAIL'])
            else:
                return render_template("facultyprofile.html",username=uname,emailid=out['EMAIL'])
        else:
            msg='invalid credientilals'
            return render_template("login.html",message1=msg)

            
    return render_template("login.html")
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=="POST":
        uname=request.form['uname']
        pwd=request.form['pwd']
        email=request.form['email']
        role=request.form['role']
        print(uname,pwd,email,role)
        sql="SELECT * FROM REGISTER WHERE USERNAME=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,uname)
        ibm_db.execute(stmt)
        out=ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            msg="Already registered"
            return render_template("register.html",msg=msg)
        else:
            sql="INSERT INTO REGISTER VALUES(?,?,?,?)"
            stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt,1,uname)
            ibm_db.bind_param(stmt,2,pwd)
            ibm_db.bind_param(stmt,3,email)
            ibm_db.bind_param(stmt,4,role)
            ibm_db.execute(stmt)
            msg="successfully Registered"
            return render_template("register.html",msg=msg)

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')