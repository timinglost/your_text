'use strict'

 $(document).ready(function(){
       $("#UserComment").submit(function(e){
            var pk = $(this).attr("post-pk");
            e.preventDefault();
            var serializedData = $(this).serialize();
            $.ajax({
                type : 'POST',
                url :  "/blog/post/comment/" + pk,
                data : serializedData,
                success : function(response){
                    $('.media-list').html(response['result']);
                    $('.comm-count').html(response['comment_count']);
                    e.target.reset();
                },
                error : function(rs, e){
                    alert(rs.statusText);
                }
            });
       });
    });
