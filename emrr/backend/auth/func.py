from backend.auth import db, bcrypt
from backend.auth.dbmodel import Staff, MedicalRecord
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.exc import IntegrityError

def create_dummy_all():
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
    try:
        db.session.commit()
    except IntegrityError:
        pass
    print('Staff Dummy added')

    dummy_records = pd.read_csv("dummy_records_full.csv", index_col=False)
    
    engine = create_engine('mysql+pymysql://emretainer:6yXgr68t3n.vB3gN@localhost/EMRetainer', echo=False)
    dummy_records.to_sql(name='MedicalRecord', con=engine)
    print('Record Dummy added')

    # for records in dummy_records:
    #     print(records)
    #     new_record = MedicalRecord(
    #         medical_record_number = dummy_records['medical_record_number'],
    #         patient_name = dummy_records['patient_name'],
    #         date_of_birth = dummy_records['date_of_birth'],
    #         date_admitted = dummy_records['date_admitted'],
    #         recent_specialization = dummy_records['recent_specialization'],
    #         health_history = dummy_records['health_history'],
    #         supportive_checkups = dummy_records['supportive_checkups'],
    #         recent_prescription = dummy_records['recent_prescription'],
    #         early_diagnosis = dummy_records['early_diagnosis'],
    #         early_diagnosis_icd10_code = dummy_records['early_diagnosis_icd10_code'],
    #         main_diagnosis = dummy_records['main_diagnosis'],
    #         main_diagnosis_icd10_code = dummy_records['main_diagnosis_icd10_code'],
    #         actions_taken = dummy_records['actions_taken'],
    #         actions_icd9cm_code = dummy_records['actions_icd9cm_code'],
    #         allergy_reactions = dummy_records['allergy_reactions'],
    #         condition_on_release = dummy_records['condition_on_release'],
    #         follow_up_notes = dummy_records['follow_up_notes'],
    #         image_path = dummy_records['image_path']
    #         )
        
    #     db.session.add(new_record)
    # print('Records Dummy added')

    # db.session.commit()
    # print('DB Committed.')


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