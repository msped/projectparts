$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            url:'competition/get_current/',
            success: function(data){
                if (data !== $('#tickets-left').text()){
                    $('#tickets-left').text(data).animate({color: 'rgb(235, 25, 25)'}).animate({color: '#000'}, 750);
                    console.log("Changed!: " + data);
                }                
            }
        });
    }, 3000);
});