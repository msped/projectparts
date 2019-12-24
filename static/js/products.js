$(document).ready(function(){
    $('#make').on('change', function(){
        $('.added-value-model').remove();
        var make = $('#make').find(":selected").text();
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/tickets/models/',
            data: {
                'make': make,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            success: function(result){
                for (var d of result){
                    var template = '<option class="added-value-model" value="' + d + '">' + d + '</option>'; 
                    $('#model').append(template);
                }                
            }
        });
    });

    $('#model').on('change', function(){
        $('.added-value-generation').remove();
        var make = $('#make').find(":selected").text();
        var model = $('#model').find(":selected").text();
        $.ajax({
            type: 'POST',
            url: '/tickets/gens/',
            data: {
                'make': make,
                'model': model,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            success: function(result){
                for ( var d of result){
                    var template = '<option class="added-value-generation" value="' + d + '">' + d + '</option>'; 
                    $('#generation').append(template);
                }        
            }
        });
    });
});