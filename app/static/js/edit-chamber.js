// به‌روزرسانی وضعیت نمایش سوییچ‌ها
const publicSwitch = document.getElementById('chamberIsPublic');
const primarySwitch = document.getElementById('chamberIsPrimary');
const publicStatus = document.getElementById('publicStatus');
const primaryStatus = document.getElementById('primaryStatus');

const basePub = `
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
            </svg>
            %s
        `;
const basePri = `
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
            </svg>
            %s
        `;

publicSwitch.addEventListener('change', function() {
    if (this.checked) {
        publicStatus.className = 'settings-status status-active-public';
        publicStatus.innerHTML = basePub.replace('%s', _('عمومی'));
    } else {
        publicStatus.className = 'settings-status status-inactive';
        publicStatus.innerHTML = basePub.replace('%s', _('خصوصی'));
    }
});

primarySwitch.addEventListener('change', function() {
    if (this.checked) {
        primaryStatus.className = 'settings-status status-active-primary';
        primaryStatus.innerHTML = basePri.replace('%s', _('تالار اصلی'));
    } else {
        primaryStatus.className = 'settings-status status-inactive';
        primaryStatus.innerHTML = basePri.replace('%s', _('تالار اصلی نیست'));
    }
});
