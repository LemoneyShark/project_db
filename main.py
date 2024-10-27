from fastapi import FastAPI,Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from db import*

app = FastAPI()

# ตั้งค่าให้เสิร์ฟไฟล์ static จากโฟลเดอร์ "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# ตั้งค่าโฟลเดอร์ templates
templates = Jinja2Templates(directory="templates")

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

@app.get("/dashboard", response_class=HTMLResponse)
def serve_index(request: Request):
    totals = fetch_total_all()
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "totals": totals})

# API สำหรับดึงข้อมูลบริษัท
@app.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    try:
        query = text("select c.name,c.website,a.type_name from cominfo as c left join area as a on c.area = a.id")
        result = db.execute(query).fetchall()
        
        # แปลงผลลัพธ์เป็น JSON
        companies = [
            {
                "name": row[0],
                "website": row[1] if row[1] is not None else 'N/A',
                "area": row[2] if row[2] is not None else 'N/A',
            } for row in result
        ]
        return {"data": companies}
    
    except Exception as e:
        print(f"Error fetching companies: {e}")
        raise HTTPException(status_code=500, detail="An error occurred fetching companies")

user_data = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
    {"id": 3, "name": "Charlie", "age": 35},
]

@app.get("/test", response_class=HTMLResponse)
async def read_root(request: Request):
    data = fetch()
    # ส่งข้อมูล user_data ไปยัง template index.html
    return templates.TemplateResponse("test1.html", {"request": request, "datas": data})

@app.get("/data/{data_id}", response_class=HTMLResponse)
async def get_user(request: Request, data_id: str):
    # ค้นหาผู้ใช้ตาม `id`
    data = fetch()
    name = next((u for u in data if u["id"] == data_id), None)
    if not name:
        return HTMLResponse(content="<h1>User not found</h1>", status_code=404)
    
    # ส่งข้อมูลผู้ใช้ไปยัง template user.html
    return templates.TemplateResponse("test2.html", {"request": request, "name": name})
    
    
