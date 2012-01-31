    function update_game(data) {
       $('span.players_score').text(data['players_score']);
       $('span.players_team').text(data['players_team']);
       $('span.opponents_team').text(data['opponents_team']);
       $('span.opponents_score').text(data['opponents_score']);
	   $('#current_game').attr("gid",data['gid']);	
		t = data;
	   if (!data['is_valid']) {
		   $('#game-not-valid').css('display','block')		
	   } else {
		   $('#game-not-valid').css('display','none')		
	   }
       if (data['players_score']>=10) {
	       $("#winner").text(data['players_team']);
           win();
       } else if (data['opponents_score']>=10) {
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
		  $players_score = $('span.payers_score');
		  var cur_score = parseInt($players_score.text());
		  if (cur_score)
             $players_score.text(cur_score+1);								  
	      var game_id = $('#current_game').attr('gid');
          $.ajax({'url':'/action/increment_score/',
                  'type':'GET',
                  'dataType':'json',
                  'data':{'gid':game_id},
                  'success' : update_game, 
                  'error' : error_dialog
                });
       return false;
       });
	   $('#decrement-score-button').click(function(event) {
		  $players_score = $('span.payers_score');
		  var cur_score = parseInt($players_score.text());
		  if (cur_score)
             $players_score.text(cur_score-1);								  
	      var game_id = $('#current_game').attr('gid');
          $.ajax({'url':'/action/decrement_score/',
                  'type':'GET',
                  'dataType':'json',
                  'data':{'gid':game_id},
                  'success' : update_game, 
                  'error' : error_dialog
                });
       return false;
	   });
	   $('#refresh-score-button').click(function(event) {
		  event.preventDefault();
	      var game_id = $('#current_game').attr('gid');
          $.ajax({'url':'/action/refresh_score/',
                  'type':'GET',
                  'dataType':'json',
                  'data':{'gid':game_id},
                  'success' : update_game, 
                  'error' : error_dialog
                 });
          return false;											
       });
	   $('#end-game-button').click(function(event) {
		  event.preventDefault();
	      var game_id = $('#current_game').attr('gid');
          $.ajax({'url':'/action/end_game/',
                  'type':'GET',
                  'dataType':'json',
                  'data':{'gid':game_id},
                  'success' : function() {window.location="/"},
                  'error' : function(data) {window.location="/";} //weird bug!!
                });
       return false;
       });


	});
