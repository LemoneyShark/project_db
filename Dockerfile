# เลือก Python Image เบื้องต้น
FROM python:3.9-slim

# ติดตั้ง dependencies ที่จำเป็น (ODBC Driver และ UnixODBC)
RUN apt-get update && apt-get install -y \
    curl apt-transport-https unixodbc unixodbc-dev gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# ตั้งค่าตำแหน่งทำงานใน container
WORKDIR /app

# คัดลอกโค้ดโปรเจกต์ทั้งหมดลง container
COPY . .

# ติดตั้ง dependencies ของ Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# เปิดพอร์ต 8000 (FastAPI ใช้ค่าเริ่มต้นนี้)
EXPOSE 8000

# คำสั่งสำหรับรันแอป FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
