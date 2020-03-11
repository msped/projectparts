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
        if (confirm("Do you wish to remove this item from your cart?")) {
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({ 
                beforeSend: function(xhr, settings) {
                    function getCookie(name) {
                        var cookieValue = null;
                        if (document.cookie && document.cookie != '') {
                            var cookies = document.cookie.split(';');
                            for (var i = 0; i < cookies.length; i++) {
                                var cookie = jQuery.trim(cookies[i]);
                                // Does this cookie string begin with the name we want?
                                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                    break;
                                }
                            }
                        }
                        return cookieValue;
                    }
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                } 
            });
            $.ajax({
                url: '/cart/remove/',
                data: {
                    'order_id': order_id
                },
                type: 'POST',
                success: function (d) {
                    $('#product-count').css('display', 'initial').text(d.cart_amount);
                    order_total.text(d.total);
                    setTimeout(function () {
                        row.fadeOut('slow', function () {
                            row.remove();
                        });
                    }, 500);
                }
            });
        }
    });
});
