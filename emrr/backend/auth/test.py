import pandas as pd

dummy_records = pd.read_excel("emrr/records_dummy.xlsx")
print(dummy_records.columns)
dummy_records = dummy_records.rename(columns={
    'Nama Pasien': 'patient_name',
    'Tgl.Lahir/Umur ': 'date_of_birth',
    'No. Rekam Medis': 'medical_record_number',
    'Tanggal Masuk': 'date_admitted',
    'Unit Rawat Terakhir (Poli)': 'recent_specialization',
    'Riwayat Penyakit': 'health_history',
    'Pemeriksaan Fisik': 'history_of_physical_checkups',
    'Pemriksaan Penunjang': 'supportive_checkups',
    'Pengobatan': 'recent_prescription',
    'Diagnosis Awal': 'early_diagnosis'
    'Kode ICD 10 Diagnosis Awal' : 'early_diagnosis_icd10_code', 
    'Diagnosis Utama' : 'main_diagnosis',
    'Kode ICD 10 Diagnosis Utama' : 'main_diagnosis_icd10_code', 
    'Tindakan/Prosedur' : 'actions_taken',
    'Kode ICD 9 CM Tindakan/Prosedur' : 'actions_icd9cm_code', 
    'Alergi/Reaksi Obat' : 'allergy_reactions',
    'Keadaan Waktu Pulang / Keluar' : 'condition_on_release', 
    'Anjuran / Kontrol Ulang' : 'follow_up_notes'
    })

pritn(dummy_records)