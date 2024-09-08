function showElement(selector, display_style="flex") {
    event.preventDefault();
    const element = document.querySelector(`${selector}`);
    element.style.display = display_style;
}

function hideElement(selector) {
    event.preventDefault();
    const element = document.querySelector(selector);
    element.style.display = "none";
}
