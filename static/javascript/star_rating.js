document.querySelectorAll('.star-rating').forEach(rating => {
    const stars = rating.querySelectorAll('span');
    const inputId = rating.dataset.field;
    const input = document.getElementById(inputId);

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const value = star.dataset.value;
            input.value = value;

            stars.forEach(s => {
                s.textContent = s.dataset.value <= value ? '★' : '☆';
            });
        });
    });
});
