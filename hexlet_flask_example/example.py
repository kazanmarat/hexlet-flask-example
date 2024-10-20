from flask import Flask, render_template, request, url_for, redirect
from flask import flash, get_flashed_messages
from hexlet_flask_example.db_repository import UserRepository
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
repo = UserRepository(conn)

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route('/')
def index():
    return 'Welcome to Flask!'

@app.route('/users/')
def users_get():
    messages = get_flashed_messages(with_categories=True)
    term = request.args.get('query', '')
    if term:
        users = repo.get_by_term(term)
    else:
        users = repo.get_content()
    return render_template(
        'users/index.html',
        users=users,
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
    user = repo.find(id)
    if not user:
        return 'Page not found', 404
    return render_template(
        'users/show.html',
        user=user,
    )


@app.route('/users/<id>/edit')
def users_edit(id):
    user = repo.find(id)
    errors = []
    return render_template(
           'users/edit.html',
           user=user,
           errors=errors,
    )


@app.route('/users/<id>/patch', methods=['POST'])
def users_patch(id):
    user = repo.find(id)
    data = request.form.to_dict()
    data['email'] = user['email']

    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
        ), 422

    user['name'] = data['name']
    repo.save(user)
    flash('User has been updated', 'success')
    return redirect(url_for('users_get'))

@app.route('/users/<id>/delete', methods=['POST'])
def users_delete(id):
    repo.destroy(id)
    flash('user has been deleted', 'success')
    return redirect(url_for('users_get'))


def validate(user):
    errors = {}
    if len(user['name']) < 4:
        errors['name'] = "Nickname must be greater than 4 characters"
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors
