from backend.auth import db, bcrypt
from backend.auth.dbmodel import Staff, MedicalRecord
import pandas as pd
import numpy as np


def create_dummy_staff():
    # Dummy data
    dummy_staff = [
        {'username': 'nicholasjuan', 'full_name': 'dr. Nicholas Juan K. P., Sp.N (K)., FINR., FINA','email': 'nicholas.juan.kalvin-2020@ftmm.unair.ac.id', 'password': 'kelompok1', 'profile_picture_url': 'https://2.gravatar.com/avatar/cfe94dac9ebebba8994201fa9d2886a77b147ab1a0c08d8afd7e314d82d37f7a?size=256', 'activity_log_path': '/logs/john_doe.log'},
        {'username': 'mauliahibatillah', 'full_name': 'dr. M. Aulia Hibatillah, Sp. JP (K)','email': 'muhammad.aulia.hibatillah-2020@ftmm.unair.ac.id', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile1.jpg', 'activity_log_path': '/logs/john_doe.log'},
        {'username': 'nabiladien', 'full_name': 'dr. Nabila Dien J., Sp.KJ (K)','email': 'nabila.dien.jasmine-2021@ftmm.unair.ac.id', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile1.jpg', 'activity_log_path': '/logs/john_doe.log'},
        {'username': 'sukmasekar', 'full_name': 'dr. Sukma Sekar D., Sp.A	','email': 'sukma.sekar.devita-2021@ftmm.unair.ac.id', 'password': 'kelompok1', 'profile_picture_url': 'http://example.com/profile1.jpg', 'activity_log_path': '/logs/john_doe.log'},
    ]

    for staff in dummy_staff:
        hashed_password = bcrypt.generate_password_hash(staff['password']).decode('utf-8')
        new_staff = Staff(
            username=staff['username'],
            full_name=staff['full_name'],
            email=staff['email'],
            password_salted=hashed_password,
            profile_picture_url=staff['profile_picture_url'],
            activity_log_path=staff['activity_log_path']
        )
        db.session.add(new_staff)


    # dummy_records = pd.read_excel("emrr/records_dummy.xlsx")

    # for records in dummy_records:
    #     hashed_password = bcrypt.generate_password_hash(staff['password']).decode('utf-8')
    #     new_record = MedicalRecord(
    #         medical_record_number = db.Column(db.Integer, primary_key=True)
    #         patient_name = db.Column(db.String(255), nullable=False)
    #         date_of_birth = db.Column(db.Date)
    #         date_admitted = db.Column(db.Date)
    #         recent_specialization = db.Column(db.String(255))
    #         history_of_physical_checkups = db.Column(db.Text)
    #         supportive_checkups = db.Column(db.Text)
    #         recent_prescription = db.Column(db.Text)
    #         early_diagnosis = db.Column(db.Text)
    #         early_diagnosis_icd10_code = db.Column(db.String(10))
    #         main_diagnosis = db.Column(db.Text)
    #         main_diagnosis_icd10_code = db.Column(db.String(10))
    #         actions_taken = db.Column(db.Text)
    #         actions_icd9cm_code = db.Column(db.String(10))
    #         allergy_reactions = db.Column(db.Text)
    #         condition_on_release = db.Column(db.Text)
    #         follow_up_notes = db.Column(db.Text)
    #         image_path = db.Column(db.String(255))
    #         )
        
        db.session.add(new_staff)

    db.session.commit()
    print('Committed')


def remove_dummy_staff():
    dummy_usernames = ['jon_doe', 'nadine_chandrawinata', 'andi_suhendra', 'ayu_wardani', 'budi_santoso']

    for username in dummy_usernames:
        staff = Staff.query.filter_by(username=username).first()
        if staff:
            db.session.delete(staff)

    db.session.commit()
    print('Removed dummy data')


def reset_database():
    db.drop_all()
    db.create_all()
    print('Database reset')