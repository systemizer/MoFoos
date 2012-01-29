function error_dialog(data) {
	$('#error-text').text(data.responseText);
	$('#error-dialog-button').click();
}

function change_page(pageName) {
	$('.ui-page-active').removeClass("ui-page-active");
	$('#'+pageName).addClass("ui-page-active");
}

$('#home').live("pagecreate", function() 
				{
					$('#logout-button').click(function(e) 
											  {
												  $.get("/auth/logout/");
												  window.location = "/";
											  });											 
				});