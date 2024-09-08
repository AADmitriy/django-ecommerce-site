var filters = document.querySelector('.filters');
var mobile_filters = document.querySelector('.filters_mobile');
var productsContainer = document.querySelector('.products_container');

var categoryToggles = null;
var minPriceInput = null;
var maxPriceInput = null;
var sortToggles = null;
var searchBar = null;
var searchButton  = null;

function isHidden(el) {
    var style = window.getComputedStyle(el);
    return (style.display === 'none')
}

searchButton = document.querySelector('.search_bar button');
searchBar = document.querySelector('.search_bar input');

if (!isHidden(filters)) {
    categoryToggles = filters.querySelectorAll('.category-wrapper input');
    minPriceInput = filters.querySelector('.price-range input[name="min-price"]');
    maxPriceInput = filters.querySelector('.price-range input[name="max-price"]');
    sortToggles = filters.querySelectorAll('.filter-wrapper input');
}
else {
    categoryToggles = mobile_filters.querySelectorAll('.category-select');
    minPriceInput = mobile_filters.querySelector('.price-range input[name="min-price"]');
    maxPriceInput = mobile_filters.querySelector('.price-range input[name="max-price"]');
    sortToggles = mobile_filters.querySelectorAll('.sort-select');
}


function loadProducts() {
    productsContainer.innerHTML = ''
    productsContainer.classList = "products-loader"
    
    var name_like = searchBar.value;
    if (!isHidden(filters)) {
        var category = filters.querySelector('.category-wrapper input:checked').value;
        var minPrice = minPriceInput.value;
        var maxPrice = maxPriceInput.value;
        var sort_by = filters.querySelector('.filter-wrapper input:checked').value;
    }
    else {
        var category = categoryToggles[0].value;
        var minPrice = minPriceInput.value;
        var maxPrice = maxPriceInput.value;
        var sort_by = sortToggles[0].value;
    }

    const paramsArray = []
    if (category != '') {
        paramsArray.push(['category', category]);
    }
    if (minPrice != '') {
        paramsArray.push(['min_price', minPrice]);
    }
    if (maxPrice != '') {
        paramsArray.push(['max_price', maxPrice]);
    }
    if (sort_by != '') {
        paramsArray.push(['sort_by', sort_by]);
    }
    if (name_like != '') {
        paramsArray.push(['name_like', name_like]);
    }
 
    const params = new URLSearchParams(paramsArray);

    sendAndProcessRequest(params);
}

async function sendAndProcessRequest(params) {
    try {
        const response = await fetch(`${window.location.origin}/api/products?${params}`, {
            method: "GET",
        });
        var responseData = await response.json();
    } catch (e) {
        console.error(e);
    }

    //productsContainer = document.querySelector('.products_container');
    //productsContainer.innerHTML = ''

    new_innerHTML = ''

    for (var productInfo of responseData) {
        new_innerHTML += `
        <a href="/product_page/${productInfo.id}">
            <div class="product">
                <img src="${productInfo.main_img_webp_url}" onerror="if (this.src != 'media/fallback.png') this.src = 'media/fallback.png';">
                <div class="product-info">
                    <h4 class="product_title">${productInfo.title}</h4>
                    <p>Price: <span>${productInfo.price}</span>$</p>
                    <p>${productInfo.date}</p>
                </div>
            </div>
        </a>`
    }

    productsContainer.classList = "products_container";

    productsContainer.innerHTML = new_innerHTML;

}

categoryToggles.forEach((toggle) => {
    toggle.addEventListener('change', loadProducts);
});

minPriceInput.addEventListener('focusout', loadProducts);

maxPriceInput.addEventListener('focusout', loadProducts);

sortToggles.forEach((toggle) => {
    toggle.addEventListener('change', loadProducts);
});

searchButton.addEventListener('click', loadProducts);

searchBar.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        searchButton.click();
    }
});
