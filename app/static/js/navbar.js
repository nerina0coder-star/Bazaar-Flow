/**
 * Handles DOM manipulation and UI interactions.
 */
class UIManager {
    constructor() {
        this.navbarCollapse = document.getElementById('navbarMainContent');
        this.searchInput = document.querySelector('.search-input-modern');
    }

    init() {
        this.setupMobileMenuAutoClose();
        this.setupSearchFocusEffects();
    }

    setupMobileMenuAutoClose() {
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link:not(.dropdown-toggle)');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (this.navbarCollapse && this.navbarCollapse.classList.contains('show')) {
                    // Using Bootstrap 5 Collapse instance to toggle
                    const bsCollapse = bootstrap.Collapse.getInstance(this.navbarCollapse) || new bootstrap.Collapse(this.navbarCollapse, { toggle: false });
                    bsCollapse.hide();
                }
            });
        });
    }

    setupSearchFocusEffects() {
        if (this.searchInput) {
            this.searchInput.addEventListener('focus', () => {
                this.searchInput.closest('.position-relative').classList.add('search-focused');
            });
            this.searchInput.addEventListener('blur', () => {
                this.searchInput.closest('.position-relative').classList.remove('search-focused');
            });
        }
    }
}

/**
 * Main application entry point and initialization.
 */
class App {
    constructor() {
        this.ui = new UIManager();
        this.init();
    }

    init() {
        this.ui.init();
        console.log('BazarFlow UI initialized successfully.');
    }
}

// ==========================================
// Initialization: Wrapped in DOMContentLoaded
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    new App();
});