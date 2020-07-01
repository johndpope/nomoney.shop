$(document).ready(function() {
	$("#live_search").on('input', function(e) {
		var search_string = $(this).val();
		if (search_string == ''){
				$('#search_results').empty();
		}else{
			$.ajax({
				url : '/search/ajax/live/' + search_string + '/',
				type: 'GET',
				success: function(data){
					$('#search_results').html(data);
				}
			})
		}
	});
});