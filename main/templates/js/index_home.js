function error_dialog(data) {
	$('#error-text').text(data.responseText);
	$('#error-dialog-button').click();
}

function change_page(pageName) {
	$('#change-page-'+pageName).click();
}

function poll() {
	console.log("polling...");
	if ($("#game").hasClass("ui-page-active") && $('#current_game').attr("gid")) {
		var gameId = $('#current_game').attr("gid");
		$.ajax({'url':'/action/refresh_score/',
				'type':'GET',
				'dataType':'json',
				'data':{'gid':gameId},
				'success' : update_game
			   });
		}
	setTimeout(poll,20000);
}



function join_game(gameId) {
	$("#current_game").attr("gid",gameId)
	$.ajax({'url':'/action/refresh_score/',
            'type':'GET',
            'dataType':'json',
            'data':{'gid':gameId},
            'success' : update_game, 
            'error' : error_dialog
           });
	change_page("game");		
}

$('#home').live("pagecreate", function() 
				{
					poll();
					$('#logout-button').click(function(e) 
											  {
												  $.get("/auth/logout/");
												  window.location = "/";
											  });											 
					$('.join_game').click(function(e) {
											  join_game($(this).attr('id'));
											  return false;
										  });
				});