import json
import uuid
from flask import Flask, render_template, request, url_for, redirect
from flask import flash, get_flashed_messages
from user_repository import UserRepository

app = Flask(__name__)
app.secret_key = "secret_key"

users = json.load(open('./users.json', 'r'))

@app.route('/')
def index():
    return 'Welcome to Flask!'

@app.route('/users/')
def users_get():
    messages = get_flashed_messages(with_categories=True)
    term = request.args.get('term', '')
    repo = UserRepository()
    users = repo.get_content()
    filtered_users = [user for user in users if term in user['name']]
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=term,
        messages=messages
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
    repo = UserRepository()
    repo.save(user_data)
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


@app.route('/users/<id>')
def users_show(id):
    repo = UserRepository()
    user = repo.find(id)

    if not user:
        return 'Page not found', 404

    return render_template(
        'users/show.html',
        user=user,
    )

def validate(user):
    errors = {}
    if len(user['name']) <= 4:
        errors['name'] = "Nickname must be greater than 4 characters"
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors
