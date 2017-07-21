var barca_array = [
	[".",".",".",".","BE1","BE2",".",".",".","."],
	[".",".",".","BL1","BR1","BR2","BL2",".",".","."],
	[".",".",".",".",".",".",".",".",".","."],
	[".",".",".",".",".",".",".",".",".","."],
	[".",".",".",".",".",".",".",".",".","."],
	[".",".",".",".",".",".",".",".",".","."],
	[".",".",".",".",".",".",".",".",".","."],
	[".",".",".",".",".",".",".",".",".","."],
	[".",".",".","WL1","WR1","WR2","WL2",".",".","."],
	[".",".",".",".","WE1","WE2",".",".",".","."]
];

/*Extra information that is necessary to retrieve information about 
pieces on the board quickly*/
var piece_locations = {
	"BE1": 04,
	"BE2": 05,
	"BL1": 13,
	"BR1": 14,
	"BR2": 15,
	"BL2": 16,
	"WL1": 83,
	"WR1": 84,
	"WR2": 85,
	"WL2": 86,
	"WE1": 94,
	"WE2": 95
};
var pieces_afraid_of = {
	"WE1": ["BR1","BR2"],
	"WE2": ["BR1","BR2"],
	"BE1": ["WR1","WR2"],
	"BE2": ["WR1","WR2"],
	"WL1": ["BE1","BE2"],
	"WL2": ["BE1","BE2"],
	"BL1": ["WE1","WE2"],
	"BL2": ["WE1","WE2"],
	"WR1": ["BL1","BL2"],
	"WR2": ["BL1","BL2"],
	"BR1": ["WL1","WL2"],
	"BR2": ["WL1","WL2"]
};
var clicks_made = [];
var player_TURN = "WHITE";
var valid_clicks = [];
var scared_pieces = new Set();
var trapped_pieces = [];
var victory = false;
var who_won = "";
var mode = "PLAYER V. PLAYER";

function checkForValue(i,j){
	if((i+j)%2 != 0)
	{
		return "smallBox1"; 
	}
	else
	{
		return "smallBox2";
	}
}

/*Function that initializes the board*/
function newBoard(){
	var output = "";
	for(var i = 0; i < 10; i++){
		for(var j = 0; j < 10; j++){
			var title = "tile_"+i+","+j;
			output += '<div id= \''+title+'\' class="'+ checkForValue(i,j) + '" onclick = "clickMade(\''+i+'\',\''+j+'\',\''+title+'\',\''+barca_array[i][j]+'\')"></div>';
		}
	}
	document.getElementById('barca_board').innerHTML = output;
}

/*Function that positions initial images onto the board*/
function placeInitImage(){
	document.getElementById('tile_0,4').innerHTML += '<img src = "./images/ElephantB.png"/>';
	document.getElementById('tile_0,5').innerHTML += '<img src = "./images/ElephantB.png"/>';
	document.getElementById('tile_9,4').innerHTML += '<img src = "./images/elephantW.gif"/>';
	document.getElementById('tile_9,5').innerHTML += '<img src = "./images/elephantW.gif"/>';
	document.getElementById('tile_1,3').innerHTML += '<img src = "./images/LionB.png"/>';
	document.getElementById('tile_1,4').innerHTML += '<img src = "./images/MouseB.png"/>';
	document.getElementById('tile_1,5').innerHTML += '<img src = "./images/MouseB.png"/>';
	document.getElementById('tile_1,6').innerHTML += '<img src = "./images/LionB.png"/>';
	document.getElementById('tile_8,3').innerHTML += '<img src = "./images/lionW.gif"/>';
	document.getElementById('tile_8,4').innerHTML += '<img src = "./images/mouseW.gif"/>';
	document.getElementById('tile_8,5').innerHTML += '<img src = "./images/mouseW.gif"/>';
	document.getElementById('tile_8,6').innerHTML += '<img src = "./images/lionW.gif"/>';
}

/*Initializes the initial valid clicks on the board*/
function initValidClicks(){
	if(player_TURN == "WHITE"){
		valid_clicks.push(83);
		valid_clicks.push(84);
		valid_clicks.push(85);
		valid_clicks.push(86);
		valid_clicks.push(94);
		valid_clicks.push(95);		
	}
	else if(mode == "PLAYER V. AI"){
		getAIMove();
	}
	else{
		barca_array[0][4] = "WE1";
		barca_array[0][5] = "WE2";
		barca_array[1][3] = "WL1";
		barca_array[1][4] = "WR1";
		barca_array[1][5] = "WR2";
		barca_array[1][6] = "WL2";
		barca_array[8][3] = "BL1";
		barca_array[8][4] = "BR1";
		barca_array[8][5] = "BR2";
		barca_array[8][6] = "BL2";
		barca_array[9][4] = "BE1";
		barca_array[9][5] = "BE2";
		
		/*Set where pieces are located on the board*/
		piece_locations["WE1"] = 4;
		piece_locations["WE2"] = 5;
		piece_locations["WL1"] = 13;
		piece_locations["WR1"] = 14;
		piece_locations["WR2"] = 15;
		piece_locations["WL2"] = 16;
		piece_locations["BL1"] = 83;
		piece_locations["BR1"] = 84;
		piece_locations["BR2"] = 85;
		piece_locations["BL2"] = 86;
		piece_locations["BE1"] = 94;
		piece_locations["BE2"] = 95;
	}
}

/*Returns the direction of movement*/
function directionMovedIn(from_row,from_col,to_row,to_col)
{
	if(from_row-to_row == 0 && from_col-to_col == 0){
		return "INVALID";
	}
	if(from_row-to_row == 0 && from_col-to_col != 0){
		return "HORIZONTAL";
	}
	else if(from_row-to_row != 0 && from_col-to_col == 0){
		return "VERTICAL";
	}
	else if(Math.abs(from_row-to_row) == Math.abs(from_col-to_col)){
		return "DIAGONAL";
	}
	else{
		return "INVALID";
	}
}

/*Switches turn of players in two-player mode*/
function switchTurn(){
	player_TURN = (player_TURN === "WHITE") ? "BLACK" : "WHITE";
}

/*Checks if a particular piece is scared or not if the next move is made*/
function checkIfPieceIsScared(piece,to_row,to_col){
	var data = pieces_afraid_of[piece];
	for(var i = 0; i < data.length; i++){
		var value = piece_locations[data[i]];
		r1 = Math.floor(value/10);
		c1 = value%10;
		if(!(to_col-c1 == 0 && to_row-r1 == 0)){
			if(Math.abs(to_row-r1) <= 1 && Math.abs(to_col-c1) <= 1){
				return true;
			}
		}	
	}
	return false;
}

/*Checks the appropriate direction to make sure a piece is not jumping over 
another piece while making a move*/
function checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)
{
	var y_dif = to_row - from_row;
	var x_dif = to_col - from_col;
	var x_inc = 0;
	var y_inc = 0;
	console.log("from_row: " + from_row + ",from_col: " + from_col + ",to_row: " + to_row + ",to_col" + to_col);
	//console.log("x_dif: " + x_dif + ", y_dif: " + y_dif);
	while(y_inc != y_dif || x_inc != x_dif){
		x_inc = (x_dif == 0) ? 0 : ((x_dif < 0) ? x_inc - 1 : x_inc + 1);
		y_inc = (y_dif == 0) ? 0 : ((y_dif < 0) ? y_inc - 1 : y_inc + 1);
//		console.log("x_inc: " + x_inc + ", y_inc: " + y_inc);
//		console.log(barca_array[from_row+y_inc][from_col+x_inc]);
		if(barca_array[from_row+y_inc][from_col+x_inc] != "."){
			//console.log("TRUE IN OBSTACLES");
			return true;
		}
	}
	console.log("FALSE IN OBSTACLES");
	return false;
}

