'use strict'

$(".sub").on("click", function(){

    var pk = $(this).attr("id");
    var url = $(this).attr("url-sub");

    $.ajax({
        url: url,
        success : function(response){
            if (response['authenticated']) {
                if (response['sub']) {
                    $('.sub').html('отписаться');
                } else {
                    $('.sub').html('подписаться')
                }
            } else {
                window.location.href = '/auth/login/?next=' + location.href;
            }
        },
        error: function(rs, e) {
            console.log(rs);
            alert(rs.statusText);
        }
    });
});