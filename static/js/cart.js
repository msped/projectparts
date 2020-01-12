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

    $('td').on('click', '.remove-item', function(e) {
        order_id = $(this).closest('td').find('.order-id').val();
        row = $(this).closest('tr');
        template = `<td colspan="4" class="tickets-removed"><p>Ticket(s) Removed.</p></td>`;
        $.ajax({
            url: '/cart/remove/',
            data: {
                'order_id': order_id,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            type: 'POST',
            success: function(d){
                $('#product-count').css('display', 'initial').text(d.cart_amount);
                order_total.text(d.total);
                row.empty().append(template);
                setTimeout(function(){
                    row.fadeOut( 'slow', function(){
                        row.remove();
                    });
                }, 3000);
            }
        });
    });
});
