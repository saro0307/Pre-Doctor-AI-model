from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        new_username = User.query.filter_by(username=username).first()
        new_email = User.query.filter_by(email=email).first()
        if new_username:
            flash("Username already exists! Please choose another...", category="error")
            # return redirect(url_for('auth.signup'))
        elif new_email:
            flash("Email already exists! Please choose another...", category="error")
            # return redirect(url_for("auth.signup"))
        elif len(username) < 5:
            flash("Username must include atleast 5 characters!", category="error")
        elif len(email) < 10:
            flash("Email is too short! Please enter another...", category="error")
        elif len(password) < 8:
            flash("Password must contain atleast 8 characters!", category="error")
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True if request.form.get('remember_me') == 'on' else False)
            flash("Account created successfully!", category="success")
            return redirect(url_for("views.home"))
        # return redirect(url_for("auth.signup"))
        # return "<h1>Done signup</h1>"
    return render_template("signup.html", user=current_user)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for('auth.login'))


# @auth.route('/', methods=['POST', 'GET'])
@auth.route('login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                flash("Logged in successfully!", category="success")
                # print(request.form.get('remember_me'))
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Password is incorrect!", category="error")
        else:
            flash("Username does not exist!", category="error")
        return redirect(url_for('auth.login'))
        # return "<h1>Done login</h1>"
    return render_template('login.html', user=current_user)
