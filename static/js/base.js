$(document).ready(function() {
    $(".help_button").click(function(){
    	$("#help_block").toggle();
    });
    $("search_toggle").click(function(){
    	$("#search_box").toggle();
    });
	$('#id_text').keydown(function (e) {
	  if ((event.keyCode == 10 || event.keyCode == 13) && event.ctrlKey) {
	    $(this).closest('form').submit();
	  }
	});
});



function load() {
	// chat-(re)load function - could be optimized with timestamp
	var url = $('#chat').data('url');
	$.get(url, function(data) {
		$("#chat_messages").html(data);
	});
}


$(document).ready(function() {
	// send Chat input via Ajax and reload chat
	$('#chat_form').submit(function() {
		$.ajax({
			data : $(this).serialize(),
			method : $(this).attr('method'),
			url : $(this).attr('action'),
			success : function(response) {
				load()
				$('#chat_form')[0].reset()
			}
		});
		return false;
	});
    $("#chat_button").click(function(){
    	load();
    });
});

function initialize_chat(){
	load();
}

$(document).ready(function() {
	$(window).resize(function(){
		var menu_height = $('#main_menu').height();
		$('#wrapper').css('margin-top', menu_height);
	})
	$(function () {
	  $('[data-toggle="tooltip"]').tooltip()
	})
});
