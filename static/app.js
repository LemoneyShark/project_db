document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // ป้องกันการส่งฟอร์มปกติ

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        });

        if (response.redirected) {
            const result = await response.json();
            Swal.fire({
                icon: 'success',
                title: 'Login Success',
            });
            window.location.href = response.url; // ถ้าสำเร็จให้เปลี่ยนเส้นทาง
        } else {
            const result = await response.json();
            Swal.fire({
                icon: 'warning',
                title: 'Login Failed',
                text: 'Username or password is wrong.',
            });
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'An error occurred while logging in',
        });
    }
});