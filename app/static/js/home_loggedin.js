/**
 * Handles DOM manipulation and UI interactions for the Authenticated Dashboard.
 */
class UIManager {
    constructor() {
        this.searchInput = document.getElementById('globalSearch');
        this.tabButtons = document.querySelectorAll('.tab-btn');
        this.tabContents = document.querySelectorAll('.tab-content');
    }

    init() {
        this.setupTabs();
        this.setupSearch();
    }

    setupTabs() {
        this.tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const tabName = btn.id.replace('tab-', '');
                this.switchTab(tabName);
            });
        });
    }

    setupSearch() {
        if (this.searchInput) {
            this.searchInput.addEventListener('keyup', () => this.filterContent());
        }
    }

    switchTab(tabName) {
        // Update active states
        this.tabButtons.forEach(btn => {
            btn.classList.remove('active');
            btn.setAttribute('aria-selected', 'false');
        });
        this.tabContents.forEach(content => content.classList.remove('active'));
        
        const targetTab = document.getElementById('tab-' + tabName);
        const targetContent = document.getElementById('content-' + tabName);
        
        if (targetTab) {
            targetTab.classList.add('active');
            targetTab.setAttribute('aria-selected', 'true');
        }
        if (targetContent) targetContent.classList.add('active');
        
        // Reset search and filter when switching tabs
        if (this.searchInput) {
            this.searchInput.value = '';
        }
        this.filterContent();
    }

    filterContent() {
        const query = this.searchInput ? this.searchInput.value.toLowerCase() : '';
        const activeTab = document.querySelector('.tab-content.active');
        if (!activeTab) return;
        
        const items = activeTab.querySelectorAll('.filter-item');
        items.forEach(item => {
            const name = item.getAttribute('data-name').toLowerCase();
            item.style.display = name.includes(query) ? 'flex' : 'none';
        });
    }
}

/**
 * Main application entry point.
 */
class App {
    constructor() {
        this.ui = new UIManager();
        this.init();
    }

    init() {
        this.ui.init();
        console.log('BazarFlow Auth UI initialized.');
    }
}

// Safe execution wrapper
document.addEventListener('DOMContentLoaded', () => {
    new App();
});