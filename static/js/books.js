document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validate required fields
            const requiredFields = this.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    const errorMsg = field.closest('.form-group').querySelector('.error-message');
                    if (errorMsg) errorMsg.style.display = 'block';
                }
            });
            
            // Validate check-in/check-out dates
            const checkIn = document.getElementById('check-in');
            const checkOut = document.getElementById('check-out');
            if (checkIn.value && checkOut.value && new Date(checkIn.value) >= new Date(checkOut.value)) {
                isValid = false;
                alert('Check-out date must be after check-in date');
            }
            
            if (!isValid) {
                e.preventDefault();
                return;
            }
            
            // In a real implementation, this would submit to the server
            console.log('Booking submitted:', {
                room_type: this.querySelector('#room-type').value,
                check_in: checkIn.value,
                check_out: checkOut.value,
                adults: this.querySelector('#adults').value,
                children: this.querySelector('#children').value,
                first_name: this.querySelector('#first-name').value.trim(),
                last_name: this.querySelector('#last-name').value.trim(),
                email: this.querySelector('#email').value.trim(),
                phone: this.querySelector('#phone').value.trim(),
                special_requests: this.querySelector('#special-requests').value.trim(),
                terms: this.querySelector('#terms').checked
            });
        });
        
        // Hide error messages when user starts typing
        const inputs = this.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                const errorMsg = this.closest('.form-group')?.querySelector('.error-message');
                if (errorMsg) errorMsg.style.display = 'none';
            });
        });
    }
    
    // Dynamic pricing based on room selection
    const roomTypeSelect = document.getElementById('room-type');
    if (roomTypeSelect) {
        roomTypeSelect.addEventListener('change', function() {
            const roomType = this.value;
            // Update the booking summary based on selection
            // This would be more dynamic in a real implementation
            console.log('Room type selected:', roomType);
        });
    }
    
    // Date validation for check-in/check-out
    const checkInInput = document.getElementById('check-in');
    const checkOutInput = document.getElementById('check-out');
    
    if (checkInInput && checkOutInput) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        checkInInput.min = today;
        
        checkInInput.addEventListener('change', function() {
            if (this.value) {
                const nextDay = new Date(this.value);
                nextDay.setDate(nextDay.getDate() + 1);
                checkOutInput.min = nextDay.toISOString().split('T')[0];
            }
        });
    }
});