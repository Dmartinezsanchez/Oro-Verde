document.addEventListener('DOMContentLoaded', function() {
    const termsSection = document.getElementById('terms_section');
    const showMoreBtn = document.getElementById('showMoreBtn');
    const showLessBtn = document.getElementById('showLessBtn');

    showMoreBtn.addEventListener('click', function() {
        termsSection.style.display = 'block';
        showMoreBtn.style.display = 'none';
        showLessBtn.style.display = 'inline-block';
    });

    showLessBtn.addEventListener('click', function() {
        termsSection.style.display = 'none';
        showMoreBtn.style.display = 'inline-block';
        showLessBtn.style.display = 'none';
    });
});
