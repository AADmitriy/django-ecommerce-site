var resend_button = document.getElementById('email_resend');

resend_button.addEventListener('click', resend_verify_code);

async function resend_verify_code() {
    event.preventDefault()
    var full_url = window.location.href;
    var url_array = full_url.split('/');
    var user_id = url_array[url_array.length - 2];

    var form = resend_button.closest('form');
    var formData = new FormData(form)

    try {
        const response = await fetch(`${window.location.origin}/accounts/resend_verify_email/${user_id}/`, {
            method: "POST",
            body: formData,
        });
        //var responseData = await response.json();
    } catch (e) {
        console.error(e);
    }
}