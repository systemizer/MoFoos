    function update_game(data) {
       $('#players_score').text(data['players_score']);
       $('.players_team').text(data['players_team']);
       $('.opponents_team').text(data['opponents_team']);
       $('#opponents_score').text(data['opponents_score']);
	   $('#current_game').attr("gid",data['gid']);	
       if (data['players_score']===10) {
	       $("#winner").text(data['players_team']);
           win();
       } else if (data['opponents_score'] === 10) {
	       $("#winner").text(data['opponents_team']);
           lose();
       }
    }
  
   function win() {
	   change_page("win");
    }
   function lose() {
	   change_page("lose");
    }  

	$('#game').live('pagecreate',function() {
	   $('#score-button').click(function(event) {
	      var game_id = $('#current_game').attr('gid');
          $.ajax({'url':'/action/increment_score/',
                  'type':'GET',
                  'dataType':'json',
                  'data':{'gid':game_id},
                  'success' : update_game, 
                  'error' : function() {alert('error')} //to fix
                });
       });
	   $('#decrement-score-button').click(function(event) {
	      var game_id = $('#current_game').attr('gid');
          $.ajax({'url':'/action/decrement_score/',
                  'type':'GET',
                  'dataType':'json',
                  'data':{'gid':game_id},
                  'success' : update_game, 
                  'error' : function() {alert('error')} //to fix
                });
	   });
	   $('#refresh-score-button').click(function(event) {
	      var game_id = $('#current_game').attr('gid');
          $.ajax({'url':'/action/refresh_score/',
                  'type':'GET',
                  'dataType':'json',
                  'data':{'gid':game_id},
                  'success' : update_game, 
                  'error' : function() {alert('error')} //to fix
                });
       });

	});
