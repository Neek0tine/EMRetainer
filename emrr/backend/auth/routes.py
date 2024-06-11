from flask import render_template, redirect, url_for, flash, request, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from backend.auth import app, db, bcrypt
from backend.auth.dbmodel import Staff
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(username=form.username.data).first()
        if staff and bcrypt.check_password_hash(staff.password_salted, form.password.data):
            login_user(staff, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Email atau Password salah, mohon periksa ulang!', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@app.route('/scanner', methods=['GET', 'POST'])
@login_required
def scanner():
    if request.method == 'POST':
        # Process the form data here
        data = request.form
        # Add code to handle the data as needed
        return 'Form data submitted'
    return render_template('submit.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

from backend.auth.func import create_dummy_all, remove_dummy_staff, reset_database

@app.route('/create_dummy')
def create_dummy():
    create_dummy_all()
    return 'Dummy staff created'

@app.route('/remove_dummy')
def remove_dummy():
    remove_dummy_staff()
    return 'Dummy staff removed'

@app.route('/hard_reset')
def hard_reset():
    reset_database()
    return 'Everything resetted'

@app.route('/rmrf')
def delete_db():
    db.drop_all()
    return 'Everything removed'

@app.route('/mkdir')
def create_db():
    db.create_all()
    return 'Created from db schema.'