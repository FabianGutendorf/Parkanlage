from flask import Flask, url_for, request, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'Parkanlage.db'

# init DB
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        return db

# close DB
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# execute Query
def query_db(query, args=(), one = False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv # return the first entry if "one" is set, else return all 



## Routing

@app.route("/")
@app.route("/index")
def index(): #index html
    return render_template('index.html', 
        login_path=url_for("login"),
        project_path=url_for("database"), 
        req_path=url_for("requirements"))
        # add params here
        
@app.route("/login") #login form, user input
def login():
    return render_template('login.html', param="Test")

@app.route("/requirements") # requirements for the project
def requirements():
    return render_template('requirements.html')

@app.route("/starter", methods= ['POST', 'GET']) #logged in form, notify user
def starter():
    name = ""
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.GET('name')
    
    return "logged " + name + " in"

@app.route("/database")
def database():

    result = ""
    for parker in query_db('SELECT * FROM Parker'):
        result += parker['Kennzeichen']

    return render_template('database.html', req_path=result)

# Main start
if __name__ == '__main__':
    app.run(port=4698, debug=True)