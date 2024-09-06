from flask import Blueprint, flash,render_template,url_for,request,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db 
from flask_login import logout_user,login_user,login_required

auth = Blueprint('auth',__name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',  methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        error_message = f"User with email '{email}' already exists!"
        return render_template('signup.html', error_message=error_message)

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()


    return redirect(url_for('auth.login'))  


@auth.route('/login_post',methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password,password=password):
        flash("Please enter correct credentials")
        redirect(url_for('auth.login'))

    login_user(user,remember=remember)





@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')

     
    


