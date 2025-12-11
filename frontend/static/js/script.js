document.addEventListener('DOMContentLoaded', function() {
    // Card hover effects
    const cards = document.querySelectorAll('.cards');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2)';
            this.style.zIndex = '1000';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.zIndex = '0';
        });
    });
});
