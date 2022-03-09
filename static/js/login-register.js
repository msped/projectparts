$(document).ready(function() {
    $('.submit').on('click', function() {
        var formValid = true;
        $('.form-control').each(function(){
            if ($(this).val() == ''){
                formValid = false;
            }
        });
        if (formValid) {
            $('.submit').hide();
            $('.loading').show();
        }
    });
});