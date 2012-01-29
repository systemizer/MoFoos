$("#register").live("pagecreate",function() {
       $('#register-form').submit(function(e) {
	   e.preventDefault();
	   $.ajax({'url':'/register/',
			   'data':$('#register-form').serialize(),
			   'type':'post',			   
	           'success': function() {window.location = "/"},
	           'error': function() {alert("bad!!")}
			  });
		});
});
