let companies = [];  // เก็บข้อมูลบริษัททั้งหมด
let currentPage = 1;
const companiesPerPage = 10; // จำนวนบริษัทต่อหน้า

// ฟังก์ชันดึงข้อมูลจาก API
async function fetchCompanies() {
    try {
        const response = await fetch('/companies'); // เรียก API
        const result = await response.json();
        companies = result.data;

        // เริ่มต้นแสดงข้อมูล
        filterAndSortCompanies();
        setupPagination(companies);
    } catch (error) {
        console.error('Error fetching companies:', error);
    }
}

const searchInput = document.getElementById('searchInput');

// ตรวจสอบว่าค้นหาได้เมื่อพิมพ์
searchInput.addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();

    // กรองข้อมูลจาก companies array
    const filteredCompanies = companies.filter(company =>
        company.name.toLowerCase().includes(searchTerm) ||
        company.website?.toLowerCase().includes(searchTerm)
    );

    // อัปเดตหน้าปัจจุบันเป็นหน้าแรก
    currentPage = 1;

    // แสดงเฉพาะบริษัทที่ค้นพบ
    displayCompanies(filteredCompanies);
    setupPagination(filteredCompanies);
});


function displayCompanies(filteredCompanies = companies) {
    const companyTable = document.getElementById("companyTable");
    companyTable.innerHTML = ''; // เคลียร์ข้อมูลเก่า

    const headerRow = document.createElement('tr');
    headerRow.innerHTML = `
        <th>Name</th>
        <th>Website</th>
        <th>Area</th>
    `;
    companyTable.appendChild(headerRow);

    const startIndex = (currentPage - 1) * companiesPerPage;
    const endIndex = startIndex + companiesPerPage;
    const companiesToShow = filteredCompanies.slice(startIndex, endIndex);

    if (companiesToShow.length === 0) {
        const emptyRow = document.createElement('tr');
        emptyRow.innerHTML = `<td colspan="3">No Results Found</td>`;
        companyTable.appendChild(emptyRow);
    } else {
        companiesToShow.forEach(company => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${company.name}</td>
                <td>${company.website || 'N/A'}</td>
                <td>${company.area || 'N/A'}</td>
            `;

            row.addEventListener('click', () => {
                window.location.href = `/comdash/${company.id}`;
            });

            companyTable.appendChild(row);
        });
    }
}

// ฟังก์ชันกรองและเรียงข้อมูล
function filterAndSortCompanies() {
    let filteredCompanies = [...companies]; // สร้างสำเนาของข้อมูล

    // กรองข้อมูลตามพื้นที่ (Area)
    const areaFilter = document.getElementById('filterArea').value;
    if (areaFilter) {
        filteredCompanies = filteredCompanies.filter(company => company.area === areaFilter);
    }

    // ค้นหาตามชื่อหรือเว็บไซต์
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    filteredCompanies = filteredCompanies.filter(company =>
        company.name.toLowerCase().includes(searchTerm) ||
        company.website.toLowerCase().includes(searchTerm)
    );

    // เรียงข้อมูลตามตัวเลือกที่เลือก
    const sortBy = document.getElementById('sortBy').value;
    filteredCompanies.sort((a, b) => {
        if (a[sortBy] < b[sortBy]) return -1;
        if (a[sortBy] > b[sortBy]) return 1;
        return 0;
    });

    // คำนวณผลรวมหลังจากการกรอง
    const totalEmployees = filteredCompanies.reduce((acc, company) => acc + company.people_count, 0);
    const totalChanges = filteredCompanies.reduce((acc, company) => acc + company.changes_count, 0);
    const totalCompanies = filteredCompanies.length;

    // อัปเดตค่าผลรวมในหน้าเว็บ
    document.getElementById('totalEmployees').textContent = totalEmployees;
    document.getElementById('totalChanges').textContent = totalChanges;
    document.getElementById('totalCompanies').textContent = totalCompanies;

    // แสดงผลข้อมูลที่ผ่านการกรองและเรียงแล้ว
    displayCompanies(filteredCompanies);
    setupPagination(filteredCompanies);
}


// ตั้งค่าปุ่มแบ่งหน้า (Pagination)
function setupPagination(data) {
    const totalPages = Math.ceil(data.length / companiesPerPage);
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; // ล้างปุ่มเดิม

    const maxVisibleButtons = 5; // จำนวนปุ่มที่จะแสดง

    let startPage = Math.max(1, currentPage - Math.floor(maxVisibleButtons / 2));
    let endPage = Math.min(totalPages, startPage + maxVisibleButtons - 1);

    if (endPage - startPage < maxVisibleButtons - 1) {
        startPage = Math.max(1, endPage - maxVisibleButtons + 1);
    }

    // ปุ่ม "ก่อนหน้า"
    if (currentPage > 1) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Prev';
        prevButton.addEventListener('click', () => {
            currentPage--;
            filterAndSortCompanies();
        });
        pagination.appendChild(prevButton);
    }

    // ปุ่มเลขหน้า
    for (let i = startPage; i <= endPage; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        if (i === currentPage) {
            button.classList.add('active');
        }
        button.addEventListener('click', () => {
            currentPage = i;
            filterAndSortCompanies();
        });
        pagination.appendChild(button);
    }

    // ปุ่ม "ถัดไป"
    if (currentPage < totalPages) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.addEventListener('click', () => {
            currentPage++;
            filterAndSortCompanies();
        });
        pagination.appendChild(nextButton);
    }
}


// เรียกใช้ฟังก์ชันเมื่อหน้าโหลดเสร็จ
window.onload = fetchCompanies;

// Event listeners สำหรับ Search และ Sort
document.getElementById('searchInput').addEventListener('input', filterAndSortCompanies);
document.getElementById('filterArea').addEventListener('change', filterAndSortCompanies);
document.getElementById('sortBy').addEventListener('change', filterAndSortCompanies);

