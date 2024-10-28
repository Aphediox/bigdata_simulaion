from cryptography.fernet import Fernet
import sqlite3
import pandas as pd


def cargar_clave():
    try:
        with open("clave.key", "rb") as clave_file:
            return clave_file.read()
    except FileNotFoundError:
        clave = Fernet.generate_key()
        with open("clave.key", "wb") as clave_file:
            clave_file.write(clave)
        return clave

key = cargar_clave()
cipher_suite = Fernet(key)

def encrypt_data(data):
    if data and pd.notna(data):
        encrypted_data = cipher_suite.encrypt(str(data).encode())
        return encrypted_data
    return None

def decrypt_data(encrypted_data):
    if encrypted_data:
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data
    return None

def crear_base():
    csv_path = "healthcare_dataset.csv"
    data = pd.read_csv(csv_path)

    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Age INTEGER,
            Gender TEXT,
            Blood_Type TEXT,
            Medical_Condition TEXT,
            Date_of_Admission TEXT,
            Doctor TEXT,
            Hospital TEXT,
            Insurance_Provider TEXT,
            Billing_Amount REAL,
            Room_Number INTEGER,
            Admission_Type TEXT,
            Discharge_Date TEXT,
            Medication TEXT,
            Test_Results TEXT
        )
    ''')

    for index, row in data.iterrows():
        record = {
            'Name': row['Name'],
            'Age': row['Age'],
            'Gender': row['Gender'],
            'Blood_Type': row['Blood Type'],
            'Medical_Condition': encrypt_data(row['Medical Condition']),
            'Date_of_Admission': row['Date of Admission'],
            'Doctor': row['Doctor'],
            'Hospital': row['Hospital'],
            'Insurance_Provider': row['Insurance Provider'],
            'Billing_Amount': row['Billing Amount'],
            'Room_Number': row['Room Number'],
            'Admission_Type': row['Admission Type'],
            'Discharge_Date': row['Discharge Date'],
            'Medication': encrypt_data(row['Medication']),
            'Test_Results': encrypt_data(row['Test Results'])
        }
        cursor.execute('''
            INSERT INTO patient_records (Name, Age, Gender, Blood_Type, Medical_Condition, Date_of_Admission, Doctor, Hospital, Insurance_Provider, Billing_Amount, Room_Number, Admission_Type, Discharge_Date, Medication, Test_Results)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(record.values()))

    conn.commit()
    conn.close()
    print("Registros cifrados insertados correctamente.")


def desencriptar():
    conn = sqlite3.connect("proyecto_bd.sqlite")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM patient_records LIMIT 5')
    results = cursor.fetchall()

    for result in results:
        decrypted_record = {
            'Name': result[1],
            'Age': result[2],
            'Gender': result[3],
            'Blood_Type': result[4],
            'Medical_Condition': decrypt_data(result[5]),
            'Date_of_Admission': result[6],
            'Doctor': result[7],
            'Hospital': result[8],
            'Insurance_Provider': result[9],
            'Billing_Amount': result[10],
            'Room_Number': result[11],
            'Admission_Type': result[12],
            'Discharge_Date': result[13],
            'Medication': decrypt_data(result[14]),
            'Test_Results': decrypt_data(result[15])
        }
        print("Registro descifrado:", decrypted_record)

    conn.close()

