from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models.user import User
from flask_app.models.grocery import Grocery
from datetime import datetime

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    user = User.get_by_id(session['user_id']) 
    if not user:
        return redirect('/login')
    need_groceries = Grocery.get_need(session['user_id'])
    bought_groceries = Grocery.get_bought(session['user_id'])
    return render_template('dashboard.html', user=user, need_groceries=need_groceries, bought_groceries=bought_groceries)

@app.route('/new_grocery', methods=['GET'])
def make_grocery():
    user = User.get_by_id(session['user_id'])
    return render_template('add.html', user=user)

@app.route('/submit_grocery', methods=['POST'])
def make_grocery_process():
    if 'user_id' not in session:
        return redirect('/login')
    
    data = {
        "item": request.form["item"],
        "type": request.form["type"],
        "brand": request.form["brand"],
        "person": request.form["person"],
        "need": 0,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "user_id": session['user_id'],
        "bought": False
    }
    Grocery.make_grocery(data)

    return redirect('/dashboard')

@app.route('/grocery/<int:id>/edit', methods=['GET'])
def show_grocery(id):
    if 'user_id' not in session:
        return redirect('/login')
    grocery = Grocery.get_one(id)
    user = User.get_by_id(session['user_id'])
    return render_template('edit.html', grocery=grocery, user=user)

@app.route('/grocery/<int:id>/delete')
def delete_grocery(id):
    if 'user_id' not in session:
        return redirect('/login')
    grocery = Grocery.get_one(id)
    if not grocery or grocery.user_id != session['user_id']:
        return redirect('/dashboard')
    Grocery.delete(id)
    return redirect('/dashboard')

@app.route('/grocery/<int:id>/update', methods=['POST'])
def update_grocery(id):
    if 'user_id' not in session:
        return redirect('/login')
    grocery = Grocery.get_one(id)
    if not grocery or grocery.user_id != session['user_id']:
        return redirect('/dashboard')
    data = Grocery.get_grocery_data_from_request(id, grocery)
    Grocery.update(id, data)
    return redirect('/dashboard')


@app.route('/grocery/<int:id>/buy')
def buy(id):
    grocery = Grocery.get_one(id)
    data = {
        "id": id,
        "need": 1 if not grocery.need else 0,
    }
    Grocery.buy(data)
    return redirect('/dashboard')

@app.route('/grocery/<int:id>/unbuy')
def unbuy(id):
    grocery = Grocery.get_one(id)
    data = {
        "id": id,
        "need": 0 if not grocery.need else 1,
    }
    Grocery.unbuy(data)
    return redirect('/dashboard')

@app.route('/grocery/<int:id>/view')
def view_grocery(id):
    grocery = Grocery.get_one(id)
    return render_template('view.html', grocery=grocery)