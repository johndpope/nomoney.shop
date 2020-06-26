$(function(){
    $(".category_btn").click(function() {
    	var collapse_id = $(this).data('target');
    	var category_id = $(this).data('category');
        $.ajax({
	        url : '/category/ajax/' + category_id + '/',
	        type: 'GET',
	        success: function(data){
	        	$(collapse_id).html(data);
	        }
        })
    });
})
