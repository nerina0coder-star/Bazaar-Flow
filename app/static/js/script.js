const csrfToken = document.querySelector('meta[name="csrf"]').getAttribute('content');

document.addEventListener("DOMContentLoaded", () => {
    cy = document.getElementById('current-year');
    if (cy !== null) cy.innerText = new Date().getFullYear();
});