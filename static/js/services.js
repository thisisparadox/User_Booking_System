document.addEventListener('DOMContentLoaded', function() {
    // Image gallery functionality
    const mainImage = document.querySelector('.main-image');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (thumbnails.length) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                const newImageUrl = this.style.backgroundImage;
                mainImage.style.backgroundImage = newImageUrl;
                
                // Update active thumbnail
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
        
        // Set first thumbnail as active
        thumbnails[0].classList.add('active');
    }
    
    // Smooth scrolling for service navigation
    const navLinks = document.querySelectorAll('.services-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop - 100,
                    behavior: 'smooth'
                });
                
                // Update active nav link
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
    
    // Highlight current section in nav as user scrolls
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        
        document.querySelectorAll('.service-section').forEach(section => {
            const sectionTop = section.offsetTop - 150;
            const sectionBottom = sectionTop + section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
});