$(document).ready(function(){
    const form = $('#contact-form');
    form.submit(function(e){
        e.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response){
                console.log(response.sent)
                if(response.sent){
                    $('.contact-form').css('display', 'none');
                    $('.contact-form-success').css('display', 'initial');
                } else {
                    $('#form-errors').text(response)
                }                
            }
        });
        return false
    })
})