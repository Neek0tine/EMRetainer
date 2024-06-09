
from flask import Flask, render_template, redirect, url_for, flash, request, session
from .config import Config
from .dbmodel import Staff
from app import bcrypt
import os


    
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        staff = Staff.query.filter_by(username=username).first()
        if staff and bcrypt.check_password_hash(staff.password_salted, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if 'username' in session:
        if request.method == 'POST':
            # Process the form data here
            data = request.form
            # Add code to handle the data as needed
            return 'Form data submitted'
        return render_template('submit.html')
    return redirect(url_for('login'))
