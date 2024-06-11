import pandas as pd
import shutil
import random
import time
import glob
import os 
from tqdm import tqdm

dummy_records = pd.read_excel("emrr/records_dummy.xlsx")
dummy_records = dummy_records.rename(columns=
    {'No. Rekam Medis': 'medical_record_number',
    'Nama Pasien': 'patient_name',
    'Tgl.Lahir/Umur': 'date_of_birth',
    'Tanggal Masuk': 'date_admitted',
    'Unit Rawat Terakhir (Poli)': 'recent_specialization',
    'Riwayat Penyakit': 'health_history',
    'Pemeriksaan Fisik': 'history_of_physical_checkups',
    'Pemriksaan Penunjang': 'supportive_checkups',
    'Pengobatan': 'recent_prescription',
    'Diagnosis Awal': 'early_diagnosis',
    'Kode ICD 10 Diagnosis Awal' : 'early_diagnosis_icd10_code', 
    'Diagnosis Utama' : 'main_diagnosis',
    'Kode ICD 10 Diagnosis Utama' : 'main_diagnosis_icd10_code', 
    'Tindakan/Prosedur' : 'actions_taken',
    'Kode ICD 9 CM Tindakan/Prosedur' : 'actions_icd9cm_code', 
    'Alergi/Reaksi Obat' : 'allergy_reactions',
    'Keadaan Waktu Pulang / Keluar' : 'condition_on_release', 
    'Anjuran / Kontrol Ulang' : 'follow_up_notes'})

path = r"emrr/model/preprocessor/data"
dest = "emrr/dummy/forms"

for filename in tqdm(os.listdir(dest)):
    if filename.endswith('.png'):
        os.remove(os.path.join(dest, filename))

def form_randomizer():
    img = random.choices(["form1.png", "form4.png", "form3.png", "form2.png"], k=1)
    return img 

def path_generator():
    paths = pd.DataFrame(columns=["image_path"])
    for p in tqdm(range(0, 30)):
        _path = path + "/" + form_randomizer()[0]
        time.sleep(1)
        dst = "emrr/dummy/forms" + "/" + str(int(time.time()) ) + ".png"
        shutil.copyfile(_path, dst)
        _data = {'image_path' : [dst]}
        newpath = pd.DataFrame(data=_data)
        paths = pd.concat([paths, newpath])
        
    return paths

paths = path_generator()
paths.reset_index(drop=True, inplace=True)
dummy_records.reset_index(drop=True, inplace=True)
dummy_records = dummy_records.astype(str)
df = pd.concat([dummy_records, paths], axis=1) 

df.to_csv('dummy_records_full.csv', index=False, quotechar='"', quoting=1)

# dummy_records = pd.read_csv('dummy_records_full.csv', sep=',').to_dict()
                
# dummy_records = pd.read_csv("dummy_records_full.csv")
# print(dummy_records['date_of_birth'])