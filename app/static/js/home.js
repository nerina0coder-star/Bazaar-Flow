
        // تابع جابجایی بین تب‌ها
function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      
    document.getElementById('tab-' + tabName).classList.add('active');
    document.getElementById('content-' + tabName).classList.add('active');
            
    document.getElementById('globalSearch').value = '';
    filterContent();
}

        // تابع فیلتر کردن لحظه‌ای
function filterContent() {
    const query = document.getElementById('globalSearch').value.toLowerCase();
    const activeTab = document.querySelector('.tab-content.active');
    const items = activeTab.querySelectorAll('.filter-item');
    
    items.forEach(item => {
        const name = item.getAttribute('data-name').toLowerCase();
        if (name.includes(query)) {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}
document.getElementById('globalSearch').addEventListener('keyup', () => { filterContent(); })
document.getElementById('tab-chambers').addEventListener('click', () => { switchTab('chambers'); })
document.getElementById('tab-users').addEventListener('click', () => { switchTab('users'); })
