// ดึงข้อมูลจาก data-* attributes
const tableRow = document.querySelector('.data-table tbody tr');

// รับค่าจาก attributes
const peopleCount = parseInt(tableRow.getAttribute('data-people-count'), 10);
const seniorPeopleCount = parseInt(tableRow.getAttribute('data-senior-people-count'), 10);
const emailsCount = parseInt(tableRow.getAttribute('data-emails-count'), 10);
const phonesCount = parseInt(tableRow.getAttribute('data-phones-count'), 10);

const changesCount = parseInt(tableRow.getAttribute('data-changes-count'), 10);
const peopleChangesCount = parseInt(tableRow.getAttribute('data-people-changes-count'), 10);
const contactChangesCount = parseInt(tableRow.getAttribute('data-contact-changes-count'), 10);

// ตั้งค่า Bar Chart: Contact Information
const ctxBar = document.getElementById('contactBarChart').getContext('2d');
const contactBarChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: ['People Count', 'Senior People Count', 'Emails Count', 'Phones Count'],
        datasets: [{
            label: 'Count',
            data: [peopleCount, seniorPeopleCount, emailsCount, phonesCount],
            backgroundColor: ['#4CAF50', '#2196F3', '#FF9800', '#F44336']
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// ตั้งค่า Pie Chart: Changes Distribution
const ctxPie = document.getElementById('changesPieChart').getContext('2d');
const changesPieChart = new Chart(ctxPie, {
    type: 'pie',
    data: {
        labels: ['Changes Count', 'People Changes Count', 'Contact Changes Count'],
        datasets: [{
            label: 'Distribution',
            data: [changesCount, peopleChangesCount, contactChangesCount],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
        }]
    },
    options: {
        responsive: true
    }
});
// ปุ่มย้อนกลับไปหน้าก่อนหน้า
document.getElementById('backButton').addEventListener('click', () => {
    history.back(); 
});
