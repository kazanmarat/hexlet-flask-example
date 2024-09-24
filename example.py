from flask import Flask, render_template, request

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'mike'},
    {'id': 2, 'name': 'mishel'},
    {'id': 3, 'name': 'adel'},
    {'id': 4, 'name': 'keks'},
    {'id': 5, 'name': 'kamila'}
]

@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'

@app.get('/users/')
def users_get():
    filtered_users = []
    query = request.args.get('query', '')
    for user in users:
        if query in user['name']:
            filtered_users.append(user)

    return render_template(
        'users/index.html',
        users=filtered_users,
        search=query,
    )


@app.post('/users')
def user():
    return 'Users', 302

@app.route('/courses/<id>')
def courses_show(id):
    return f'Course id: {id}'

@app.route('/users/<id>')
def users_show(id):
    user = {
        'id': id,
        'name': f'user-{id}'
    }
    return render_template(
        'users/show.html',
        user=user,
    )

    
