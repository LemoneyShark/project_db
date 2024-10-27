import pandas as pd
import pyodbc
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"  # ใช้สองแบ็คสแลชเพื่อ escape
    "DATABASE=aihitdata;"
    "Trusted_Connection=yes;"
)


# ฟังก์ชันสำหรับดึงข้อมูลและส่งคืนค่าเป็น list ของ dictionary
def fetch():
    user_data = []  # สร้าง list สำหรับเก็บข้อมูล
    query = "SELECT TOP 10 id, name FROM cominfo;"  # คำสั่ง query ดึง id และ name
    
    try:
        # สร้างการเชื่อมต่อ
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # รัน query และดึงข้อมูล
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # เพิ่มข้อมูลลงใน list ในรูปแบบ dictionary
        for row in rows:
            print(row[0])
            user_data.append({"id": row[0], "name": row[1]})
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # ปิดการเชื่อมต่อ
        conn.close()
    
    return user_data  # ส่งคืน list ของ dictionary

# เรียกใช้ฟังก์ชันและแสดงผลลัพธ์
def fetch_total_all():
        total_data = []
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = "SELECT SUM(people_count) AS total_emp,SUM(changes_count) AS total_change,COUNT(com_id) AS total_com FROM comlogs;"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            total_data.append({"emp": row[0], "changes": row[1],"com":row[2]})
        return total_data
