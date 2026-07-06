// home_guest.js
/**
 * Handles DOM manipulation and UI interactions for the Guest Landing Page.
 */
class UIManager {
    constructor() {
        this.featureCards = document.querySelectorAll('.feature-card');
    }

    init() {
        this.setupScrollAnimations();
    }

    setupScrollAnimations() {
        // Intersection Observer for smooth fade-in on scroll
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            this.featureCards.forEach(card => observer.observe(card));
        } else {
            // Fallback for older browsers
            this.featureCards.forEach(card => card.classList.add('visible'));
        }
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
        console.log('BazarFlow Guest UI initialized.');
    }
}

// Safe execution wrapper
document.addEventListener('DOMContentLoaded', () => {
    new App();
});