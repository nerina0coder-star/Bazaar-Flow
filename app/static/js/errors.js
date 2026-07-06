document.addEventListener('DOMContentLoaded', function() {
    const backButton = document.getElementById('btn-back');
    if(backButton) {
        backButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.history.back();
        });
    }
});