from app import db

class Staff(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_salted = db.Column(db.String(255), nullable=False)
    profile_picture_url = db.Column(db.String(255))
    activity_log_path = db.Column(db.Text)

class MedicalRecord(db.Model):
    medical_record_number = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date)
    date_admitted = db.Column(db.Date)
    recent_specialization = db.Column(db.String(255))
    history_of_physical_checkups = db.Column(db.Text)
    supportive_checkups = db.Column(db.Text)
    recent_prescription = db.Column(db.Text)
    early_diagnosis = db.Column(db.Text)
    early_diagnosis_icd10_code = db.Column(db.String(10))
    main_diagnosis = db.Column(db.Text)
    main_diagnosis_icd10_code = db.Column(db.String(10))
    actions_taken = db.Column(db.Text)
    actions_icd9cm_code = db.Column(db.String(10))
    allergy_reactions = db.Column(db.Text)
    condition_on_release = db.Column(db.Text)
    follow_up_notes = db.Column(db.Text)