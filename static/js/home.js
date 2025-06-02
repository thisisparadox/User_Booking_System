document.addEventListener('DOMContentLoaded', function() {
    // Hero slider functionality
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const dotsContainer = document.querySelector('.slide-dots');
    const prevBtn = document.querySelector('.prev-slide');
    const nextBtn = document.querySelector('.next-slide');
    
    // Create dots
    if (slides.length && dotsContainer) {
        slides.forEach((_, index) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (index === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(index));
            dotsContainer.appendChild(dot);
        });
    }
    
    function updateSlider() {
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === currentSlide);
        });
        
        // Update dots
        const dots = document.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }
    
    function goToSlide(index) {
        currentSlide = (index + slides.length) % slides.length;
        updateSlider();
    }
    
    function nextSlide() {
        goToSlide(currentSlide + 1);
    }
    
    function prevSlide() {
        goToSlide(currentSlide - 1);
    }
    
    // Event listeners for buttons
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    
    // Auto-advance slides
    let slideInterval = setInterval(nextSlide, 5000);
    
    // Pause on hover
    const slider = document.querySelector('.slider-container');
    if (slider) {
        slider.addEventListener('mouseenter', () => clearInterval(slideInterval));
        slider.addEventListener('mouseleave', () => {
            slideInterval = setInterval(nextSlide, 5000);
        });
    }
    
    // Booking widget form
    const bookingWidget = document.querySelector('.booking-form');
    if (bookingWidget) {
        bookingWidget.addEventListener('submit', function(e) {
            e.preventDefault();
            const serviceType = this.querySelector('#service-type').value;
            const checkIn = this.querySelector('#check-in').value;
            const checkOut = this.querySelector('#check-out').value;
            
            if (!serviceType || !checkIn || !checkOut) {
                alert('Please fill in all fields');
                return;
            }
            
            // In a real implementation, this would check availability
            console.log('Checking availability for:', {
                serviceType,
                checkIn,
                checkOut
            });
            
            // Redirect to booking page with parameters
            window.location.href = `book.html?service=${serviceType}&checkin=${checkIn}&checkout=${checkOut}`;
        });
    }
    
    // Animate stats counter
    const statNumbers = document.querySelectorAll('.stat-number');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = +entry.target.getAttribute('data-count');
                const count = +entry.target.innerText;
                const increment = target / 100;
                
                if (count < target) {
                    entry.target.innerText = Math.ceil(count + increment);
                    setTimeout(() => observer.observe(entry.target), 10);
                } else {
                    entry.target.innerText = target;
                }
            }
        });
    }, { threshold: 0.5 });
    
    statNumbers.forEach(stat => observer.observe(stat));
    
    // Facilities tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Update active tab button
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabId) {
                    content.classList.add('active');
                }
            });
        });
    });
});