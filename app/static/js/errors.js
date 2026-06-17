document.addEventListener('DOMContentLoaded', function() {
    // ثبت یک پیام ساده در کنسول برای اهداف دیباگ (اختیاری)
    console.log('صفحه خطای {{ type }} با موفقیت بارگذاری شد.');

    const backButton = document.getElementById('btn-back');
    if(backButton) {
        backButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.history.back();
        });
    }
});