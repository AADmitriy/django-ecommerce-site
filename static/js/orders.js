window.onload = loadCheckoutItems();

async function loadCheckoutItems(){
    try {
        const response = await fetch(`${window.location.origin}/cart/api_cart_detail`, {
            method: 'GET'
        });
        var responseData = await response.json();
    } catch (e) {
        console.error(e);
    }

    var productLists = document.querySelectorAll('.product-list');
    var newProductListHTML = '';

    for (var product of responseData) {
        var image_url = (product['product']['main_img_url'] != '') ? product['product']['main_img_url'] : '/media/fallback.png';
        newProductListHTML += `
        <div class="checkout-product">
            <div class="product-image-wrapper">
                <img src="${image_url}">
                <label class="quantity-number">${product['quantity']}</label>
            </div>
            <p class="checkout-product-title">${product['product']['title']}</p>
            <p class="checkout-product-price">$ ${product['total_price']}</p>
        </div>`;
    }

    for (var productList of productLists) {
        productList.innerHTML = newProductListHTML;   
    }
}

var userAddreses = document.getElementById('user_addreses_select');
fillAddressFields();
userAddreses.addEventListener('change', fillAddressFields);

function fillAddressFields() {
    var address_id = userAddreses.value;
    
    var country_selector = document.querySelector('#id_country');
    country_selector.value = addresses_dict[address_id]['country_id'];
    var address_field = document.querySelector('input[name="address"]');
    address_field.value = addresses_dict[address_id]['address'];
    var city_field = document.querySelector('input[name="city"]');
    city_field.value = addresses_dict[address_id]['city'];
    var zipCode_field = document.querySelector('input[name="zipCode"]');
    zipCode_field.value = addresses_dict[address_id]['zipCode'];
}

var paymentChoices = document.querySelectorAll('input[name="card-choice"]');
var paypalFormWrapper = document.querySelector('.paypal-form');
var payButton = document.querySelector('.pay-button');

paymentChoices.forEach((toggle) => {
    toggle.addEventListener('change', changePaypalFormVisability);
});

function changePaypalFormVisability() {
    toggle = event.target;
    if (toggle.value == 'paypal') {
        payButton.style.display = 'none';
        paypalFormWrapper.style.display = 'block';
    }
    else {
        payButton.style.display = 'block';
        paypalFormWrapper.style.display = 'none';
    }
}

var paypalForm = paypalFormWrapper.querySelector('form');

paypalForm.addEventListener('click', saveOrderInfo);

async function saveOrderInfo() {
    event.preventDefault();
    var addressForm = document.querySelector('.shipping-address-info');
    var requiredInputs = addressForm.querySelectorAll("[required]");
    for (var i of requiredInputs) {
        if (!i.value) { 
            i.focus();
            return; 
        }
    }

    form = document.querySelector('form.order-info-form');

    const formData = new FormData(form);

    try {
        const response = await fetch(`${window.location.origin}/orders/payment_page`, {
            method: "POST",
            body: formData,
        });
        var responseData = await response.json();
    } catch (e) {
        console.error(e);
    }

    var return_url = paypalForm.querySelector('input[name="return"]');
    if (!return_url.value.includes('?order_id=')) {
        return_url.value = return_url.value + `?order_id=${responseData.order_id}`;
    }

    var item_name = paypalForm.querySelector('input[name="item_name"]');
    if (!item_name.value.includes(`${responseData.order_id}`)) {
        item_name.value = item_name.value + `${responseData.order_id}`;
    }
    
    var invoice = paypalForm.querySelector('input[name="invoice"]');
    invoice.value = `${responseData.order_id}`;
    
    paypalForm.setAttribute('inert', '');
    document.querySelector('.page-loader').style.display = 'flex'
    paypalForm.submit();
}