/*Checks if a valid move exists for elephant*/
function checkIfASingleValidMoveExistsForElephant(value){
	var obstacles = [false,false,false,false,false,false,false,false];
	var move_adv = 0;
	var location_piece = piece_locations[value];
	var row = Math.floor(location_piece/10);
	var col = location_piece%10;

	while(!obstacles[0] || !obstacles[1] || !obstacles[2] || !obstacles[3] ||
		!obstacles[4] || !obstacles[5] || !obstacles[6] || !obstacles[7])
	{
		move_adv++;
		/*Check a move in up direction*/
		if(!obstacles[0] && (row - move_adv) >= 0){
			if(barca_array[row-move_adv][col] != "." && 
				checkIfPieceIsScared(value,row-move_adv,col) == false)
			{
				return true;
			}
			obstacles[0] = (barca_array[row-move_adv][col] != ".") ? true : obstacles[0];
		}
		/*Check one move in diagonal upper right*/	
		if(!obstacles[1] && (row - move_adv) >= 0 && (col + move_adv) < 10){
			if(barca_array[row-move_adv][col+move_adv] != "." && 
				checkIfPieceIsScared(value,row-move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[1] = (barca_array[row-move_adv][col+move_adv] != ".") ? true : obstacles[1];
		}
		/*Check a move in right direction*/
		if(!obstacles[2] && (col + move_adv) < 10){
			if(barca_array[row][col+move_adv] != "." && 
				checkIfPieceIsScared(value,row,col+move_adv) == false)
			{
				return true;
			}
			obstacles[2] = (barca_array[row][col+move_adv] != ".") ? true : obstacles[2];
		}
		/*Check one move in diagonal bottom right*/
		if(!obstacles[3] && (row + move_adv) < 10 && (col + move_adv) < 10){
			if(barca_array[row+move_adv][col+move_adv] != "." && 
				checkIfPieceIsScared(value,row+move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[3] = (barca_array[row+move_adv][col+move_adv] != ".") ? true : obstacles[3];			
		}
		/*Check a move in down direction*/
		if(!obstacles[4] && (row + move_adv) < 10){
			if(barca_array[row+move_adv][col] != "." && 
				checkIfPieceIsScared(value,row+move_adv,col) == false)
			{
				return true;
			}
			obstacles[4] = (barca_array[row+move_adv][col] != ".") ? true : obstacles[4];
		}
		/*Check one move in diagonal bottom left*/
		if(!obstacles[5] && (row + move_adv) < 10 && (col - move_adv) >= 0){
			if(barca_array[row+move_adv][col-move_adv] != "." && 
				checkIfPieceIsScared(value,row+move_adv,col-move_adv) == false)
			{
				return true;
			}
			obstacles[5] = (barca_array[row+move_adv][col-move_adv] != ".") ? true : obstacles[5];			
		}
		/*Check a move in left direction*/		
		if(!obstacles[6] && (col - move_adv) >= 0){
			if(barca_array[row][col-move_adv] != "." && 
				checkIfPieceIsScared(value,row,col-move_adv) == false)
			{
				return true;
			}
			obstacles[6] = (barca_array[row][col-move_adv] != ".") ? true : obstacles[6];
		}
		/*Check one move in diagonal upper left*/
		if(!obstacles[7] && (row - move_adv) >= 0 && (col - move_adv) >= 0){
			if(barca_array[row-move_adv][col-move_adv] != "." && 
				checkIfPieceIsScared(value,row-move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[7] = (barca_array[row-move_adv][col+move_adv] != ".") ? true : obstacles[7];
		}
	}
	
	return false;
}

/*Checks if a valid move exists for lion*/
function checkIfASingleValidMoveExistsForLion(value){
	var obstacles = [false,false,false,false];
	var move_adv = 0;
	var location_piece = piece_locations[value];
	var row = Math.floor(location_piece/10);
	var col = location_piece%10;
	while(!obstacles[0] || !obstacles[1] || !obstacles[2] || !obstacles[3])
	{
		move_adv++;
		/*Check one move in diagonal upper left*/
		if(!obstacles[0] && (row - move_adv) >= 0 && (col - move_adv) >= 0){
			if(barca_array[row-move_adv][col-move_adv] != "." && 
				checkIfPieceIsScared(value,row-move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[0] = (barca_array[row-move_adv][col+move_adv] != ".") ? true : obstacles[0];
		}
		/*Check one move in diagonal upper right*/	
		if(!obstacles[1] && (row - move_adv) >= 0 && (col + move_adv) < 10){
			if(barca_array[row-move_adv][col+move_adv] != "." && 
				checkIfPieceIsScared(value,row-move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[1] = (barca_array[row-move_adv][col+move_adv] != ".") ? true : obstacles[1];
		}
		/*Check one move in diagonal bottom right*/
		if(!obstacles[2] && (row + move_adv) < 10 && (col + move_adv) < 10){
			if(barca_array[row+move_adv][col+move_adv] != "." && 
				checkIfPieceIsScared(value,row+move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[2] = (barca_array[row+move_adv][col+move_adv] != ".") ? true : obstacles[3];			
		}
		/*Check one move in diagonal bottom left*/
		if(!obstacles[3] && (row + move_adv) < 10 && (col - move_adv) >= 0){
			if(barca_array[row+move_adv][col-move_adv] != "." && 
				checkIfPieceIsScared(value,row+move_adv,col-move_adv) == false)
			{
				return true;
			}
			obstacles[3] = (barca_array[row+move_adv][col-move_adv] != ".") ? true : obstacles[2];			
		}		
	}
}

/*Checks if a valid move exists for mouse*/
function checkIfASingleValidMoveExistsForMouse(value){
	var obstacles = [false,false,false,false];
	var move_adv = 0;
	var location_piece = piece_locations[value];
	var row = Math.floor(location_piece/10);
	var col = location_piece%10;

	while(!obstacles[0] || !obstacles[1] || !obstacles[2] || !obstacles[3]) 
	{
		move_adv++;
		/*Check a move in up direction*/
		if(!obstacles[0] && (row - move_adv) >= 0){
			if(barca_array[row-move_adv][col] != "." && 
				checkIfPieceIsScared(value,row-move_adv,col) == false)
			{
				return true;
			}
			obstacles[0] = (barca_array[row-move_adv][col] != ".") ? true : obstacles[0];
		}
		/*Check a move in right direction*/
		if(!obstacles[1] && (col + move_adv) < 10){
			if(barca_array[row][col+move_adv] != "." && 
				checkIfPieceIsScared(value,row,col+move_adv) == false)
			{
				return true;
			}
			obstacles[1] = (barca_array[row][col+move_adv] != ".") ? true : obstacles[1];
		}
		/*Check a move in down direction*/
		if(!obstacles[2] && (row + move_adv) < 10){
			if(barca_array[row+move_adv][col] != "." && 
				checkIfPieceIsScared(value,row+move_adv,col) == false)
			{
				return true;
			}
			obstacles[2] = (barca_array[row+move_adv][col] != ".") ? true : obstacles[2];
		}
		/*Check a move in left direction*/		
		if(!obstacles[3] && (col - move_adv) >= 0){
			if(barca_array[row][col-move_adv] != "." && 
				checkIfPieceIsScared(value,row,col-move_adv) == false)
			{
				return true;
			}
			obstacles[3] = (barca_array[row][col-move_adv] != ".") ? true : obstacles[3];
		}
	}
	return false;
}

/*Calculates new scared pieces because of the move made*/
function calculateScaredPieces(){
	scared_pieces = new Set();
	for (var key in piece_locations){
		var piece_location_of_key = piece_locations[key];
		var r1 = Math.floor(piece_location_of_key/10);
		var c1 = piece_location_of_key%10;
		if(checkIfPieceIsScared(key,r1,c1)){
			scared_pieces.add(key);
		}
	}
}

/*Calculate new trapped pieces because of the move made and 
also remove the pieces that are trapped from the scared pieces 
list. Goal: just find one possible valid move for the piece,
if you find it, it is not trapped*/
function calculateTrappedPieces(){
	var trapped_piece_array = scared_pieces;
	for(var value in trapped_piece_array){
		var validMoveFound = false;
		if(value[1] == 'E'){
			if(checkIfASingleValidMoveExistsForElephant(value)){
				trapped_pieces.push(value);
				scared_pieces.delete(value);
			}
		}
		if(value[1] == 'L'){
			if(checkIfASingleValidMoveExistsForLion(value)){
				trapped_pieces.push(value);
				scared_pieces.delete(value);
			}
		}
		if(value[1] == 'R'){
			if(checkIfASingleValidMoveExistsForMouse(value)){
				trapped_pieces.push(value);
				scared_pieces.delete(value);
			}
		}
	}
}

function checkIfInTrappedPieces(piece){
	for(var i in trapped_pieces){
		if(i === piece){
			return true;
		}
	}
	return false;
}

/*Checks if the move made is valid or invalid*/
function verifyValidMove(from_row,from_col,to_row,to_col){
	var piece = barca_array[from_row][from_col];
	var direction = directionMovedIn(from_row,from_col,to_row,to_col);
	var side = piece[0];
	/*Checks if the piece is moved in invalid direction*/
	if(direction == "INVALID")
	{
		console.log("INVALID");
		return false;
	}
	else if(!checkIfInTrappedPieces(piece) && 
		checkIfPieceIsScared(piece,to_row,to_col))
	{
		console.log("SCARED");
		return false;
	}		
	else if(piece[1] == 'L')
	{
		if(direction !== "DIAGONAL" || 
			checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			console.log("Direction for L: "+direction);
			return false;
		}
	}
	else if(piece[1] == 'E')
	{
		if(checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			console.log("Direction for E: "+direction);
			return false;
		}
	}
	else
	{
		if((direction !== "VERTICAL" && direction !== "HORIZONTAL") ||
			checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			console.log("Direction for R: "+direction);
			return false;
		}
	}
	return true;
}

/*Verify if the piece that user is trying to move is in the list*/
function verifyValidClick(str){
	for(var i = 0; i < valid_clicks.length; i++){
		if(valid_clicks[i] == str){
			return true;
		}
	}
	return false;
}

/*Function that checks for victory*/
function checkVictory(){
	if(barca_array[4][4] != "." && barca_array[4][4][0] == barca_array[4][7][0] && 
		barca_array[4][7][0] == barca_array[7][4][0]){
		victory = true;
		who_won = (barca_array[4][4][0] == 'W') ? "WHITE" : "BLACK";
	}
	else if(barca_array[4][4] != "." && barca_array[4][4][0] == barca_array[7][4][0] && 
		barca_array[7][4][0] == barca_array[7][7][0]){
		victory = true;
		who_won = (barca_array[4][4][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "Game is over...";
		return true;
	}
	else if(barca_array[4][4] != "." && barca_array[4][4][0] == barca_array[7][7][0] && 
		barca_array[7][7][0] == barca_array[4][7][0]){
		victory = true;
		who_won = (barca_array[4][4][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "Game is over...";
		return true;
	}
	else if(barca_array[4][7] != "." && barca_array[4][7][0] == barca_array[7][4][0] && 
		barca_array[7][4][0] == barca_array[7][7][0]){
		victory = true;
		who_won = (barca_array[4][7][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "Game is over...";
		return true;
	}	
	return false;
}

/*Function that computes the pieces a certain user can move*/
function recomputeValidClicks(turn){
	valid_clicks = [];
	scared_pieces.forEach(function(value){
		if(value[0] === turn[0]){
			valid_clicks.push(piece_locations[value]);
		}
	});
	if(valid_clicks.length == 0){
		if(checkIfInTrappedPieces(turn[0]+"E1") ||
			checkIfASingleValidMoveExistsForElephant(turn[0]+"E1")){
			valid_clicks.push(piece_locations[turn[0]+"E1"]);
		}
		if(checkIfInTrappedPieces(turn[0]+"E2") || 
			checkIfASingleValidMoveExistsForElephant(turn[0]+"E2")){
			valid_clicks.push(piece_locations[turn[0]+"E2"]);		
		}
		if(checkIfInTrappedPieces(turn[0]+"L1") || 
			checkIfASingleValidMoveExistsForLion(turn[0]+"L1")){
			valid_clicks.push(piece_locations[turn[0]+"L1"]);		
		}
		if(checkIfInTrappedPieces(turn[0]+"L2") || 
			checkIfASingleValidMoveExistsForLion(turn[0]+"L2")){
			valid_clicks.push(piece_locations[turn[0]+"L2"]);		
		}
		if(checkIfInTrappedPieces(turn[0]+"R1") || 
			checkIfASingleValidMoveExistsForMouse(turn[0]+"R1")){
			valid_clicks.push(piece_locations[turn[0]+"R1"]);		
		}
		if(checkIfInTrappedPieces(turn[0]+"R2") || 
			checkIfASingleValidMoveExistsForMouse(turn[0]+"R2")){
			valid_clicks.push(piece_locations[turn[0]+"R2"]);		
		}
	}
}

/*Function that returns right image extension for the piece*/
function findImgName(side,type){
	switch(type){
		case 'E': return (side == 'W') ? "elephantW.gif" : "ElephantB.png";
		case 'L': return (side == 'W') ? "lionW.gif" : "LionB.png";
		default: return (side == 'W') ? "mouseW.gif" : "MouseB.png";		
	}
}

/*Function set image to black*/
function movePiece(side,type,row,col){
	document.getElementById("tile_"+row+","+col).innerHTML = '<img src = \''+"./images/"+findImgName(side,type)+'\'/>';								
}

function getAIMove(){
	/*Send API request*/
	/*Get the move from AI*/	
}

/*Function that detects clicks and displays interactive user messages*/
function clickMade(row,col,id,val){
	/*document.getElementById("message").innerHTML = "Click made at this value " + val + ", id: " + id;*/
	row = parseInt(row);
	col = parseInt(col);
	var num = row*10 + col;
	//console.log(num); /*For debugging purposes, click F12 and check the console*/
	//console.log("Barca piece: " + barca_array[row][col]);
	//console.log(clicks_made.length); /*For debugging purposes, click F12 and check the console*/
	if(victory){
		document.getElementById("message").innerHTML = "Game is over...";
	}
	else if(verifyValidClick(num)){
		clicks_made = [];
		clicks_made.push(num);
		document.getElementById("message").innerHTML = "Choose where you want to move the piece to or select another piece to move...";
	}
	else if(clicks_made.length == 1){
		//console.log("In clicks_made");
		var r1 = Math.floor(clicks_made[0]/10);
		var c1 = clicks_made[0]%10;
		var value = verifyValidMove(r1,c1,row,col);
		//console.log("valid move: "+value);
		
		if(value)
		{
			//console.log("Move made");
			document.getElementById("tile_"+r1+","+c1).innerHTML = "";
			movePiece(barca_array[r1][c1][0],barca_array[r1][c1][1],row,col);
			barca_array[row][col] = barca_array[r1][c1];
			barca_array[r1][c1] = ".";
			piece_locations[barca_array[row][col]] = row * 10 + col;
			clicks_made = [];		
			calculateScaredPieces();
			calculateTrappedPieces();
			for(let item of scared_pieces){
				console.log(item);
			}
		
			if(checkVictory()){
				return;			
			}
			/* IF MODE IS PLAYER V. AI*/
			else if(mode == "PLAYER V. AI"){
				getAIMove();
			}
			/* IF MODE IS PLAYER V. PLAYER */
			else{
				/*No need to do this computation for AI mode*/
				switchTurn();
				recomputeValidClicks(player_TURN);
				for(var i in valid_clicks){
					console.log("number: " + i);
				}
			}
			
			if(checkVictory()){
				return;
			}
		}
		else{
			document.getElementById("message").innerHTML = "Invalid Move. Please select a valid move...";
		}
	}
	else{
		console.log("IN INVALID MOVE");
		document.getElementById("message").innerHTML = "Invalid Move. Please select a valid move...";
	}
}