// ==========================================
// اعتبارسنجی و مدیریت فرم ویرایش پروفایل
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // بخش ۱: شمارنده کاراکتر توضیحات
    // ==========================================
    const descriptionField = document.getElementById('description');
    const charCounter = document.getElementById('descCharCount');
    
    if (descriptionField && charCounter) {
        function updateCharCount() {
            charCounter.textContent = descriptionField.value.length;
        }
        
        descriptionField.addEventListener('input', updateCharCount);
        updateCharCount();
    }

    // ==========================================
    // بخش ۲: مدیریت سوییچ و مودال شرایط
    // ==========================================
    const isPublicSwitch = document.getElementById('isPublic');
    const termsModal = document.getElementById('termsModal');
    const termsCheckbox1 = document.getElementById('termsCheckbox1');
    const termsCheckbox2 = document.getElementById('termsCheckbox2');
    const confirmTermsBtn = document.getElementById('confirmTermsBtn');
    const cancelTermsBtn = document.getElementById('cancelTermsBtn');
    const termsItem1 = document.getElementById('termsItem1');
    const termsItem2 = document.getElementById('termsItem2');
    const visibilityStatus = document.getElementById('visibilityStatus');

    const basePub = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                    </svg>
                    %s
                `;

    // فقط اگر المان‌ها وجود دارند، کد را اجرا کن
    if (isPublicSwitch && termsModal) {
        
        let wasInitiallyPublic = isPublicSwitch.checked;

        isPublicSwitch.addEventListener('change', function() {
            if (this.checked) {
                if (!wasInitiallyPublic) {
                    this.checked = false;
                    termsModal.classList.add('active');
                } else {
                    updateVisibilityStatus(true);
                }
            } else {
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
            wasInitiallyPublic = true;
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
            if (!visibilityStatus) return;

            if (isActive) {
                visibilityStatus.className = 'visibility-status status-active';
                visibilityStatus.innerHTML = basePub.replace('%s', _('فعال'));
            } else {
                visibilityStatus.className = 'visibility-status status-inactive';
                visibilityStatus.innerHTML = basePub.replace('%s', _('غیر فعال'));
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
    }
});