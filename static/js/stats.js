$(document).ready(
function() 
	{
		$('.comment-button').click(function() 
								   {
									   var uid = $(this).attr("id").split("-")[1];
									   console.log(uid);
									   var commentbox = $("#commentbox-"+uid);
									   if (commentbox.css("display")=="none")
										   commentbox.css("display","block");
									   else
										   commentbox.css("display","none");										   
									   
								   });		
		$('.commentbox form').submit(function(e) 
									  {			
										  var action=$(this).attr("action");
										  e.preventDefault();
										  $.ajax(
											  {
												  'url':action,
												  'type':'post',
												  'data':$(this).serialize(),
												  'success':function(data) {window.location="/stats/"},
												  'error':function(data) {alert('failure');}
											  }
										  );
									  });
		/* hack */
		$('.commentbox textarea').attr('rows','2').addClass("span9");
		
	});