
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world"

@app.route("/Test")
def test():
    return "Tets"


if __name__ == '__main__':
    app.run(port=4698, debug=True)