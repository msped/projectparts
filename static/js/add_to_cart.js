$(document).ready(function() {

    $('.add-qty-to-cart').submit(function(e){
        e.preventDefault();

        var qty = $(this).find('.quantity').val();
        var product_id = $(this).find('.product_id').val();
        console.log("qty: " + qty + " Prod id: " + product_id)

        $.ajax({
            url: '/cart/add/',
            data: {
                'qty': qty,
                'product_id': product_id,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            type: 'POST',
            success: function(d){
                $('#cart').animate({color: '#00B500'});
                $('#product-count').css('display', 'initial').text(d.cart_amount);
                $('#cart').animate({color: 'rgba(0, 0, 0, .5)'}, 750);
            }
        })
    })

    if (parseInt(cart_product_count) > 0 ){
        $('#product-count').css('display', 'initial');
    } else {
        $('#product-count').css('display', 'none');
    }
})