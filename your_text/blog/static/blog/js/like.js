'use strict'

$(".like").on("click", function(){

    var pk = $(this).attr("name");
    var url = $(this).attr("url-like");
    $(this).toggleClass('like-on');

    $.ajax({
        url: url,
        success : function(response){
            if (response['authenticated']) {
                $(`.count-like-${pk}`).html(response['like_count']);
            } else {
                window.location.href = '/auth/login/?next=' + location.href;
            }
        },
        error: function(rs, e) {
            alert(rs.statusText);
        }
    });
});