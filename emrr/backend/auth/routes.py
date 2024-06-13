from flask import render_template, redirect, url_for, flash, request, session, abort
from flask_login import login_user, current_user, logout_user, login_required
from backend.auth import app, db, bcrypt
from backend.auth.dbmodel import Staff, MedicalRecord
from flask_wtf import FlaskForm
import os
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
# from datetime import datetime

# Constants
UPLOAD_FOLDER = 'C:\\Users\\nicho\\Documents\\8th Semester\\Machine Learning\\EMRetainer\\emrr\\emr'  # Adjust this path
ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    search_query = request.form.get('search_query', '').strip()
    if request.method == 'POST' and search_query:
        records = MedicalRecord.query.filter(
            (MedicalRecord.patient_name.ilike(f"%{search_query}%")) |
            (MedicalRecord.medical_record_number.ilike(f"%{search_query}%")) |
            (MedicalRecord.recent_specialization.ilike(f"%{search_query}%")) |
            (MedicalRecord.main_diagnosis.ilike(f"%{search_query}%"))
        ).limit(1).all()
    else:
        records = MedicalRecord.query.all()
    return render_template('index.html', records=records)

@app.route('/scanner', methods=['GET', 'POST'])
@login_required
def scanner():
    if request.method == 'POST':
        file = request.files.get('rekam_medis')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded', 'success')
            return redirect(url_for('scanner'))
        flash('Invalid file type. Only PNG files are allowed.', 'danger')
    return render_template('submit.html')

@app.route('/detail/<int:record_number>')
@login_required
def detail(record_number):
    # Fetch the record from the database using record_id
    record = MedicalRecord.query.get(record_number)
    # Pass the record to the detail template
    return render_template('detail.html', record=record)

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