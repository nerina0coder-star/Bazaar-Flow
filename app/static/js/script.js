const csrfToken = document.querySelector('meta[name="csrf"]').getAttribute('content');

document.getElementById('current-year').innerText = new Date().getFullYear();
