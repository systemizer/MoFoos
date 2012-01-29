$('#home').live("pagecreate", function() 
				{
					$('#logout-button').click(function(e) 
											  {
												  $.get("/auth/logout/");
												  window.location = "/";
											  });											 
				});