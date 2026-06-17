var password1 = document.getElementById('new_password');
var passwordC = document.getElementById('confirm_password');

function validatePassword() {
	if (password1.value !== passwordC.value
	&& password1.value !== '' &&
	passwordC.value != '') {
		document.getElementById(
		'higherPasswordMatch'
		).className = "custom-alert alert-danger-custom";
		document.getElementById(
		'passwordMatch'
		).innerText =
		"رمز عبور با رمز عبور تاییدی مطابقت ندارد ";
		return false;
	} else if (passwordC.value == '' && password1.value !== '') {
		document.getElementById(
		"higherPasswordMatch"
		).classList.remove("d-none");
		document.getElementById(
		"passwordMatch"
		).innerText = "رمز عبور تایید نشده است";
		return false;
	}
	document.getElementById('higherPasswordMatch').classList.add("d-none")
	return true;
}


const descriptionField = document.getElementById('description');
const charCounter = document.getElementById('descCharCount');

function updateCharCount() {
    charCounter.textContent = descriptionField.value.length;
}

descriptionField.addEventListener('input', updateCharCount);
updateCharCount();

const isPublicSwitch = document.getElementById('isPublic');
const termsModal = document.getElementById('termsModal');
const termsCheckbox1 = document.getElementById('termsCheckbox1');
const termsCheckbox2 = document.getElementById('termsCheckbox2');
const confirmTermsBtn = document.getElementById('confirmTermsBtn');
const cancelTermsBtn = document.getElementById('cancelTermsBtn');
const termsItem1 = document.getElementById('termsItem1');
const termsItem2 = document.getElementById('termsItem2');
const visibilityStatus = document.getElementById('visibilityStatus');

// وضعیت اولیه از بک‌اند
let wasInitiallyPublic = isPublicSwitch.checked;

isPublicSwitch.addEventListener('change', function() {
    if (this.checked) {
        // فقط اگر قبلاً فعال نبوده، مودال باز کن
        if (!wasInitiallyPublic) {
            this.checked = false; // موقتاً غیرفعال
            termsModal.classList.add('active');
        } else {
            updateVisibilityStatus(true);
        }
    } else {
        // خاموش کردن بدون مودال
        updateVisibilityStatus(false);
    }
});

function checkTermsStatus() {
    const bothChecked = termsCheckbox1.checked && termsCheckbox2.checked;
    confirmTermsBtn.disabled = !bothChecked;
    termsItem1.classList.toggle('checked', termsCheckbox1.checked);
    termsItem2.classList.toggle('checked', termsCheckbox2.checked);
}

termsCheckbox1.addEventListener('change', checkTermsStatus);
termsCheckbox2.addEventListener('change', checkTermsStatus);

confirmTermsBtn.addEventListener('click', function() {
    isPublicSwitch.checked = true;
    wasInitiallyPublic = true; // حالا فعال شده
    updateVisibilityStatus(true);
    termsModal.classList.remove('active');
});

cancelTermsBtn.addEventListener('click', function() {
    termsModal.classList.remove('active');
    termsCheckbox1.checked = false;
    termsCheckbox2.checked = false;
    checkTermsStatus();
});

termsModal.addEventListener('click', function(e) {
    if (e.target === termsModal) {
        termsModal.classList.remove('active');
        termsCheckbox1.checked = false;
        termsCheckbox2.checked = false;
        checkTermsStatus();
    }
});

function updateVisibilityStatus(isActive) {
    if (isActive) {
        visibilityStatus.className = 'visibility-status status-active';
        visibilityStatus.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
            </svg>
            فعال
        `;
    } else {
        visibilityStatus.className = 'visibility-status status-inactive';
        visibilityStatus.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
            </svg>
            غیرفعال
        `;
    }
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && termsModal.classList.contains('active')) {
        termsModal.classList.remove('active');
        termsCheckbox1.checked = false;
        termsCheckbox2.checked = false;
        checkTermsStatus();
    }
});
