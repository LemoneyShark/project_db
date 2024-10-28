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

def fetch_total_uk():
        total_data = []
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = "SELECT SUM(people_count) AS total_emp,SUM(changes_count) AS total_change,COUNT(com_id) AS total_com FROM comlogs where area = 2;"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            total_data.append({"emp": row[0], "changes": row[1],"com":row[2]})
        return total_data

def fetch_total_ww():
        total_data = []
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        query = "SELECT SUM(people_count) AS total_emp,SUM(changes_count) AS total_change,COUNT(com_id) AS total_com FROM comlogs where area = 1;"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            total_data.append({"emp": row[0], "changes": row[1],"com":row[2]})
        return total_data

def fetch_com(name):
    com_data = []  # สร้าง list สำหรับเก็บข้อมูล
    query = f''' SELECT c.name, c.website, c.url, c.description_short,a.type_name,
     l.people_count, l.senior_people_count, l.emails_count, l.personal_emails_count,	
     l.phones_count, l.addresses_count, l.investors_count,	l.clients_count,	
     l.partners_count, l.changes_count, l.people_changes_count, l.contact_changes_count
     FROM cominfo as c
     JOIN area as a ON c.area = a.id
     JOIN comlogs as l ON c.id = l.com_id
     WHERE c.name = ?; '''
     
     
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, (name,))
    rows = cursor.fetchall()
    for row in rows:
        com_data.append({"name": row[0], "website": row[1],"url": row[2],"description_short": row[3], "area":row[4],
                          "people_count":row[5], "senior_people_count":row[6],"emails_count":row[7],"personal_emails_count":row[8],"phones_count":row[9], 
                          "addresses_count":row[10],"investors_count":row[11],"clients_count":row[12],"partners_count":row[13],"changes_count":row[14],
                          "people_changes_count":row[15],"contact_changes_count":row[16]})

    conn.close()
    
    return com_data  # ส่งคืน list ของ dictionary

 
