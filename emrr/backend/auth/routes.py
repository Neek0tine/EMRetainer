import os
from flask import render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from backend.auth import app, db, bcrypt
from backend.auth.dbmodel import Staff, MedicalRecord
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from werkzeug.utils import secure_filename

# Constants
UPLOAD_FOLDER = 'emrr/emr'  # Adjust this path
ALLOWED_EXTENSIONS = {'png'}

# Configurations
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Utility functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png'}
# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Return the path to the uploaded file
            return jsonify({'url': url_for('uploaded_file', filename=filename)})
        return jsonify({'error': 'Invalid file type. Only PNG files are allowed.'}), 400
    return render_template('submit.html')

@app.route('/uploads/<filename>')
def show_results(filename):
    return f'<h1>Processed Image</h1><img src="/{app.config["UPLOAD_FOLDER"]}/{filename}" alt="Processed Image">'

@app.route('/process_image', methods=['POST'])
@login_required
def process_image():
    file = request.files.get('rekam_medis')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the image here (e.g., perform OCR)
        processed_image_path = process_text_detection(file_path)

        return redirect(url_for('show_results', filename=processed_image_path))
    else:
        flash('Invalid file type. Only PNG files are allowed.', 'danger')
        return redirect(url_for('scanner'))

def process_text_detection(file_path):
    # Dummy function to simulate image processing
    # Replace this with actual image processing logic
    return file_path  # Just returning the same path for demonstration


@app.route('/detail/<int:record_number>')
@login_required
def detail(record_number):
    record = MedicalRecord.query.get(record_number)
    return render_template('detail.html', record=record)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Utility routes for database manipulation
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

if __name__ == '__main__':
    app.run(debug=True)
