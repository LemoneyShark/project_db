import pandas as pd
import pyodbc

# อ่านไฟล์ CSV และแปลงคอลัมน์ให้เป็น string
# file_path = 'E:/db/project_db/importCSVtoDB/aihitdata-worldwide-10k.csv'
file_path = 'E:/db/project_db/importCSVtoDB/aihitdata-uk-10k.csv'
data2 = pd.read_csv(file_path, dtype={
    'id': str,
    'website':str,
    'url':str,
    'description_shorts' :str, 
    'people_count': int,
    'senior_people_count': int,
    'emails_count': int,
    'personal_emails_count': int,
    'phones_count': int,
    'addresses_count': int,
    'investors_count': int,
    'clients_count': int,
    'partners_count': int,
    'changes_count': int,
    'people_changes_count': int,
    'contact_changes_count': int
})
# ตรวจสอบและจัดการค่า NaN
data2.fillna('', inplace=True)

# ตั้งค่าการเชื่อมต่อกับ SQL Server
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"  # ใช้สองแบ็คสแลชเพื่อ escape
    "DATABASE=aihitdata;"
    "Trusted_Connection=yes;"
)

# สร้างการเชื่อมต่อกับ SQL Server
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# นำเข้าข้อมูลไปยังตาราง cominfo
for _, row in data2.iterrows():
    try:
        cursor.execute('''
            INSERT INTO cominfo (id, name, website, url, description_short, type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', row['id'], row['name'], row['website'], row['url'], row['description_short'],2)
    except Exception as e:
        print(f"Error inserting row {row['id']}: {e}")
# นำเข้าข้อมูลไปยังตาราง comstatistics
for _, row in data2.iterrows():
        cursor.execute('''
            INSERT INTO comlogs (com_id, people_count, senior_people_count, emails_count, personal_emails_count,
                                       phones_count, addresses_count, investors_count, clients_count, partners_count,
                                       changes_count, people_changes_count, contact_changes_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row['id'], row['people_count'], row['senior_people_count'], row['emails_count'],
           row['personal_emails_count'], row['phones_count'], row['addresses_count'], row['investors_count'],
           row['clients_count'], row['partners_count'], row['changes_count'], row['people_changes_count'],
           row['contact_changes_count'])
    # except Exception as e:
    #     print(f"Error inserting row {row['id']}: {e}")

conn.commit()
cursor.close()
conn.close()