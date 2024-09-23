from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'

@app.get('/users')
def users_get():
    return 'GET /users'


@app.post('/users')
def users_post():
    return 'POST /users'
