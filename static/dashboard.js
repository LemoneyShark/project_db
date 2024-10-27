let companies = [];  // เก็บข้อมูลบริษัททั้งหมด
let currentPage = 1;
const companiesPerPage = 10; // จำนวนบริษัทต่อหน้า

// ฟังก์ชันสำหรับดึงข้อมูลจาก API
async function fetchCompanies() {
    try {
        const response = await fetch('/companies');
        const result = await response.json();
        companies = result.data;

        // แสดงบริษัททั้งหมด
        displayCompanies();
        setupPagination();
    } catch (error) {
        console.error('Error fetching companies:', error);
    }
}

// ฟังก์ชันสำหรับแสดงรายชื่อบริษัททั้งหมดหรือบริษัทที่กรองแล้ว
function displayCompanies() {
    const companyTable = document.getElementById("companyTable");
    companyTable.innerHTML = ''; // เคลียร์ข้อมูลเก่า

    // สร้างแถวหัวตาราง
    const headerRow = document.createElement('tr');
    headerRow.innerHTML = `
        <th>Name</th>
        <th>Website</th>
        <th>Area</th>
    `;
    companyTable.appendChild(headerRow);

    // คำนวณบริษัทที่จะเริ่มต้นแสดงในแต่ละหน้า
    const startIndex = (currentPage - 1) * companiesPerPage;
    const endIndex = startIndex + companiesPerPage;
    const companiesToShow = companies.slice(startIndex, endIndex);

    if (companiesToShow.length === 0    ) {
        const emptyRow = document.createElement('tr');
        emptyRow.innerHTML = `<td colspan="4">Not Found</td>`;
        companyTable.appendChild(emptyRow);
    } else {
        companiesToShow.forEach(company => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${company.name}</td>
                <td>${company.website || 'N/A'}</td>
                <td>${company.area || 0}</td>
                
            `;
            companyTable.appendChild(row);
        });
    }
}

// Live search function
document.getElementById('searchInput').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();

    if (searchTerm === '') {
        // หากช่องค้นหาว่าง ให้แสดงบริษัททั้งหมด
        fetchCompanies();
    } else {
        // กรองบริษัทตามคำที่ค้นหา
        const filteredCompanies = companies.filter(company => 
            company.name.toLowerCase().includes(searchTerm)
        );

        // แสดงเฉพาะผลลัพธ์ที่ค้นหาเจอ
        companies = filteredCompanies.length ? filteredCompanies : [];
        currentPage = 1; // เริ่มต้นที่หน้าที่ 1
        displayCompanies();
        setupPagination();
    }
});

// ฟังก์ชันสำหรับตั้งค่าปุ่มแบ่งหน้า
function setupPagination() {
    const totalPages = Math.ceil(companies.length / companiesPerPage);
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = ''; // เคลียร์ปุ่มเดิม

    // เพิ่มปุ่มก่อนหน้า
    if (currentPage > 1) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Prev';
        prevButton.addEventListener('click', function() {
            currentPage--;
            displayCompanies();
            setupPagination();
        });
        pagination.appendChild(prevButton);
    }

    // กำหนดช่วงปุ่มที่จะแสดง
    let startPage, endPage;
    if (totalPages <= 5) {
        startPage = 1;
        endPage = totalPages;
    } else {
        startPage = Math.max(1, currentPage - 2);
        endPage = Math.min(totalPages, currentPage + 2);

        // หากหน้าปัจจุบันอยู่ใกล้สุดขอบ ให้ปรับขอบเขต
        if (currentPage <= 3) {
            endPage = 5; // แสดง 5 หน้าแรก
        }
        if (currentPage + 2 >= totalPages) {
            startPage = totalPages - 4; // แสดง 5 หน้าสุดท้าย
        }
    }

    // สร้างปุ่มสำหรับแต่ละหน้า
    for (let i = startPage; i <= endPage; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        // ตรวจสอบว่าหน้าเป็นหน้าปัจจุบันและเพิ่มคลาส active
        if (i === currentPage) {
            button.classList.add('active'); // เพิ่มคลาส active ให้กับปุ่มหน้าปัจจุบัน
        }
        button.addEventListener('click', function() {
            currentPage = i;
            displayCompanies();
            setupPagination();
        });
        pagination.appendChild(button);
    }

    // เพิ่มปุ่มถัดไป
    if (currentPage < totalPages) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', function() {
            currentPage++;
            displayCompanies();
            setupPagination();
        });
        pagination.appendChild(nextButton);
    }
}

// เรียกใช้ฟังก์ชัน fetchCompanies เมื่อโหลดหน้าเสร็จ
window.onload = fetchCompanies;