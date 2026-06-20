// ==========================================
// اعتبارسنجی فرم ثبت‌نام
// ==========================================

// توابع کمکی برای نمایش/مخفی کردن خطاها
function showError(boxId, textId, message) {
    const box = document.getElementById(boxId);
    const text = document.getElementById(textId);
    
    if (box) {
        box.classList.remove('none');
        box.classList.add('flex');
    }
    if (text) text.textContent = message;
}

function hideError(boxId) {
    const box = document.getElementById(boxId);
    
    if (box) {
        box.classList.remove('flex');
        box.classList.add('none');
    }
}

// اعتبارسنجی رمز عبور
function validatePassword() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password === '' && confirmPassword === '') {
        showError('higherPasswordMatch', 'passwordMatch', 'رمز عبور وارد نشده است');
        return false;
    }
    if (password === '') {
        showError('higherPasswordMatch', 'passwordMatch', 'رمز عبور وارد نشده است');
        return false;
    }
    if (confirmPassword === '') {
        showError('higherPasswordMatch', 'passwordMatch', 'تکرار رمز عبور خالی است');
        return false;
    }
    if (password !== confirmPassword) {
        showError('higherPasswordMatch', 'passwordMatch', 'رمز عبور با تکرار آن مطابقت ندارد');
        return false;
    }

    hideError('higherPasswordMatch');
    return true;
}

// اعتبارسنجی نام کاربری و ایمیل
function validateEtc() {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();

    if (username === '' && email === '') {
        showError('higherEtcError', 'etcError', 'نام کاربری و ایمیل خالی هستند');
        return false;
    }
    if (username === '') {
        showError('higherEtcError', 'etcError', 'نام کاربری خالی است');
        return false;
    }
    if (email === '') {
        showError('higherEtcError', 'etcError', 'ایمیل خالی است');
        return false;
    }

    hideError('higherEtcError');
    return true;
}

// اعتبارسنجی کلی فرم (هر دو باید درست باشند)
function validateForm() {
    const isEtcValid = validateEtc();
    const isPasswordValid = validatePassword();
    return isEtcValid && isPasswordValid;
}

// اتصال به فرم پس از لود DOM
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('register-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!validateForm()) {
                event.preventDefault();
            }
        });
    }
});