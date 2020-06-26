$(function(){
    $("#two-tab").click(function() {
        $.ajax({
	        url : '/dashboard/ajax/2d/',
	        type: 'GET',
	        success: function(data){
	            $('#two').html(data);
	        }
        })
    });
})

$(function(){
	$("#three-tab").click(function() {
		$.ajax({
			url : '/dashboard/ajax/3d/',
			type: 'GET',
			success: function(data){
				$('#three').html(data);
			}
		})
	});
})