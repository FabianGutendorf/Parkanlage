
from flask import Flask, url_for, request

app = Flask(__name__)

@app.route("/")
def hello():
    return '<a href=' + url_for("test") + '>Zum Login</a>'

@app.route("/test") #HTML Formular
def test():
    return '''
        <html>
            <body>
                <form action = "http://localhost:4698/login" method = "post">
                    <p>Name:</p>
                    <p><input type = "text" name = "name" /></p>
                    <p><input type = "submit" value = "submit" /></p>
                </form>
            </body>
        </html>
    '''

@app.route("/login", methods= ['POST', 'GET'])
def login():
    name = ""
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.GET('name')

    return "logged " + name + " in"


if __name__ == '__main__':
    app.run(port=4698, debug=True)