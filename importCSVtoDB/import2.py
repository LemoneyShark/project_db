import pandas as pd
import pyodbc

# ตั้งค่าการเชื่อมต่อกับ SQL Server
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=aihitdata.cvkk4gk2kk2s.ap-southeast-2.rds.amazonaws.com,1433;"
    "DATABASE=aihitdata;"
    "UID=phiraphat;"  # ใส่ชื่อผู้ใช้ที่ตั้งไว้
    "PWD=p1305p2547;"  # ใส่รหัสผ่านที่ตั้งไว้
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

# สร้างการเชื่อมต่อกับ SQL Server
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# อ่านข้อมูลจากไฟล์ CSV
file_path = r'importCSVtoDB\aihitdata-worldwide-10k.csv'
data = pd.read_csv(file_path)

# ตรวจสอบว่ามีคอลัมน์ชื่อ 'id' ในไฟล์
if 'id' in data.columns:
    ids = data['id'].tolist()  # ดึงค่าทั้งหมดในคอลัมน์ 'id'
    
    # อัปเดตฐานข้อมูลสำหรับแต่ละ 'id'
    for id_value in ids:
        cursor.execute("UPDATE cominfo SET area = 1 WHERE id = ?", id_value)
    
    # ยืนยันการเปลี่ยนแปลง
    conn.commit()