console.log('product.js loaded...');

$(document).ready(function() {
    
    $.ajax({
        url: "/get-product-details/",
        type: "POST",
        data: {
            'product_id': '{{ product.id }}',
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function(response) {
            $('#product-description').text(response.description);
            $('#product-image').attr('src', response.image_url);
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        },
        complete: function() {
            // Remove the 'is-loading' class from the spinner element after the Ajax call is complete
            $('.loading-spinner').removeClass('is-loading');
        }
    });
});