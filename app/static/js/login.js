/**
 * Handles DOM manipulation and UI interactions for the Login Page.
 */
class UIManager {
    constructor() {
        this.passwordInput = document.querySelector('input[name="password"]');
        this.toggleBtn = document.querySelector('.password-toggle-btn');
    }

    init() {
        if (this.passwordInput && this.toggleBtn) {
            this.setupPasswordToggle();
        }
    }

    setupPasswordToggle() {
        this.toggleBtn.addEventListener('click', () => {
            const type = this.passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            this.passwordInput.setAttribute('type', type);
            
            const eyeIcon = this.toggleBtn.querySelector('.eye-icon');
            const isHidden = type === 'password';
            
            // Update ARIA label for screen readers
            this.toggleBtn.setAttribute('aria-label', isHidden ? 'نمایش رمز عبور' : 'مخفی کردن رمز عبور');
            
            // Update SVG icon paths
            if (isHidden) {
                eyeIcon.innerHTML = '<path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/><path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>';
            } else {
                eyeIcon.innerHTML = '<path d="M13.875 18.825A10.05 10.05 0 0 1 12 19c-4.418 0-8-3.134-8-7s3.582-7 8-7a10.05 10.05 0 0 1 1.875.175.5.5 0 0 1 .125.825l-8.5 8.5a.5.5 0 0 1-.825-.125z"/><path d="M11.293 11.293a1 1 0 0 0-1.414-1.414L8 11.757l-1.879-1.878a1 1 0 1 0-1.414 1.414l1.878 1.879-1.878 1.878a1 1 0 1 0 1.414 1.414L8 14.586l1.879 1.878a1 1 0 0 0 1.414-1.414L9.414 13.172l1.879-1.879z"/>';
            }
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
        console.log('BazarFlow Login UI initialized.');
    }
}

// Safe execution wrapper
document.addEventListener('DOMContentLoaded', () => {
    new App();
});