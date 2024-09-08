function showNextElement(element) {
    var targetElement = element.closest('.widget-toggle').nextSibling.nextSibling;
    targetElement.style.display = "grid";
    element.textContent = "remove";
    element.setAttribute('onclick', "hideNextElement(this)");
}

function hideNextElement(element) {
    var targetElement = element.closest('.widget-toggle').nextSibling.nextSibling;
    targetElement.style.display = "none";
    element.textContent = "add";
    element.setAttribute('onclick', "showNextElement(this)")
}