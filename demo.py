from flask import Flask,url_for,redirect
app = Flask(__name__)
@app.route("/")
def hai():
    return "welcome to klu"
@app.route("/hello")
def hello():
    return "hello world"
@app.route("/type/<desg>")
def desg(desg):
    return "<h1>welcome all "+desg+"to CAD class</h1>"
@app.route("/faculty")
def faculty():
    return "good morning all faculty members of KLU"
@app.route("/to/<person>")
def to(person):
    if person=="faculty":
        return redirect(url_for("faculty"))
    else:
        return redirect(url_for("desg",desg=person))


if __name__ =="__main__":
    app.run(debug=True)