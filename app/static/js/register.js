/**
 * ==========================================
 * Module: ui.js
 * ==========================================
 * Handles presentational UI interactions for the Register page.
 */
class UIManager {
    constructor() {
        this.registerCard = document.querySelector('.register-card');
        this.firstInput = document.querySelector('#register-form input[type="text"], #register-form input[type="email"]');
    }

    init() {
        this.setupEntranceAnimations();
        this.autoFocusFirstInput();
    }

    setupEntranceAnimations() {
        if (this.registerCard) {
            this.registerCard.classList.add('ui-ready');
        }
    }

    autoFocusFirstInput() {
        // Only autofocus if there are no errors displayed (meaning the user just arrived)
        const hasErrors = document.querySelector('.custom-alert, .text-danger');
        if (this.firstInput && !hasErrors) {
            // Slight delay to allow CSS entrance animation to complete
            setTimeout(() => {
                this.firstInput.focus({ preventScroll: true });
            }, 600);
        }
    }
}

/**
 * ==========================================
 * Module: app.js
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
        console.log('Register UI initialized.');
    }
}

// ==========================================
// Initialization: Wrapped in DOMContentLoaded
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    new App();
});