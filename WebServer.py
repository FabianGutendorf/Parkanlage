from flask import Flask, url_for, request, render_template

app = Flask(__name__)

@app.route("/")
def hello(): #index html
    return render_template('index.html', 
        login_path=url_for("input"), 
        req_path=url_for("requirements"))
        # add params here


@app.route("/input") #login form, user input
def input():
    return render_template('login.html', param="Test")

@app.route("/requirements") # requirements for the project
def requirements():
    return render_template('requirements.html')

@app.route("/login", methods= ['POST', 'GET']) #logged in form, notify user
def login():
    name = ""
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.GET('name')

    return "logged " + name + " in"



if __name__ == '__main__':
    app.run(port=4698, debug=True)