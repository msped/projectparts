$(document).ready(function() {

    $('.add-qty-to-cart').submit(function(e){
        e.preventDefault();

        var qty = $(this).find('.quantity').val();
        var product_id = $(this).find('.product_id').val();

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
})