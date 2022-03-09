$(document).ready(function() {
    if (parseInt(cart_product_count) > 0 ){
        $('#product-count').css('display', 'initial');
    } else {
        $('#product-count').css('display', 'none');
    }
});