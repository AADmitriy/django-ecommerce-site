var minPriceLabel = document.getElementById('min_price');
var maxPriceLabel = document.getElementById('max_price');

const rangeFill = document.querySelector('.range-fill-green');

function validateRange() {
    var minPriceValue = parseInt(inputElements[0].value);
    var maxPriceValue = parseInt(inputElements[1].value);
    
    if (minPriceValue > maxPriceValue) {
        var tempValue = minPriceValue;
        minPriceValue = maxPriceValue;
        maxPriceValue = tempValue;
    }

    minPricePercent = ((minPriceValue - 10)/490) * 100;
    maxPricePercent = ((maxPriceValue - 10)/490) * 100;

    rangeFill.style.left = minPricePercent + "%";
    rangeFill.style.width = maxPricePercent - minPricePercent + "%";

    minPriceLabel.textContent = minPriceValue + "$";
    maxPriceLabel.textContent = maxPriceValue + "$";
}

const inputElements = document.querySelectorAll('input[type="range"]');

inputElements.forEach((element) => {
    
    element.addEventListener("input", validateRange);
});

validateRange();