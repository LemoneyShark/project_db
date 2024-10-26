from fastapi import FastAPI,Depends, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

# ตั้งค่าให้เสิร์ฟไฟล์ static จากโฟลเดอร์ "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# ตั้งค่าเชื่อมต่อฐานข้อมูล SQL Server
DATABASE_URL = "mssql+pyodbc://localhost\\SQLEXPRESS/project_db?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency สำหรับการเชื่อมต่อฐานข้อมูล
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Serve หน้า html
@app.get("/")
def serve_index():
    return FileResponse("templates/login.html")

@app.get("/dashboard")
def serve_index():
    return FileResponse("templates/dashboard.html")

# Pydantic model สำหรับรับข้อมูล login
class LoginData(BaseModel):
    username: str
    password: str
    
# API สำหรับการ login
@app.post("/login")
async def login(data: LoginData, db: Session = Depends(get_db)):
    # Query เพื่อตรวจสอบ username และ password จากฐานข้อมูล
        query = text("SELECT * FROM users WHERE username = :username AND password = :password")
        result = db.execute(query, {"username": data.username, "password": data.password}).fetchone()

        # ตรวจสอบว่าพบผู้ใช้หรือไม่
        if result:
            # ถ้าพบผู้ใช้ ให้ redirect ไปที่หน้า dashboard
            return RedirectResponse(url="/dashboard")
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
# API สำหรับดึงข้อมูลบริษัท
@app.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    try:
        query = text("SELECT name FROM company")  # เปลี่ยนชื่อตารางตามที่คุณใช้
        result = db.execute(query).fetchall()
        
        # แปลงผลลัพธ์เป็น JSON
        companies = [{"name": row[0]} for row in result]
        return {"data": companies}
    
    except Exception as e:
        print(f"Error fetching companies: {e}")
        raise HTTPException(status_code=500, detail="An error occurred fetching companies")