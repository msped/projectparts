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
            
        //Stripe.createToken(card, function(status, response) {
        //    if (status === 200) {
        //        $("#credit-card-errors").hide();
        //        $("#id_stripe_id").val(response.id);

        //        $("#id_credit_card_number").removeAttr('name');
        //        $("#id_cvv").removeAttr('name');
        //        $("#id_expiry_month").removeAttr('name');
        //        $("#id_expiry_year").removeAttr('name');

        //        form.submit();
        //    } else {
        //        $('.loading').hide();
        //        $('.submit').show();
        //        $(".stripe-error-messages").text(response.error.message);
        //        $(".credit-card-errors").show();
        //        $("#validate_card_btn").attr("disabled", false);
        //    }
        //});
        return false;
        }
    });
});