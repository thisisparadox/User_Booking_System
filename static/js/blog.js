document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.main-navigation');
    
    if (menuToggle && nav) {
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            nav.classList.toggle('active');
        });
    }

    // Search functionality
    const searchForm = document.querySelector('.blog-search form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchTerm = this.querySelector('input').value.trim();
            if (searchTerm) {
                // Implement search logic
                console.log('Searching for:', searchTerm);
            }
        });
    }

    // Category filter
    const categoryLinks = document.querySelectorAll('.blog-categories a');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            categoryLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            // Implement category filtering
        });
    });

    // Star rating
    const starInputs = document.querySelectorAll('.star-rating input');
    starInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Update star display
            const value = this.value;
            console.log('Rating:', value);
        });
    });

    // Feedback form
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Form validation and submission
            console.log('Form submitted');
        });
    }
});