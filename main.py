from fastapi import FastAPI,Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from db import *

app = FastAPI()

# ตั้งค่าให้เสิร์ฟไฟล์ static จากโฟลเดอร์ "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# ตั้งค่าโฟลเดอร์ templates
templates = Jinja2Templates(directory="templates")

# ตั้งค่าเชื่อมต่อฐานข้อมูล SQL Server
DATABASE_URL = (
    "mssql+pyodbc://phiraphat:p1305p2547"
    "@aihitdata.cvkk4gk2kk2s.ap-southeast-2.rds.amazonaws.com:1433/aihitdata"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=yes"
)

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

@app.get("/top")
def serve_index():
    return FileResponse("templates/top.html")

@app.get("/dashboard", response_class=HTMLResponse)
def serve_index(request: Request):
    totals = fetch_total_all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "totals": totals})


@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# API สำหรับดึงข้อมูลบริษัท
@app.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    try:
        query = text("select c.name,c.website,a.type_name,c.id,l.people_count,l.changes_count from cominfo as c left join area as a on c.area = a.id left join comlogs as l on c.id = l.com_id")
        result = db.execute(query).fetchall()


        
        # แปลงผลลัพธ์เป็น JSON
        companies = [
            {
                "name": row[0],
                "website": row[1] if row[1] is not None else 'N/A',
                "area": row[2] if row[2] is not None else 'N/A',
                "id": row[3] if row[3] is not None else 'N/A',
                "people_count": row[4] if row[4] is not None else 0,
                "changes_count": row[5] if row[5] is not None else 0,
            } for row in result
        ]
        return {"data": companies}
    
    except Exception as e:
        print(f"Error fetching companies: {e}")
        raise HTTPException(status_code=500, detail="An error occurred fetching companies")


@app.get("/comdash/{com_id}", response_class=HTMLResponse)
async def read_dashboard(request: Request, com_id: str):
    # ค้นหาผู้ใช้ตาม `id`
    datas = fetch_com(com_id)
    return templates.TemplateResponse("comdashboard.html", {"request": request, "datas":datas})    

@app.post("/register")
async def register(
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    # ใส่โค้ดสำหรับบันทึกข้อมูลลงตารางที่มีอยู่
    insert_query = text("INSERT INTO users (firstName, lastName, username, password, email) VALUES (:first_name, :last_name, :username, :password, :email)")
    db.execute(
        insert_query,
        {"first_name": first_name, "last_name": last_name, "username": username, "password": password, "email": email}
    )
    db.commit()
    
    # Redirect ไปยังหน้าอื่น เช่น หน้า Login หลังสมัครเสร็จ
    return RedirectResponse(url="/", status_code=303)
# API สำหรับดึงข้อมูล Top 10 บริษัทตามจำนวนพนักงาน
@app.get("/top_companies_by_employees")
def get_top_companies(db: Session = Depends(get_db)):
    query = text("SELECT TOP 10 c.name, l.people_count FROM cominfo as c left join comlogs as l on c.id = l.com_id ORDER BY people_count DESC")
    result = db.execute(query).fetchall()

    companies = [{"name": row[0], "people_count": row[1]} for row in result]
    return companies
