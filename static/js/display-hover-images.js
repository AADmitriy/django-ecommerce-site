const allHoverImages = document.querySelectorAll('.hover-container img');
const mainImageContainer = document.querySelector('.main-image')

allHoverImages.forEach((hoverImage) => {
    hoverImage.addEventListener('mouseover', () => {
        mainImageContainer.querySelector('img').src = hoverImage.src;
    })
})