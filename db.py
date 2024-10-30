import pyodbc

conn_str = (
    "mssql+pyodbc://phiraphat:p1305p2547"
    "@aihitdata.cvkk4gk2kk2s.ap-southeast-2.rds.amazonaws.com:1433/aihitdata"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=yes"
    "Connect Timeout=30;"
)

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

def fetch_com(com_id):
    com_data = []  # สร้าง list สำหรับเก็บข้อมูล
    query = f''' SELECT c.name, c.website, c.url, c.description_short,a.type_name,
     l.people_count, l.senior_people_count, l.emails_count, l.personal_emails_count,	
     l.phones_count, l.addresses_count, l.investors_count,	l.clients_count,	
     l.partners_count, l.changes_count, l.people_changes_count, l.contact_changes_count
     FROM cominfo as c
     JOIN area as a ON c.area = a.id
     JOIN comlogs as l ON c.id = l.com_id
     WHERE c.id = ?; '''
     
     
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query, (com_id,))
    rows = cursor.fetchall()
    for row in rows:
        com_data.append({"name": row[0], "website": row[1],"url": row[2],"description_short": row[3], "area":row[4],
                          "people_count":row[5], "senior_people_count":row[6],"emails_count":row[7],"personal_emails_count":row[8],"phones_count":row[9], 
                          "addresses_count":row[10],"investors_count":row[11],"clients_count":row[12],"partners_count":row[13],"changes_count":row[14],
                          "people_changes_count":row[15],"contact_changes_count":row[16]})

    conn.close()
    
    return com_data  # ส่งคืน list ของ dictionary

# r = fetch_com(10002511)  
# print(r)
