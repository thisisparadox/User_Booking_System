document.addEventListener('DOMContentLoaded', function() {
    // Initialize Google Map
    window.initMap = function() {
        const location = { lat: 9.3333, lng: 122.8633 };
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 15,
            center: location,
            styles: [
                {
                    "featureType": "poi",
                    "stylers": [{ "visibility": "off" }]
                }
            ]
        });
        new google.maps.Marker({
            position: location,
            map: map,
            title: "Storm's Beach and Country Club"
        });
    };

    // Contact form submission
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Form validation
            const name = this.querySelector('#name').value.trim();
            const email = this.querySelector('#email').value.trim();
            const message = this.querySelector('#message').value.trim();
            
            if (!name || !email || !message) {
                alert('Please fill in all required fields');
                return;
            }
            
            // In a real implementation, this would submit to the server
            console.log('Contact form submitted:', {
                name,
                email,
                phone: this.querySelector('#phone').value.trim(),
                subject: this.querySelector('#subject').value,
                message
            });
            
            // Show success message
            alert('Thank you for your message! We will respond within 24 hours.');
            this.reset();
        });
    }
    
    // FAQ accordion functionality
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const answer = this.nextElementSibling;
            const isOpen = answer.style.display === 'block';
            
            // Close all answers first
            document.querySelectorAll('.faq-answer').forEach(ans => {
                ans.style.display = 'none';
                ans.previousElementSibling.classList.remove('active');
            });
            
            // Toggle this answer
            if (!isOpen) {
                answer.style.display = 'block';
                this.classList.add('active');
            }
        });
    });
});