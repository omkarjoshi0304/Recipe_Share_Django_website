// Right-click context handling
document.addEventListener('contextmenu', (e) => {
    if (e.target.closest('.recipe-card, .member')) {
        e.preventDefault();
        alert('Content protection: Right-click disabled');
    }
});

// Input field focus assistance
document.querySelectorAll('[data-validation]').forEach(input => {
    input.addEventListener('focus', (e) => {
        const hint = e.target.parentNode.querySelector('.hint');
        if (hint) hint.style.display = 'block';
    });
    
    input.addEventListener('blur', (e) => {
        const hint = e.target.parentNode.querySelector('.hint');
        if (hint) hint.style.display = 'none';
    });
});

// Enhanced hover effects
document.querySelectorAll('.recipe-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
        card.style.boxShadow = '0 8px 15px rgba(0,0,0,0.1)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'none';
        card.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
    });
});