from flask import Blueprint,render_template,request,flash,redirect,url_for
from sqlalchemy.exc import IntegrityError
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user
from . import database
from .models import *

auth = Blueprint('auth', __name__)


@auth.route('/admin/', methods=('POST', 'GET'))
def admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, role=UserStatusEnum.admin).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials provided. Please check your login details and try again.')
            return redirect(url_for('auth.admin'))
        
        login_user(user)
        return redirect(url_for('main.dashboard'))  # Change to your admin dashboard route
    
    return render_template('auth/admin_login.html')



@auth.route('/login/',methods=('POST','GET'))
def login():
    if request.method == 'POST':
        email= request.form['email']
        password=request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            print(check_password_hash(user.password, password))
            flash('Invalid credentials provided, please check your login details and try again.')
            return redirect(url_for('auth.login')) 
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('auth/login.html')

@auth.route('/register/',methods=('POST','GET'))
def signup():
    try:
        if request.method == 'POST':
            first_name   = request.form['first_name']
            last_name    = request.form['last_name']
            email       = request.form['email']
            phone       = request.form['phone']
            password    = request.form['password']
            password2   = request.form['confirmpassword']
            
            user = User.query.filter_by(email=email).first() 
            if user: # if a user is found, we want to redirect back to signup page so user can try again
                flash('User with that email already exists')    
                return redirect(url_for('auth.signup'))
            
            if password == password2:
                user = User( 
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email,phone=phone,
                    password = generate_password_hash(password)
                    )
                # print('user:---------------------:', user)
                database.session.add(user)
                database.session.commit()
                flash('Created account successfully!')
                return redirect(url_for('auth.login'))
            
            flash('The two passwords did not match')
            return redirect(url_for('auth.signup'))
    except IntegrityError:
        flash('UNIQUE constraint failed: ensure you are not using a phone or email that is already registered with another user')
        return redirect(url_for('auth.signup'))
        
    return render_template('auth/signup.html')
     
  

@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


 