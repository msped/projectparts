$(document).ready(function() {
    const order_total = $('#order-total');

    $('.order-qty').each(function(){
        if ($(this).text() == 1){
           $(this).closest('td').find('#remove-one-item').removeClass('remove-one-item').css('opacity', '0.5');
        }
    });

    $('td').on('click', '.remove-one-item', function(e) {
        order_qty = $(this).closest('td').find('.order-qty');
        order_id = $(this).closest('td').find('.order-id').val();
        $.ajax({
            url:'/cart/remove_one/' + order_id,
            success: function(data){
                order_qty.text(data.qty);
                order_total.text(data.total);
                if (data.qty == 1) {
                    order_qty.closest('td').find('#remove-one-item').removeClass('remove-one-item').css('opacity', '0.5');
                }
            }
        });
    });

    $('td').on('click', '.add-one-item', function(e) {
        order_qty = $(this).closest('td').find('.order-qty');
        order_id = $(this).closest('td').find('.order-id').val();
        $.ajax({
            url:'/cart/add_one/' + order_id,
            success: function(data){
                order_qty.text(data.qty);
                order_total.text(data.total);
                if (data.qty > 1) {
                    order_qty.closest('td').find('#remove-one-item').addClass('remove-one-item').css('opacity', '1');
                }
            }
        });
    });

    $('td').on('click', '.remove-item', function (e) {
        order_id = $(this).closest('td').find('.order-id').val();
        row = $(this).closest('tr');
            $.ajax({
                url: '/cart/remove/',
                data: {
                    'order_id': order_id
                },
                type: 'POST',
                success: function (d) {
                    $('#product-count').css('display', 'initial').text(d.cart_amount);
                    if (d.cart_amount === 0){
                        $('.products').empty().append('<div class="offset-lg-2 col-lg-8 offset-md-2 col-md-8 col-sm-12 col-12 text-center">'+
                        '<p class="text-center no-cart-items">There are no items in your cart, add some <a href="/tickets/">tickets.</a></p>'+
                    '</div>');
                    } else {
                        order_total.text(d.total);
                        setTimeout(function () {
                            row.fadeOut('slow', function () {
                                row.remove();
                            });
                        }, 500);
                    }                    
                }
            });
        }
    });
});
