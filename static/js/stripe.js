$(function() {
    Stripe.setPublishableKey('pk_test_Um7FHiRm0SgosZhvLa3RubN700KnQ9jDll');

    $('#payment-form').submit(function(){
        if ($("#user-answer option:selected").text() !== "Please select an option"){      
            $('.submit').hide();
            $('.loading').show();  
            var form = this;
            var card = {
                number: $("#id_credit_card_number").val(),
                expMonth: $("#id_expiry_month").val(),
                expYear: $("#id_expiry_year").val(),
                cvc: $('#id_cvv').val()
            };
            
        Stripe.createToken(card, function(status, response) {
            if (status === 200) {
                $("#credit-card-errors").hide();
                $("#id_stripe_id").val(response.id);

                $("#id_credit_card_number").removeAttr('name');
                $("#id_cvv").removeAttr('name');
                $("#id_expiry_month").removeAttr('name');
                $("#id_expiry_year").removeAttr('name');

                form.submit();
            } else {
                $('#loading').hide();
                $('#submit').show();
                $("#stripe-error-messages").text(response.error.message);
                $("#credit-card-errors").show();
                $("#validate_card_btn").attr("disabled", false);
            }
        });
        return false;
        }
    });
});