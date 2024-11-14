document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const successContainer = document.querySelector('.success-container');
        successContainer.classList.add('visible');
    }, 500); // delay to match the pop-in animation
});
