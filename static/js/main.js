document.addEventListener('DOMContentLoaded', function () {
    // Oddiy interaktivlik: scroll top linki
    const up = document.querySelector('footer a');
    if (up) {
        up.addEventListener('click', e => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});
