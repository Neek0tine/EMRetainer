from backend.auth import db, bcrypt
from backend.auth.dbmodel import Staff, MedicalRecord
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import datetime
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
    # dummy_records['date_of_birth'] = dummy_records['date_of_birth'].astype('datetime64[ns]')
    # dummy_records['date_admitted'] = dummy_records['date_admitted'].astype('datetime64[ns]')
    
    engine = create_engine('mysql+pymysql://emretainer:6yXgr68t3n.vB3gN@localhost/EMRetainer', echo=False)
    dummy_records.to_sql(name='medical_record', con=engine, if_exists='append', index=False)
    print('Record Dummy added')

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