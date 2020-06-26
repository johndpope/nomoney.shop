$(function(){
	$("#live_search").click(function() {
		$.ajax({
			url : '/search/ajax/live/3d/',
			type: 'GET',
			success: function(data){
				$('#search_result').html(data);
			}
		})
	});
})