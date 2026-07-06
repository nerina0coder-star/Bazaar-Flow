/**
 * ==========================================
 * Module: UIManager
 * ==========================================
 * Handles presentational UI interactions for the Create Chamber page.
 */
class UIManager {
    constructor() {
        this.formCard = document.querySelector('.form-card');
        this.firstInput = document.querySelector('#create-chamber-form input[type="text"]');
        this.alerts = document.querySelectorAll('.csrf-alert, .custom-alert');
    }

    init() {
        this.setupEntranceAnimations();
        this.autoFocusFirstInput();
        this.setupErrorShake();
    }

    setupEntranceAnimations() {
        if (this.formCard) {
            this.formCard.classList.add('ui-ready');
        }
    }

    autoFocusFirstInput() {
        // Only autofocus if there are no errors displayed
        if (this.firstInput && this.alerts.length === 0) {
            setTimeout(() => {
                this.firstInput.focus({ preventScroll: true });
            }, 600);
        }
    }

    setupErrorShake() {
        // Add a subtle shake animation if there are form errors
        if (this.alerts.length > 0 && this.formCard) {
            this.formCard.classList.add('has-errors');
        }
    }
}

/**
 * ==========================================
 * Module: App
 * ==========================================
 * Main application entry point.
 */
class App {
    constructor() {
        this.ui = new UIManager();
        this.init();
    }

    init() {
        this.ui.init();
        console.log('Create Chamber UI initialized.');
    }
}

// ==========================================
// Initialization: Wrapped in DOMContentLoaded
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    new App();
});