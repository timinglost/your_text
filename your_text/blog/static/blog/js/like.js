'use strict'

$(".like").on("click", function(){

    var pk = $(this).attr("name");
    var url = $(this).attr("url-like");
    $(this).toggleClass('like-on');

    $.ajax({
        url: url,
        success : function(response){
            $(`.count-like-${pk}`).html(response['like_count']);
        },
        error: function(rs, e) {
            alert(rs.statusText);
        }
    });
});