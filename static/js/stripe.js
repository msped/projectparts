$(function() {
    var stripe = Stripe('pk_test_Um7FHiRm0SgosZhvLa3RubN700KnQ9jDll');
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');

    card.addEventListener('change', ({error}) => {
        const displayError = document.getElementById('card-errors');
        if (error) {
          displayError.textContent = error.message;
        } else {
          displayError.textContent = '';
        }
    });

    $('#payment-form').submit(function(e){
        e.preventDefault();
        if ($("#user-answer option:selected").text() !== "Please select an option"){      
            $('.submit').hide();
            $('.loading').show();
            $.ajax({
                type: "POST",
                url: "/checkout/",
                data: {
                    "user-answer": $("#user-answer option:selected").text()
                },
                success: function(data){
                    try {
                        stripe.confirmCardPayment(data, {
                        payment_method: {
                            card: card
                        }
                        }).then(function (result) {
                            if (result.error) {
                                $('.loading').hide();
                                $('.submit').show();
                                $("#card-errors").text(result.error.message);
                                $("#validate_card_btn").attr("disabled", false);
                            } else {
                                // The payment has been processed!
                                if (result.paymentIntent.status === 'succeeded') {
                                    window.location.href = "/checkout/complete/";
                                }
                            }
                        });  
                    }
                    catch(error){
                        console.log(error.message);
                    }
                }
            })
        return false;
        }
    });
});