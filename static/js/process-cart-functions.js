const addItemForm = document.querySelector('form.add-item');
const cartIcon = document.querySelector('a.cart');


cartIcon.addEventListener("click", loadCartInfo);

async function sendRequest(url, method, bodyData=null) {
    request_dict = {
        method: method,
    }

    if (bodyData != null) {
        request_dict.body = bodyData;
    }

    try {
        const response = await fetch(`${window.location.origin}${url}`, request_dict);
        var responseData = await response.json();
    } catch (e) {
        console.error(e);
    }

    return responseData;
}


async function addItemToCart(item_id) {
    event.preventDefault();

    const formData = new FormData(addItemForm);

    var responseData = await sendRequest(`/cart/api_cart_add/${item_id}/`, method='POST', bodyData=formData);

    loadCartInfo();

    const element = document.querySelector('.cart-sidebar');
    element.style.display = "flex";
}


async function setTotalCartQuantity() {
    var responseData = await sendRequest(`/cart/api_cart_get_total_quantity`, method='GET');

    var cartTotalQuantityLabels = document.querySelectorAll('#cartTotalQuantity');
    cartTotalQuantityLabels.forEach((label) => {
        label.textContent = responseData;
    })
}



async function setItemQuantity(item_id, quantity=1) {
    event.preventDefault();

    var quantityForm = event.target.closest('form');
    var input = quantityForm.querySelector('input[name="product-id-quantity"]');
    var newQuantity = parseInt(input.value) + quantity;

    if (newQuantity < 1) { return; }

    const formData = new FormData(quantityForm);

    var responseData = await sendRequest(`/cart/api_cart_set_quantity/${item_id}/${newQuantity}`, method='POST', bodyData=formData);

    if (responseData.success) { 
        reloadCartItem(item_id); 
        setTotalCartQuantity();
    }
}


async function reloadCartItem(item_id) {
    var responseData = await sendRequest(`/cart/api_cart_get_product/${item_id}`, method='GET');

    var itemElement = document.querySelector(`.line-item[item-id="${item_id}"]`);
    var quantityInput = itemElement.querySelector('input[name="product-id-quantity"]');
    var totalPrice = itemElement.querySelector('.line-item-price');

    quantityInput.value = responseData['quantity'];
    totalPrice.textContent = '$' + responseData['total_price'];
}


async function removeItemFromCart(item_id) {
    event.preventDefault();

    var closeIcon = event.target;
    var container = closeIcon.closest('.line-item');
    const removeItemForm = closeIcon.closest('form');

    container.style.display = 'none';
    
    const formData = new FormData(removeItemForm);

    var responseData = await sendRequest(`/cart/api_cart_remove/${item_id}/`, method='POST', bodyData=formData);
}


async function loadCartInfo() {
    loadCartItems();
    setTotalCartQuantity();
}


async function loadCartItems() {
    var responseData = await sendRequest(`/cart/api_cart_detail`, method='GET');

    productsContainer = document.querySelector('.cart-products');
    productsContainer.innerHTML = ''

    new_innerHTML = ''

    for (var product of responseData) {
        image_url = (product['product']['main_img_webp_url'] != '') ? product['product']['main_img_webp_url'] : '/media/fallback.png';
        new_innerHTML += `
        <div class="line-item" item-id="${product['product']['id']}">
            <img src="${image_url}">
            <div class="line-item-info">
                <div class="item-info-header">
                    <p class="line-item-title">${product['product']['title']}</p>
                    <form method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                        <button onclick="removeItemFromCart('${product['product']['id']}')"><span class="material-symbols-outlined">close</span></button>
                    </form>
                </div>
                <div class="item-info-footer">
                    <form class="quantity-selector" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                        <button onclick="setItemQuantity(${product['product']['id']}, quantity=-1)"><span class="down">-</span></button>
                        <input onfocusout="setItemQuantity(${product['product']['id']}, quantity=0)" type="number" inputmode="numeric" name="product-id-quantity" value="${product['quantity']}"/>
                        <button onclick="setItemQuantity(${product['product']['id']})"><span class="up">+</span></button>
                    </form>
                    <p class="line-item-price">$ ${product['total_price']}</p>
                </div>
            </div>
        </div>`
    }

    productsContainer.innerHTML = new_innerHTML;
}

