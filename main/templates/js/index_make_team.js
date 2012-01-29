	$("#make_team").live("pagecreate",function() {
       $('#make-team-form').submit(function(e) {
	   e.preventDefault();
	   $.ajax({'url':'/make_team/',
			   'data':$('#make-team-form').serialize(),
			   'type':'post',			   
	           'success': function() {window.location = "/"},
	           'error': error_dialog
			  });
		});
	   $('#make-team-form-submit').click(function(e) {
											 $('#make-team-form').submit();
											 return false;
										 });

});
