from fastapi import FastAPI,Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

# ตั้งค่าให้เสิร์ฟไฟล์ static จากโฟลเดอร์ "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# ตั้งค่าเชื่อมต่อฐานข้อมูล SQL Server
DATABASE_URL = "mssql+pyodbc://localhost\\SQLEXPRESS/aihitdata?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency สำหรับการเชื่อมต่อฐานข้อมูล
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model สำหรับรับข้อมูล login
class LoginData(BaseModel):
    username: str
    password: str


# API สำหรับการ login
@app.post("/login")
async def login(data: LoginData, db: Session = Depends(get_db)):
    # Query เพื่อตรวจสอบ username และ password จากฐานข้อมูล
    try:
        query = text("SELECT * FROM users WHERE username = :username AND password = :password")
        result = db.execute(query, {"username": data.username, "password": data.password}).fetchone()

        # ตรวจสอบว่าพบผู้ใช้หรือไม่
        if result:
            # ถ้าพบผู้ใช้ ให้ redirect ไปที่หน้า dashboard
            return RedirectResponse(url="/dashboard")
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    
    except Exception as e:
        print(f"Error: {e}")  # แสดงข้อความ error ใน terminal เพื่อ debug
        raise HTTPException(status_code=500, detail="An internal error occurred during login")

# Serve หน้า html
@app.get("/")
def serve_index():
    return FileResponse("templates/login.html")

@app.get("/dashboard_old")
def serve_home():
    return FileResponse("templates/dashboard2.html")

@app.get("/dashboard")
def serve_index():
    return FileResponse("templates/dashboard.html")


# API สำหรับดึงข้อมูลจากตารางในฐานข้อมูล
@app.get("/data")
async def get_data(db: Session = Depends(get_db)):
    try:
        # Query ข้อมูลจากฐานข้อมูล
        query = text("SELECT TOP 10 name FROM cominfo")  # เปลี่ยนเป็นชื่อตารางของคุณ
        result = db.execute(query).fetchall()

        # แปลงผลลัพธ์เป็น JSON
        data = [dict(row) for row in result]
        return {"data": data}

    except Exception as e:
        print(f"Error: {e}")  # แสดงข้อผิดพลาดใน terminal เพื่อ debug
        raise HTTPException(status_code=500, detail="An error occurred fetching data")

# API สำหรับดึง username จากฐานข้อมูล
@app.get("/usernames")
async def get_usernames(db: Session = Depends(get_db)):
    try:
        # Query ข้อมูล username จากตาราง users
        query = text("SELECT username FROM users")  # เปลี่ยนเป็นชื่อตารางของคุณ
        result = db.execute(query).fetchall()

        # แปลงผลลัพธ์เป็น JSON
        usernames = [row['username'] for row in result]
        return JSONResponse(content={"usernames": usernames})
        

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred fetching usernames")

# API สำหรับดึงข้อมูลบริษัท
@app.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    try:
        query = text("SELECT name FROM cominfo")  # เปลี่ยนชื่อตารางตามที่คุณใช้
        result = db.execute(query).fetchall()
        
        # แปลงผลลัพธ์เป็น JSON
        companies = [{"name": row[0]} for row in result]
        return {"data": companies}
    
    except Exception as e:
        print(f"Error fetching companies: {e}")
        raise HTTPException(status_code=500, detail="An error occurred fetching companies")

  
    
    
