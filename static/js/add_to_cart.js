$(document).ready(function() {

    $('.add-qty-to-cart').submit(function(e){
        e.preventDefault();

        form = $(this);

        var qty = form.find('.quantity').val();
        var product_id = form.find('.product_id').val();

        $.ajax({
            url: '/cart/add/',
            data: {
                'qty': qty,
                'product_id': product_id,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            type: 'POST',
            success: function(d){

                if (window.location.pathname == "/tickets/" + product_id + "/") {
                    form.closest('.add').children('.add-options').fadeOut('fast', function(){
                        form.closest('.add').children('.added-to-cart').fadeIn();
                    });
                    $('#product-count').css('display', 'initial').text(d.cart_amount);
                    setTimeout(function(){
                        form.closest('.add').children('.added-to-cart').fadeOut('fast', function(){
                            form.closest('.add').children('.add-options').fadeIn(); 
                        });
                    }, 3000)
                } else {
                    form.closest('.card-footer').children('.add-options').fadeOut('fast', function(){
                        form.closest('.card-footer').children('.added-to-cart').fadeIn();
                    });
                    $('#product-count').css('display', 'initial').text(d.cart_amount);
                    setTimeout(function(){
                        form.closest('.card-footer').children('.added-to-cart').fadeOut('fast', function(){
                            form.closest('.card-footer').children('.add-options').fadeIn(); 
                        });
                    }, 3000)
                }
                
                
            }
        })
    })
})