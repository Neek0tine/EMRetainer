import pandas as pd
import openpyxl
from datetime import datetime
import random

def column_replace(df):
    old_columns = ['Nama Pasien', 'Tgl.Lahir/Umur', 'No. Rekam Medis', 'Tanggal Masuk',
                'Unit Rawat Terakhir (Poli)', 'Riwayat Penyakit', 'Pemeriksaan Fisik',
                'Pemriksaan Penunjang', 'Pengobatan', 'Diagnosis Awal',
                'Kode ICD 10 Diagnosis Awal', 'Diagnosis Utama',
                'Kode ICD 10 Diagnosis Utama', 'Tindakan/Prosedur',
                'Kode ICD 9 CM Tindakan/Prosedur', 'Alergi/Reaksi Obat',
                'Keadaan Waktu Pulang / Keluar', 'Anjuran / Kontrol Ulang']

    _new_columns = ['patient_name', 'date_of_birth', 'medical_record_number', 'date_admitted',
                'recent_specialization', 'health_history', 'history_of_physical_checkups',
                'supportive_checkups', 'recent_prescription', 'early_diagnosis',
                'early_diagnosis_icd10_code', 'main_diagnosis', 'main_diagnosis_icd10_code',
                'actions_taken', 'actions_icd9cm_code', 'allergy_reactions',
                'condition_on_release', 'follow_up_notes']

    df.columns = _new_columns
    return df

df = pd.read_excel("../../../records_dummy.xlsx")
df = column_replace(df)

def image_path_gen(n):
    image_path = list()
    image1 = 'https://raw.githubusercontent.com/Neek0tine/EMRetainer/main/emrr/frontend/assets/img/records/form1.png'
    image2 = 'https://raw.githubusercontent.com/Neek0tine/EMRetainer/main/emrr/frontend/assets/img/records/form2.png'
    image3 = 'https://raw.githubusercontent.com/Neek0tine/EMRetainer/main/emrr/frontend/assets/img/records/form3.png'
    image4 = 'https://raw.githubusercontent.com/Neek0tine/EMRetainer/main/emrr/frontend/assets/img/records/form4.png'

    for _ in range(0, n):
        image_path.append(random.choice([image1, image2, image3, image4]))
    
    return image_path

image_path = pd.DataFrame(columns=['image_path'], data=image_path_gen(len(df)))
# print(image_path)

if __name__ == "__main__":
    df = pd.concat([df, image_path], axis=1)
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], dayfirst=True)
    df['date_admitted'] = pd.to_datetime(df['date_admitted'], dayfirst=True)
    df.to_csv('dummy_records_full.csv', index=False, quotechar='"', quoting=1)