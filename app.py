from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hello/', methods=['GET', 'POST'])
def welcome_hello():
    return "Hello World!"


@app.route('/')
def welcome():
    return render_template("index.html")


@app.route('/<string:name>/')
def hello(name):
    return "Hello " + name


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

