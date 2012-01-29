$("#register").live("pagecreate",function() {
       $('#register-form').submit(function(e) {
	   e.preventDefault();
	   $.ajax({'url':'/register/',
			   'data':$('#register-form').serialize(),
			   'type':'post',			   
	           'success': function() {window.location = "/"},
	           'error': error_dialog
			  });
		});
	   $('#register-form-submit').click(function(e) {
											 $('#register-form').submit();
											 return false;
										 });

});
