function get_game(data) {
	update_game(data);
	change_page("game");
}

$("#new_game").live("pagecreate",function() {
       $('#new-game-form').submit(function(e) {
	   e.preventDefault();
	   $.ajax({'url':'/new_game/',
			   'data':$('#new-game-form').serialize(),
			   'type':'post',		
			   'dataType':'json',
	           'success': get_game,
	           'error': error_dialog
			  });
		});
	   $('#new-game-form-submit').click(function(e) {
											 $('#new-game-form').submit();
											 return false;
										 });

});
