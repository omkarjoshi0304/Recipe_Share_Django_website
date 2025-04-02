document.addEventListener('DOMContentLoaded', () => {
    const menuIcon = document.getElementById('menuIcon');
    const mainNav = document.getElementById('mainNav');
    let isOpen = false;

    const toggleMenu = () => {
        isOpen = !isOpen;
        mainNav.style.transform = isOpen ? 'translateX(0)' : 'translateX(-100%)';
        mainNav.style.opacity = isOpen ? '1' : '0';
    };

    menuIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu();
    });

    document.addEventListener('click', (e) => {
        if(isOpen && !mainNav.contains(e.target)) {
            toggleMenu();
        }
    });
});