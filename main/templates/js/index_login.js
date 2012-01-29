$("#login").live("pagecreate",function() {
       $('#login-form').submit(function(e) {
	   e.preventDefault();
	   $.ajax({'url':'/login/',
			   'data':$('#login-form').serialize(),
			   'type':'post',			   
	           'success': function() {window.location = "/"},
	           'error': error_dialog
			  });
		});
	   $('#login-form-submit').click(function(e) {
											 $('#login-form').submit();
											 return false;
										 });

});
