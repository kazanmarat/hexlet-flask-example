import json
import uuid
from flask import Flask, render_template, request, url_for, redirect
from flask import flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = "secret_key"

users = json.load(open('./users.json', 'r'))

@app.route('/')
def index():
    return 'Welcome to Flask!'

@app.get('/users/')
def users_get():
    filtered_users = []
    query = request.args.get('query', '')
    for user in users:
        if query in user['name']:
            filtered_users.append(user)

    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=query,
        messages=messages,
    )


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'users/new.html',
            user=user_data,
            errors=errors,
        )
    id = str(uuid.uuid4())
    user = {
        'id': id,
        'name': user_data['name'],
        'email': user_data['email']
    }
    users.append(user)
    with open("./users.json", "w") as f:
        json.dump(users, f)
    flash('User was added', 'success')
    return redirect(url_for('users_get'), code=302)


@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )

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

def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors
