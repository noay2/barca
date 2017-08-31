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
var mode = "PLAYER V. AI";
var singleMoveExists = {};
var fear_counter = 0;
var wateringHoleCounter = 0;
var first_to_move = "";
var AIsmove = false;
var gameStarted = false;
var resetState = {};
var draw_move_cache = {};
var difficulty = 3 ;
// var fifo_for_draw_moves = [];
var all_previous_moves = [];
var undo_moves = [];
var valid_move_set = {};
var crown_counter = 0;

//Data structure that is used to set the board back to its original point
var original_board_state = {};

var piece_type = "animals";

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
	printTurn();

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
	if(piece_type == "animals")
	{
		placeElephantLionMouseImages();
	}
	else if( piece_type == "rps"){
		placeRockPaperScissorImages();
	}
	else if(piece_type == "chess")
	{
		placeChessImages();
	}

	// document.getElementById(getDiv("BE1")).innerHTML = '<img src = "./images/BlackElephant.gif"/>';
	// document.getElementById(getDiv("BE2")).innerHTML = '<img src = "./images/BlackElephant.gif"/>';
	// document.getElementById(getDiv("WE1")).innerHTML = '<img src = "./images/elephantW.gif"/>';
	// document.getElementById(getDiv("WE2")).innerHTML = '<img src = "./images/elephantW.gif"/>';
	// document.getElementById(getDiv("BL1")).innerHTML = '<img src = "./images/BlackLion.gif"/>';
	// document.getElementById(getDiv("BR1")).innerHTML = '<img src = "./images/BlackMouse.gif"/>';
	// document.getElementById(getDiv("BR2")).innerHTML = '<img src = "./images/BlackMouse.gif"/>';
	// document.getElementById(getDiv("BL2")).innerHTML = '<img src = "./images/BlackLion.gif"/>';
	// document.getElementById(getDiv("WL1")).innerHTML = '<img src = "./images/lionW.gif"/>';
	// document.getElementById(getDiv("WR1")).innerHTML = '<img src = "./images/mouseW.gif"/>';
	// document.getElementById(getDiv("WR2")).innerHTML = '<img src = "./images/mouseW.gif"/>';
	// document.getElementById(getDiv("WL2")).innerHTML = '<img src = "./images/lionW.gif"/>';
}

function placeWateringHoles() {
	document.getElementById('tile_3,3').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_0"/>';
	document.getElementById('tile_3,6').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_1"/>';
	document.getElementById('tile_6,3').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_2"/>';
	document.getElementById('tile_6,6').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_3"/>';

	wateringHoleCounter = 4;
}

function addCurrentBoardPosition(){
	var string = "";
	var keysSorted = Object.keys(piece_locations).sort(function(a,b){return piece_locations[a]-piece_locations[b]})

	for(var keyLen = 0; keyLen < keysSorted.length; keyLen++){
		string += keysSorted[keyLen][0] + keysSorted[keyLen][1];
		if(piece_locations[keysSorted[keyLen]] < 10){
			string += '0' + piece_locations[keysSorted[keyLen]];
		}
		else{
			string += piece_locations[keysSorted[keyLen]];
		}
	}

	fifo_for_draw_moves.push(string);

	if(fifo_for_draw_moves.length === 21){
		var poppedPos = fifo_for_draw_moves.shift();
		draw_move_cache[poppedPos]--;
		if(draw_move_cache[poppedPos] <= 0){
			delete draw_move_cache[poppedPos];
		}
	}

	if(string in draw_move_cache){
		draw_move_cache[string]++;
	}
	else{
		draw_move_cache[string] = 1;
	}

}

function placeImageForWateringHolesIfEmpty(){
//'<div id= \''+title+'\' class="'+ checkForValue(i,j) + '" onclick = "clickMade(\''+i+'\',\''+j+'\',\''+title+'\',\''+barca_array[i][j]+'\')"></div>';
//'<img src = \''+"./images/"+findImgName(side,type)+'\'/>';
	if(!(document.getElementById('tile_3,3').innerHTML)){
		var id = "wateringhole_" + wateringHoleCounter;
		document.getElementById('tile_3,3').innerHTML += '<img src = \''+"./images/well.gif"+'\' id = \''+id+'\'/>';
		wateringHoleCounter++;
	}
	if(!(document.getElementById('tile_3,6').innerHTML)){
		var id = "wateringhole_" + wateringHoleCounter;
		document.getElementById('tile_3,6').innerHTML += '<img src = \''+"./images/well.gif"+'\' id = \''+id+'\'/>';
		wateringHoleCounter++;
	}
	if(!(document.getElementById('tile_6,3').innerHTML)){
		var id = "wateringhole_" + wateringHoleCounter;
		document.getElementById('tile_6,3').innerHTML += '<img src = \''+"./images/well.gif"+'\' id = \''+id+'\'/>';
		wateringHoleCounter++;
	}
	if(!(document.getElementById('tile_6,6').innerHTML)){
		var id = "wateringhole_" + wateringHoleCounter;
		document.getElementById('tile_6,6').innerHTML += '<img src = \''+"./images/well.gif"+'\' id = \''+id+'\'/>';
		wateringHoleCounter++;
	}
}

function removeImageForWateringHoles(){
	for(var i = wateringHoleCounter-1; i >= 0; i--){
		if(document.getElementById("wateringhole_"+i)){
			var element = document.getElementById("wateringhole_"+i);
			element.parentNode.removeChild(element);
		}
	}
	wateringHoleCounter = 0;
}

function initializeGame(){
	AIsmove = (player_TURN === "BLACK" && mode === "PLAYER V. AI") ? true : false;
	// console.log("INITIALIZE GAME");
	initValidClicks();
}

function initBoardPieces(){
		barca_array[0][4] = "BE1";
		barca_array[0][5] = "BE2";
		barca_array[1][3] = "BL1";
		barca_array[1][4] = "BR1";
		barca_array[1][5] = "BR2";
		barca_array[1][6] = "BL2";
		barca_array[8][3] = "WL1";
		barca_array[8][4] = "WR1";
		barca_array[8][5] = "WR2";
		barca_array[8][6] = "WL2";
		barca_array[9][4] = "WE1";
		barca_array[9][5] = "WE2";

		/*Set where pieces are located on the board*/
		piece_locations["BE1"] = 4;
		piece_locations["BE2"] = 5;
		piece_locations["BL1"] = 13;
		piece_locations["BR1"] = 14;
		piece_locations["BR2"] = 15;
		piece_locations["BL2"] = 16;
		piece_locations["WL1"] = 83;
		piece_locations["WR1"] = 84;
		piece_locations["WR2"] = 85;
		piece_locations["WL2"] = 86;
		piece_locations["WE1"] = 94;
		piece_locations["WE2"] = 95;

		// original_board_state["board"] = barca_array;
		// original_board_state["piece_locations"] = piece_locations;
}

/*Initializes the initial valid clicks on the board*/
function initValidClicks(){
	valid_clicks.push(83);
	valid_clicks.push(84);
	valid_clicks.push(85);
	valid_clicks.push(86);
	valid_clicks.push(94);
	valid_clicks.push(95);

	gameStarted = true;
	initBoardPieces();
	checkIfItIsAIsMove();
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
	checkVictory();
	if(victory){
		return;
	}
	else{
		player_TURN = (player_TURN === "WHITE") ? "BLACK" : "WHITE";
		printTurn();
	}
}

function printTurn(){
	if(mode === "PLAYER V. PLAYER" || AIsmove === false){
		document.getElementById('turnDiv').innerHTML = "<b>Current Turn: " + player_TURN +"</b>";
	}
	else if(AIsmove === true){
		var turn = (player_TURN === "WHITE") ? "BLACK" : "WHITE";
		document.getElementById('turnDiv').innerHTML = "<b>Current Turn: " +turn + " &#10070; The AI is thinking...</b>";

	}
}

/*Checks if a particular piece is scared or not if the next move is made*/
function checkIfPieceIsScared(piece,to_row,to_col){
	var data = pieces_afraid_of[piece];
	for(var i = 0; i < data.length; i++){
		var key = data[i];
		var r1 = getRow(key);
		var c1 = getCol(key);
		if(!(to_col-c1 === 0 && to_row-r1 === 0)){
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
	while(y_inc != y_dif || x_inc != x_dif){
		x_inc = (x_dif == 0) ? 0 : ((x_dif < 0) ? x_inc - 1 : x_inc + 1);
		y_inc = (y_dif == 0) ? 0 : ((y_dif < 0) ? y_inc - 1 : y_inc + 1);
		if(barca_array[from_row+y_inc][from_col+x_inc] != "."){
			return true;
		}
	}
	return false;
}

function getRow(piece){
	return Math.floor(piece_locations[piece]/10);
}

function getCol(piece){
	return piece_locations[piece]%10;
}

/*Checks if a piece has a single valid move if so sets that to true*/
function setIfSingleMoveExists(value,row,col){
	if(barca_array[row][col] === "."){
		singleMoveExists[value] = true;
	}
}

/* Returns the increment in the direction*/
function getIncrementOfDirection(move_adv,direction){
	switch(direction){
		case "UP":
			return [-move_adv,0];
		case "UR":
			return [-move_adv,move_adv];
		case "R":
			return [0,move_adv];
		case "BR":
			return [move_adv,move_adv];
		case "D":
			return [move_adv,0];
		case "BL":
			return [move_adv,-move_adv];
		case "L":
			return [0,-move_adv];
		case "UL":
			return [-move_adv,-move_adv];
	}
}

/* Returns a boolean indicating whether it is out of bounds*/
function checkIfOutOfBounds(row,col){
	return !((row >= 0 && row < 10) && (col >= 0 && col < 10));
}

/*Checks if a valid move exists for elephant*/
function checkIfASingleValidMoveExistsForElephant(value){
	var obstacles = [false,false,false,false,false,false,false,false];
	var directions = ["UP","UR","R","BR","D","BL","L","UL"];
	var move_adv = 0;
	var row = getRow(value);
	var col = getCol(value);
	singleMoveExists[value] = false;

	while(!(obstacles[0] && obstacles[1] && obstacles[2] && obstacles[3] &&
		obstacles[4] && obstacles[5] && obstacles[6] && obstacles[7]))
	{
		move_adv++;

		for(var i = 0; i < obstacles.length; i++){
			if(!obstacles[i]){
				var increment = getIncrementOfDirection(move_adv,directions[i]);
				obstacles[i] = checkIfOutOfBounds(row+increment[0],col+increment[1]);
			}
		}

		for(var i = 0; i < obstacles.length; i++){
			if(!obstacles[i]){
				var increment = getIncrementOfDirection(move_adv,directions[i]);
				setIfSingleMoveExists(value,row+increment[0],col+increment[1]);
				if(barca_array[row+increment[0]][col+increment[1]] === "." &&
					checkIfPieceIsScared(value,row+increment[0],col+increment[1]) === false){
						return true;
				}
				obstacles[i] = (barca_array[row+increment[0]][col+increment[1]] != ".") ? true : obstacles[i];
			}
		}
	}

	return false;
}

/*Checks if a valid move exists for lion*/
function checkIfASingleValidMoveExistsForLion(value){
	var obstacles = [false,false,false,false];
	var directions = ["UL","UR","BR","BL"];
	var move_adv = 0;
	var row = getRow(value);
	var col = getCol(value);
	singleMoveExists[value] = false;

	while(!(obstacles[0] && obstacles[1] && obstacles[2] && obstacles[3]))
	{
		move_adv++;

		for(var i = 0; i < obstacles.length; i++){
			if(!obstacles[i]){
				var increment = getIncrementOfDirection(move_adv,directions[i]);
				obstacles[i] = checkIfOutOfBounds(row+increment[0],col+increment[1]);
			}
		}

		for(var i = 0; i < obstacles.length; i++){
			if(!obstacles[i]){
				var increment = getIncrementOfDirection(move_adv,directions[i]);
				setIfSingleMoveExists(value,row+increment[0],col+increment[1]);
				if(barca_array[row+increment[0]][col+increment[1]] === "." &&
					checkIfPieceIsScared(value,row+increment[0],col+increment[1]) === false){
						return true;
				}
				obstacles[i] = (barca_array[row+increment[0]][col+increment[1]] != ".") ? true : obstacles[i];
			}
		}
	}

	return false;
}

/*Checks if a valid move exists for mouse*/
function checkIfASingleValidMoveExistsForMouse(value){
	var obstacles = [false,false,false,false];
	var directions = ["UP","R","D","L"];
	var move_adv = 0;
	var row = getRow(value);
	var col = getCol(value);
	singleMoveExists[value] = false;

	while(!(obstacles[0] && obstacles[1] && obstacles[2] && obstacles[3]))
	{
		move_adv++;

		for(var i = 0; i < obstacles.length; i++){
			if(!obstacles[i]){
				var increment = getIncrementOfDirection(move_adv,directions[i]);
				obstacles[i] = checkIfOutOfBounds(row+increment[0],col+increment[1]);
			}
		}

		for(var i = 0; i < obstacles.length; i++){
			if(!obstacles[i]){
				var increment = getIncrementOfDirection(move_adv,directions[i]);
				setIfSingleMoveExists(value,row+increment[0],col+increment[1]);
				if(barca_array[row+increment[0]][col+increment[1]] === "." &&
					checkIfPieceIsScared(value,row+increment[0],col+increment[1]) == false){
						return true;
				}
				obstacles[i] = (barca_array[row+increment[0]][col+increment[1]] != ".") ? true : obstacles[i];
			}
		}
	}

	return false;
}

// function computeAllValidMovesForMouse(value){
// 	var obstacles = [false,false,false,false];
// 	var directions = ["UP","R","D","L"];
// 	var move_adv = 0;
// 	var row = getRow(value);
// 	var col = getCol(value);
// 	singleMoveExists[value] = false;
//
// 	while(obstacles[0] || obstacles[1] || obstacles[2] || obstacles[3])
// 	{
// 		move_adv++;
//
// 		for(var i = 0; i < obstacles.length; i++){
// 			if(!obstacles[i]){
// 				var increment = getIncrementOfDirection(move_adv,directions[i]);
// 				obstacles[i] = checkIfOutOfBounds(row+increment[0],col+increment[1]);
// 			}
// 		}
//
// 		for(var i = 0; i < obstacles.length; i++){
// 			if(!obstacles[i]){
// 				var increment = getIncrementOfDirection(move_adv,directions[i]);
// 				setIfSingleMoveExists(value,row+increment[0],col+increment[1]);
// 				if(barca_array[row+increment[0]][col+increment[1]] === "." &&
// 					checkIfPieceIsScared(value,row+increment[0],col+increment[1]) == false){
// 						return true;
// 				}
// 				obstacles[i] = (barca_array[row+increment[0]][col+increment[1]] != ".") ? true : obstacles[i];
// 			}
// 		}
// 	}
//
// 	return false;
// }
//
// function computeAllValidMovesForLion(value){
// 	var obstacles = [false,false,false,false];
// 	var directions = ["UL","UR","BR","BL"];
// 	var move_adv = 0;
// 	var row = getRow(value);
// 	var col = getCol(value);
// 	singleMoveExists[value] = false;
//
// 	while(obstacles[0] && obstacles[1] && obstacles[2] && obstacles[3])
// 	{
// 		move_adv++;
//
// 		for(var i = 0; i < obstacles.length; i++){
// 			if(!obstacles[i]){
// 				var increment = getIncrementOfDirection(move_adv,directions[i]);
// 				obstacles[i] = checkIfOutOfBounds(row+increment[0],col+increment[1]);
// 			}
// 		}
//
// 		for(var i = 0; i < obstacles.length; i++){
// 			if(!obstacles[i]){
// 				var increment = getIncrementOfDirection(move_adv,directions[i]);
// 				setIfSingleMoveExists(value,row+increment[0],col+increment[1]);
// 				if(barca_array[row+increment[0]][col+increment[1]] === "." &&
// 					checkIfPieceIsScared(value,row+increment[0],col+increment[1]) === false){
// 						return true;
// 				}
// 				obstacles[i] = (barca_array[row+increment[0]][col+increment[1]] != ".") ? true : obstacles[i];
// 			}
// 		}
// 	}
//
// 	return false;
// }
//
// function computeAllValidMovesForElephant(value){
// 	var obstacles = [false,false,false,false,false,false,false,false];
// 	var directions = ["UP","UR","R","BR","D","BL","L","UL"];
// 	var move_adv = 0;
// 	var row = getRow(value);
// 	var col = getCol(value);
// 	singleMoveExists[value] = false;
//
// 	while(obstacles[0] || obstacles[1] || obstacles[2] || obstacles[3] ||
// 		obstacles[4] || obstacles[5] || obstacles[6] || obstacles[7])
// 	{
// 		move_adv++;
//
// 		for(var i = 0; i < obstacles.length; i++){
// 			if(!obstacles[i]){
// 				var increment = getIncrementOfDirection(move_adv,directions[i]);
// 				obstacles[i] = checkIfOutOfBounds(row+increment[0],col+increment[1]);
// 			}
// 		}
//
// 		for(var i = 0; i < obstacles.length; i++){
// 			if(!obstacles[i]){
// 				var increment = getIncrementOfDirection(move_adv,directions[i]);
// 				setIfSingleMoveExists(value,row+increment[0],col+increment[1]);
// 				if(barca_array[row+increment[0]][col+increment[1]] === "." &&
// 					checkIfPieceIsScared(value,row+increment[0],col+increment[1]) === false){
// 						return true;
// 				}
// 				obstacles[i] = (barca_array[row+increment[0]][col+increment[1]] != ".") ? true : obstacles[i];
// 			}
// 		}
// 	}
//
// 	return false;
// }

/*Calculates new scared pieces because of the move made*/
function calculateScaredPieces(){
	scared_pieces = new Set();
	for (var key in piece_locations){
		var r1 = getRow(key);
		var c1 = getCol(key);
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
	trapped_pieces = [];
	for(let item of trapped_piece_array){
		if(item[1] == 'E'){
			if(!checkIfASingleValidMoveExistsForElephant(item)){
				trapped_pieces.push(item);
				scared_pieces.delete(item);
			}
		}
		if(item[1] == 'L'){
			if(!checkIfASingleValidMoveExistsForLion(item)){
				trapped_pieces.push(item);
				scared_pieces.delete(item);
			}
		}
		if(item[1] == 'R'){
			if(!checkIfASingleValidMoveExistsForMouse(item)){
				trapped_pieces.push(item);
				scared_pieces.delete(item);
			}
		}
	}
}

function checkIfInScaredPieces(piece){
	for(let item of scared_pieces){
		if(piece === item){
			return true;
		}
	}
	return false;
}

function checkIfInTrappedPieces(piece){
	for(var i = 0; i < trapped_pieces.length; i++){
		if(trapped_pieces[i] === piece){
			return true;
		}
	}
	return false;
}

function placeImageForScaredAndTrappedPieces(){
	//'<div id= \''+title+'\' class="'+ checkForValue(i,j) + '" onclick = "clickMade(\''+i+'\',\''+j+'\',\''+title+'\',\''+barca_array[i][j]+'\')"></div>';
	//'<img src = \''+"./images/"+findImgName(side,type)+'\'/>';
	//'<img src = \''+"./images/well.gif"+'\' id = \''+id+'\'/>';
	// console.log("BEFORE PUTTING: " + fear_counter);
	// console.log("TRAPPED PIECES: " + trapped_pieces.length);
	// console.log("SCARED PIECES: " + scared_pieces.size);
	for(var i = 0; i < trapped_pieces.length; i++){
		var id = "fear_"+fear_counter;
		document.getElementById(getDiv(trapped_pieces[i])).innerHTML += '<img src = \''+"./images/cross.gif"+'\' id = \''+id+'\'/>';
		fear_counter++;
	}
	for(let i of scared_pieces){
		console.log(i);
		var id = "fear_"+fear_counter;
		document.getElementById(getDiv(i)).innerHTML += '<img src = \''+"./images/cross.gif"+'\' id = \''+id+'\'/>';
		fear_counter++;
	}
	// console.log("AFTER PUTTING: " + fear_counter);
}

function removeImageForScaredAndTrappedPieces(){
//	console.log(fear_counter);
	for(var i = fear_counter-1; i >= 0; i--){
		if(document.getElementById("fear_"+i)){
			var element = document.getElementById("fear_"+i);
			element.parentNode.removeChild(element);
		}
	}
	fear_counter = 0;
}

/*Checks if the move made is valid or invalid*/
function verifyValidMove(from_row,from_col,to_row,to_col){
	// console.log("Before verifying: ");
	// console.log(barca_array);
	var piece = barca_array[from_row][from_col];
	var direction = directionMovedIn(from_row,from_col,to_row,to_col);
	var side = piece[0];
	/*Checks if the piece is moved in invalid direction*/
	if(direction == "INVALID")
	{
		// console.log("After verifying: ");
		// console.log(barca_array);
		return false;
	}
	else if(!checkIfInTrappedPieces(piece) &&
		checkIfPieceIsScared(piece,to_row,to_col))
	{
		// console.log("After verifying: ");
		// console.log(barca_array);
		return false;
	}
	else if(piece[1] == 'L')
	{
		if(direction !== "DIAGONAL" ||
			checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			// console.log("After verifying: ");
			// console.log(barca_array);
			return false;
		}
	}
	else if(piece[1] == 'E')
	{
		if(checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			// console.log("After verifying: ");
			// console.log(barca_array);
			return false;
		}
	}
	else
	{
		if((direction !== "VERTICAL" && direction !== "HORIZONTAL") ||
			checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			// console.log("After verifying: ");
			// console.log(barca_array);
			return false;
		}
	}
	// console.log("After verifying: ");
	// console.log(barca_array);
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

function clearBarcaBoard(){
	for(var i = 0; i < 10; i++){
		for(var j = 0; j < 10; j++){
			barca_array[i][j] = ".";
		}
	}
}

/*Function that checks for victory*/
function checkVictory(){
	if(barca_array[3][3] != "." && barca_array[3][3][0] == barca_array[3][6][0] &&
		barca_array[3][6][0] == barca_array[6][6][0]){
		victory = true;
		who_won = (barca_array[3][3][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "<b>Game is over..." + who_won + " won! Click on start game to start another game or reset to reset game back to its original state!</b>";
		placeCrownOnWinningPieces();
	}
	else if(barca_array[3][3] != "." && barca_array[3][3][0] == barca_array[6][3][0] &&
		barca_array[6][3][0] == barca_array[6][6][0]){
		victory = true;
		who_won = (barca_array[3][3][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "<b>Game is over..." + who_won + " won! Click on start game to start another game or reset to reset game back to its original state!</b>";
		placeCrownOnWinningPieces();
	}
	else if(barca_array[3][3] != "." && barca_array[3][3][0] == barca_array[6][3][0] &&
		barca_array[6][3][0] == barca_array[3][6][0]){
		victory = true;
		who_won = (barca_array[3][3][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "<b>Game is over..." + who_won + " won! Click on start game to start another game or reset to reset game back to its original state!</b>";
		placeCrownOnWinningPieces();
	}
	else if(barca_array[3][6] != "." && barca_array[3][6][0] == barca_array[6][3][0] &&
		barca_array[6][3][0] == barca_array[6][6][0]){
		victory = true;
		who_won = (barca_array[3][6][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "<b>Game is over..." + who_won + " won! Click on start game to start another game or reset to reset game back to its original state!</b>";
		placeCrownOnWinningPieces();
	}
}

function removeCrowns(){
	if(crown_counter === 0){
		return;
	}
	else{
		for(var i = 0; i < crown_counter; i++){
			var value = i + 1;
			var element = document.getElementById("crown_"+value);
			element.parentNode.removeChild(element);
		}
		crown_counter = 0;
	}
}

function placeCrownOnWinningPieces() {
	if(who_won === "BLACK"){
			document.getElementById(getDiv("BE1")).innerHTML += '<img src = "./images/crown.gif" id = "crown_1"/>';
			document.getElementById(getDiv("BE2")).innerHTML += '<img src = "./images/crown.gif" id = "crown_2"/>';
			document.getElementById(getDiv("BL1")).innerHTML += '<img src = "./images/crown.gif" id = "crown_3"/>';
			document.getElementById(getDiv("BL2")).innerHTML += '<img src = "./images/crown.gif" id = "crown_4"/>';
			document.getElementById(getDiv("BR1")).innerHTML += '<img src = "./images/crown.gif" id = "crown_5"/>';
			document.getElementById(getDiv("BR2")).innerHTML += '<img src = "./images/crown.gif" id = "crown_6"/>';
	}
	else if(who_won === "WHITE"){
			document.getElementById(getDiv("WE1")).innerHTML += '<img src = "./images/crown.gif" id = "crown_1"/>';
			document.getElementById(getDiv("WE2")).innerHTML += '<img src = "./images/crown.gif" id = "crown_2"/>';
			document.getElementById(getDiv("WL1")).innerHTML += '<img src = "./images/crown.gif" id = "crown_3"/>';
			document.getElementById(getDiv("WL2")).innerHTML += '<img src = "./images/crown.gif" id = "crown_4"/>';
			document.getElementById(getDiv("WR1")).innerHTML += '<img src = "./images/crown.gif" id = "crown_5"/>';
			document.getElementById(getDiv("WR2")).innerHTML += '<img src = "./images/crown.gif" id = "crown_6"/>';
	}

	crown_counter = 6;
}

function recomputePositions(pieces,piece_info,src,dest){
	var color = (piece_info[0] === 'B') ? "BLACK" : "WHITE";
	var piece = (piece_info[1] === 'E') ? "ELEPHANT" : (piece_info[1] === 'R') ? "MOUSE" : "LION";
	all_previous_moves.push([color,piece,src[0],src[1],dest[0],dest[1]]);
	// original_board_state["all_previous_moves"].push([color,piece,src[0],src[1],dest[0],dest[1]]);
	barca_array[dest[0]][dest[1]] = barca_array[src[0]][src[1]];
	barca_array[src[0]][src[1]] = ".";
	piece_locations[barca_array[dest[0]][dest[1]]] = dest[0] * 10 + dest[1];
	// original_board_state["board"][dest[0]][dest[1]] = barca_array[dest[0]][dest[1]];
	// original_board_state["board"][src[0]][src[1]] = ".";
	// var piece_val = original_board_state["board"][dest[0]][dest[1]];
	// original_board_state["piece_locations"][piece_val] = dest[0] * 10 + dest[1];
	scared_pieces = new Set();
	trapped_pieces = [];

	for(var i = 0; i < pieces.length; i++){
		if(pieces[i][5]){
			trapped_pieces.push(barca_array[pieces[i][2]][pieces[i][3]]);
		}
		else if(pieces[i][4]){
			scared_pieces.add(barca_array[pieces[i][2]][pieces[i][3]]);
		}
	}

	for(var i = 0; i < trapped_pieces.length; i++){
		if(trapped_pieces[i][0] === player_TURN[0]){
			if(trapped_pieces[i][1] === 'L'){
				checkIfASingleValidMoveExistsForLion(trapped_pieces[i]);
			}
			else if(trapped_pieces[i][1] === 'R'){
				checkIfASingleValidMoveExistsForMouse(trapped_pieces[i]);
			}
			else{
				checkIfASingleValidMoveExistsForElephant(trapped_pieces[i]);
			}
		}
	}
}

/*Fix bugs with this function for TOMORROW*/
function resetBoardScaredAndTrappedPieces(data){
	var pieces = data["pieces"];
	var length = data["draw_moves"].length;
	var ai_move = data["draw_moves"][length-1];

	var src = [ai_move[2],ai_move[3]];
	var dest = [ai_move[4],ai_move[5]];
	var piece_info = barca_array[src[0]][src[1]];
	document.getElementById(getDiv(piece_info)).innerHTML = "";
	recomputePositions(pieces,piece_info,src,dest);
	movePiece(piece_info[0],piece_info[1],dest[0],dest[1]);
}

function determinePieceLocation(value){
	if(first_to_move === "BLACK" || (mode === "PLAYER V. AI" && player_TURN === "BLACK")){
		return 99-piece_locations[value];
	}
	else{
		return piece_locations[value];
	}
}


/*Function that computes the pieces a certain user can move*/
function recomputeValidClicks(turn){
	valid_clicks = [];
	scared_pieces.forEach(function(value){
		if(value[0] === turn[0]){
			valid_clicks.push(determinePieceLocation(value));
		}
	});

	if(valid_clicks.length == 0){
			if((checkIfInTrappedPieces(turn[0]+"E1") && singleMoveExists[turn[0]+"E1"]) ||
				checkIfASingleValidMoveExistsForElephant(turn[0]+"E1")){
				valid_clicks.push(determinePieceLocation(turn[0]+"E1"));
		 	}
			if((checkIfInTrappedPieces(turn[0]+"E2") && singleMoveExists[turn[0]+"E2"]) ||
				checkIfASingleValidMoveExistsForElephant(turn[0]+"E2")){
				valid_clicks.push(determinePieceLocation(turn[0]+"E2"));
		 	}
			if((checkIfInTrappedPieces(turn[0]+"L1") && singleMoveExists[turn[0]+"L1"]) ||
				checkIfASingleValidMoveExistsForLion(turn[0]+"L1")){
				valid_clicks.push(determinePieceLocation(turn[0]+"L1"));
		 	}
			if((checkIfInTrappedPieces(turn[0]+"L2") && singleMoveExists[turn[0]+"L2"]) ||
				checkIfASingleValidMoveExistsForLion(turn[0]+"L2")){
				valid_clicks.push(determinePieceLocation(turn[0]+"L2"));
		 	}
			if((checkIfInTrappedPieces(turn[0]+"R1") && singleMoveExists[turn[0]+"R1"]) ||
				checkIfASingleValidMoveExistsForMouse(turn[0]+"R1")){
				valid_clicks.push(determinePieceLocation(turn[0]+"R1"));
		 	}
			if((checkIfInTrappedPieces(turn[0]+"R2") && singleMoveExists[turn[0]+"R2"]) ||
				checkIfASingleValidMoveExistsForMouse(turn[0]+"R2")){
				valid_clicks.push(determinePieceLocation(turn[0]+"R2"));
		 	}
	}
}

/*Function that returns right image extension for the piece*/
// function findImgName(side,type){
// 	switch(type){
// 		case 'E': return (side == 'W') ? "elephantW.gif" : "BlackElephant.gif";
// 		case 'L': return (side == 'W') ? "lionW.gif" : "BlackLion.gif";
// 		default: return (side == 'W') ? "mouseW.gif" : "BlackMouse.gif";
// 	}
// }

function findImgName(side,type){
	switch(type){
		case 'E':
		{
			if(piece_type == "animals"){
				return (side == 'W') ? "elephantW.gif" : "BlackElephant.gif";
			}
			else if(piece_type == "rps"){
				return (side == 'W') ? "WhiteRock.gif" : "BlackRock.gif";
			}
			else if(piece_type == "chess"){
				return (side == 'W') ? "ChessElephantWhite.gif" : "ChessBlackElephant.gif";
			}
		}
		case 'L':
		{
			if(piece_type == "animals"){
				return (side == 'W') ? "lionW.gif" : "BlackLion.gif";
			}
			else if(piece_type == "rps"){
				return (side == 'W') ? "WhiteScissor.gif" : "BlackScissor.gif";
			}

			else if(piece_type == "chess"){
				return (side == 'W') ? "ChessWhiteKing.gif" : "ChessBlackKing.gif";
			}
		}
		default:
		{
			if(piece_type == "animals"){
				return (side == 'W') ? "mouseW.gif" : "BlackMouse.gif";
			}
			else if(piece_type == "rps"){
				return (side == 'W') ? "WhitePaper.gif" : "BlackPaper.gif";
			}

			else if(piece_type == "chess"){
				return (side == 'W') ? "ChessWhitePawn.gif" : "ChessBlackPawn.gif";
			}
		}
	}
}




/*Function set image to black*/
function movePiece(side,type,row,col){
	document.getElementById(getDiv(barca_array[row][col])).innerHTML = '<img src = \''+"./images/"+findImgName(side,type)+'\'/>';
}

/*Function that gets the move made by the AI and updates the board accordingly*/
function getAIMove(move){
	// console.log("IN GET AI MOVE");
	if(!gameStarted){
		// console.log("IN RETURN BYE BYE");
		return;
	}
	var API_request = {};

	checkVictory();
	if(victory){
		return;
	}
	API_request["whitetomove"] = (player_TURN === "WHITE") ? false : true;
	API_request["draw_moves"] = all_previous_moves;
	pieces = [];

	for(var piece in piece_locations){
		var info = [[null,null,null,null,null,null]];
		info[0][0] = (piece[0] == 'B') ? "BLACK" : "WHITE";
		info[0][1] = (piece[1] == 'E') ? "ELEPHANT" : (piece[1] == 'L') ? "LION" : "MOUSE";
		info[0][2] = getRow(piece);
		info[0][3] = getCol(piece);
		info[0][4] = checkIfInScaredPieces(piece);
		info[0][5] = checkIfInTrappedPieces(piece);
		pieces = pieces.concat(info);
	}
	// API_request["human_move"] = [[0,0],[0,5]];
	API_request["pieces"] = pieces;
	API_request["difficulty"] = difficulty;

	// if(move.length !== 0){
	// 	var piece = barca_array[move[2]][move[3]];
	// 	var color = (piece[0] === 'B') ? "BLACK" : "WHITE";
	// 	var type = (piece[1] === 'E') ? "ELEPHANT" : (piece[1] === 'L') ? "LION" : "MOUSE";
	// 	if(player_TURN === "BLACK"){
	// 		API_request["draw_moves"].push([color,type,9-move[0],9-move[1],9-move[2],9-move[3]]);
	// 	}
	// 	else{
	// 		API_request["draw_moves"].push([color,type,move[0],move[1],move[2],move[3]]);
	// 	}
	// 	console.log(API_request);
	// }

	// console.log("GOT TO REQUEST");
	$.ajax({
			type: "POST",
			url: "https://serene-everglades-79780.herokuapp.com/version4",
			data: JSON.stringify(API_request),
			dataType: "json",
			contentType: 'application/json',
			success: function(data){
				// document.getElementById("message").innerHTML = "<b>AI is done making its move... now it is your turn...</b>";
				document.getElementById("message").innerHTML = "<b>AI is done making its move... now it is your turn...</b>";
				removeImageForScaredAndTrappedPieces();
				removeImageForWateringHoles();
				resetBoardScaredAndTrappedPieces(data);
				checkVictory();
				// addCurrentBoardPosition();
				recomputeValidClicks(player_TURN);
				placeImageForScaredAndTrappedPieces();
				placeImageForWateringHolesIfEmpty();
				// console.log("Move made");
				AIsmove = false;
				printTurn();
				enableAllButtons();
			},
			error: function(data){
				console.log(API_request);
				alert(data);
				enableAllButtons();
			}
		});
}

/*Function that prints the board position to the backend upon a button click from user*/
function printBoardPosition(){
	if(!gameStarted){
		return;
	}
	var API_request = {};

	API_request["whitetomove"] = (player_TURN === "WHITE") ? false : true;
	pieces = [];

	for(var piece in piece_locations){
		var info = [[null,null,null,null,null,null]];
		info[0][0] = (piece[0] == 'B') ? "BLACK" : "WHITE";
		info[0][1] = (piece[1] == 'E') ? "ELEPHANT" : (piece[1] == 'L') ? "LION" : "MOUSE";
		info[0][2] = getRow(piece);
		info[0][3] = getCol(piece);
		info[0][4] = checkIfInScaredPieces(piece);
		info[0][5] = checkIfInTrappedPieces(piece);
		pieces = pieces.concat(info);
	}
	API_request["pieces"] = pieces;

	$.ajax({
			type: "PUT",
			url: "https://serene-everglades-79780.herokuapp.com/print-board",
			data: JSON.stringify(API_request),
			dataType: "json",
			contentType: 'application/json',
			success: function(data){
			},
			error: function(data){
				alert(data);
			}
		});
}

/*Function that detects clicks and displays interactive user messages*/
function clickMade(row,col,id,val){
	row = parseInt(row);
	col = parseInt(col);
	var num = row*10 + col;

	if(undo_moves.length > 0){
		return;
	}

	if(!gameStarted){
		return;
	}
	if(AIsmove){
		document.getElementById("message").innerHTML = "<b>Invalid move... It is AI's turn to move. Please wait until it is done making its move...</b>";
		return;
	}

	if(victory){
		document.getElementById("message").innerHTML = "<b>Game is over..." + who_won + " won! Click on start game to start another game or reset to reset game back to its original state!</b>";
	}
	else if(verifyValidClick(num)){
		clicks_made = [];
		clicks_made.push(num);
		document.getElementById("message").innerHTML = "<b>Choose where you want to move the piece to or select another piece to move...</b>";
	}
	else if(clicks_made.length == 1){
		var r1 = Math.floor(clicks_made[0]/10);
		var c1 = clicks_made[0]%10;

		r1 = (first_to_move === "BLACK") ? (9 - r1) : r1;
		c1 = (first_to_move === "BLACK") ? (9 - c1) : c1;
		row = (first_to_move === "BLACK") ? (9 - row) : row;
		col = (first_to_move === "BLACK") ? (9 - col) : col;

		disableAllButtons();

		if(verifyValidMove(r1,c1,row,col))
		{
			disableAllButtons();

			AIsmove = (mode === "PLAYER V. AI") ? true : false;
			printTurn();
			makeMove(r1,c1,row,col,false);
			console.log("r1,c1;row,col: "+ r1+","+c1+";"+row+","+col);

			if(mode === "PLAYER V. PLAYER"){
				var turn = (player_TURN === "WHITE") ? "BLACK" : "WHITE";
				document.getElementById("message").innerHTML = "<b> " + player_TURN + " has made the move.. Now it is " + turn + "'s move...</b>";
			}

			if(victory){
				enableAllButtons();
				return;
			}
			/* IF MODE IS PLAYER V. AI*/
			else if(mode === "PLAYER V. AI"){
				document.getElementById("message").innerHTML = "<b>You have made your move.. Now it is AI's turn</b>";
				getAIMove([r1,c1,row,col]);
				if(victory){
					return;
				}
			}
			/* IF MODE IS PLAYER V. PLAYER */
			else{
				switchTurn();
				recomputeValidClicks(player_TURN);
				enableAllButtons();
			}
		}
		else{
			enableAllButtons();
			document.getElementById("message").innerHTML = "<b>Invalid Move. Please select a valid move for the piece you selected...</b>";
		}
	}
	else{
		document.getElementById("message").innerHTML = "<b>Invalid Move. The piece you selected is not allowed to move or has no valid moves...</b>";
	}
}

function disableAllButtons(){
	document.getElementById("playFromHere").disabled = true;
	document.getElementById("undoMove").disabled = true;
	document.getElementById("redoMove").disabled = true;
	// document.getElementById("setToOriginal").disabled = true;
	document.getElementById("startGame").disabled = true;
	document.getElementById("resetGame").disabled = true;
}

function enableAllButtons(){
	document.getElementById("playFromHere").disabled = false;
	document.getElementById("undoMove").disabled = false;
	document.getElementById("redoMove").disabled = false;
	// document.getElementById("setToOriginal").disabled = false;
	document.getElementById("startGame").disabled = false;
	document.getElementById("resetGame").disabled = false;
}

/*Initially does the move checking if it is AIs turn*/
function checkIfItIsAIsMove(){
	if(AIsmove){
			disableAllButtons();
			printTurn();
			getAIMove([]);
	}
}

function makeMove(r1,c1,row,col,undo){
	removeImageForScaredAndTrappedPieces();
	removeImageForWateringHoles();
	removeCrowns();
	document.getElementById(getDiv(barca_array[r1][c1])).innerHTML = "";
	barca_array[row][col] = barca_array[r1][c1];
	barca_array[r1][c1] = ".";
	piece_locations[barca_array[row][col]] = row * 10 + col;
	// original_board_state["board"][row][col] = barca_array[row][col];
	// original_board_state["board"][r1][c1] = ".";
	// original_board_state["piece_locations"][barca_array[row][col]] = row * 10 + col;
	movePiece(barca_array[row][col][0],barca_array[row][col][1],row,col);
	clicks_made = [];
	singleMoveExists = {};
	checkVictory();
	// addCurrentBoardPosition();
	var color = (barca_array[row][col][0] === 'B') ? "BLACK" : "WHITE";
	var piece = (barca_array[row][col][1] === 'E') ? "ELEPHANT" : (barca_array[row][col][1] === 'R') ? "MOUSE" : "LION";
	if(!undo){
		all_previous_moves.push([color,piece,r1,c1,row,col]);
		// original_board_state["all_previous_moves"].push([color,piece,r1,c1,row,col]);
	}
	calculateScaredPieces();
	calculateTrappedPieces();
	placeImageForScaredAndTrappedPieces();
	placeImageForWateringHolesIfEmpty();
}



/* Returns the div of the piece*/
function getDiv(piece){
	var row = getRow(piece);
	var col = getCol(piece);
	if(first_to_move === "BLACK" && (player_TURN === "BLACK" && mode === "PLAYER V. AI")){
		return "tile_" + (9-row) + "," + (9-col);
	}
	else{
		return "tile_" + row + "," + col;
	}
}

function initialize(reset){
	disableAllButtons();
	document.getElementById("barca_board").innerHTML = "";
	gameStarted = false;
	victory = false;
	who_won = "";
	if(reset){
		player_TURN = resetState["player_TURN"];
		mode = resetState["mode"];
		difficulty = resetState["difficulty"];
		first_to_move = resetState["first_to_move"];
	}
	else{
		player_TURN = $("#playeroption").val();
		mode = $("#gametype").val();
		var str = $("#hardness").val();
		difficulty = parseInt(str);
		first_to_move = player_TURN;
		resetState["player_TURN"] = player_TURN;
		resetState["mode"] = mode;
		resetState["difficulty"] = difficulty;
		resetState["first_to_move"] = first_to_move;
	}
	checkPieceType();
	// original_board_state = {};
	// original_board_state["player_TURN"] = player_TURN;
	// original_board_state["mode"] = mode;
	fear_counter = 0;
	wateringHoleCounter = 0;
	crown_counter = 0;
	valid_clicks = [];
	draw_move_counter = {};
	all_previous_moves = [];
	// original_board_state["all_previous_moves"] = [];
	undo_moves = [];
	// fifo_for_draw_moves = [];
	clearBarcaBoard();
	newBoard();
	initBoardPieces();
	placeInitImage();
	placeWateringHoles();

}

function startGame(){
	if(gameStarted){
		var newgameStarted = confirm("Are you sure you want to start another game?");
		if(newgameStarted){
			initialize(false);
			initializeGame();
			enableAllButtons();
		}
	}
	else{
		initialize(false);
		initializeGame();
		enableAllButtons();
	}
}

function resetGame(){
	if(gameStarted){
		var newgameStarted = confirm("Are you sure you want to reset the game back to its original state?");
		if(newgameStarted){
			initialize(true);
			initializeGame();
			enableAllButtons();
		}
	}
}

// function setBackToOriginalState(){
// 	setToOriginalBoard = confirm("Are you sure you want to set back to original board game state");
// 	if(setToOriginalBoard){
// 		disableAllButtons();
// 		removeImageForScaredAndTrappedPieces();
// 		removeImageForWateringHoles();
// 		removeCrowns();
// 		// addCurrentBoardPosition();
// 		barca_array = original_board_state["board"];
// 		piece_locations = original_board_state["piece_locations"];
// 		all_previous_moves = original_board_state["all_previous_moves"];
// 		player_TURN = original_board_state["player_TURN"];
//
// 		mode = original_board_state["mode"];
// 		undo_moves = [];
// 		checkVictory();
// 		calculateScaredPieces();
// 		calculateTrappedPieces();
// 		placeImageForScaredAndTrappedPieces();
// 		placeImageForWateringHolesIfEmpty();
//
// 		if(mode === "PLAYER V. AI"){
// 			AIsmove = original_board_state["AIsmove"];
// 		}
//
// 		printTurn();
// 		if(!AIsmove){
// 			recomputeValidClicks(player_TURN);
// 		}
// 		enableAllButtons();
// 	}
// }

function takeBack(src_row,src_col,dest_row,dest_col,undo){
	if(undo){
		console.log("piece_src: " + src_row + "," + src_col + "," + barca_array[src_row][src_col]);
	}
	makeMove(src_row,src_col,dest_row,dest_col,undo);
	if(undo){
		console.log("piece_dest: " + dest_row + "," + dest_col + "," + barca_array[dest_row][dest_col]);
	}

	if(mode === "PLAYER V. AI"){
		AIsmove = !AIsmove;
	}
	else{
		switchTurn();
		recomputeValidClicks(player_TURN);
	}
}

function undoMove(){
	if(all_previous_moves.length > 0){
		undo_moves.push(all_previous_moves.pop());
		var move = undo_moves[undo_moves.length-1];
		var src_row = move[2];
		var src_col = move[3];
		var dest_row = move[4];
		var dest_col = move[5];
		takeBack(dest_row,dest_col,src_row,src_col,true);
	}
	else{
		alert("There is no move to undo");
	}
}

function redoMove(){
	if(undo_moves.length > 0){
		all_previous_moves.push(undo_moves.pop());
		var move = all_previous_moves[all_previous_moves.length - 1];
		var src_row = move[2];
		var src_col = move[3];
		var dest_row = move[4];
		var dest_col = move[5];
		takeBack(src_row,src_col,dest_row,dest_col,true);
	}
	else{
		alert("There is no move to redo");
	}
}

function playFromHere(){
	playNewGame = confirm("Do you want to make the move from here?");

	if(playNewGame)
	{
		// console.log(barca_array);
		undo_moves = [];
		if(mode === "PLAYER V. AI"){
			if(AIsmove){
				disableAllButtons();
				printTurn();
				getAIMove([]);
			}
		}
		recomputeValidClicks(player_TURN);
	}
}

function checkPieceType()
{
	// piece_type = $("#pieceType").val();
	// console.log(piece_type);

}

function placeRockPaperScissorImages(){
	document.getElementById(getDiv("BE1")).innerHTML = '<img src = "./images/BlackRock.gif"/>';
	document.getElementById(getDiv("BE2")).innerHTML = '<img src = "./images/BlackRock.gif"/>';
	document.getElementById(getDiv("WE1")).innerHTML = '<img src = "./images/WhiteRock.gif"/>';
	document.getElementById(getDiv("WE2")).innerHTML = '<img src = "./images/WhiteRock.gif"/>';
	document.getElementById(getDiv("BL1")).innerHTML = '<img src = "./images/BlackScissor.gif"/>';
	document.getElementById(getDiv("BR1")).innerHTML = '<img src = "./images/BlackPaper.gif"/>';
	document.getElementById(getDiv("BR2")).innerHTML = '<img src = "./images/BlackPaper.gif"/>';
	document.getElementById(getDiv("BL2")).innerHTML = '<img src = "./images/BlackScissor.gif"/>';
	document.getElementById(getDiv("WL1")).innerHTML = '<img src = "./images/WhiteScissor.gif"/>';
	document.getElementById(getDiv("WR1")).innerHTML = '<img src = "./images/WhitePaper.gif"/>';
	document.getElementById(getDiv("WR2")).innerHTML = '<img src = "./images/WhitePaper.gif"/>';
	document.getElementById(getDiv("WL2")).innerHTML = '<img src = "./images/WhiteScissor.gif"/>';

}

function placeElephantLionMouseImages(){
	document.getElementById(getDiv("BE1")).innerHTML = '<img src = "./images/BlackElephant.gif"/>';
	document.getElementById(getDiv("BE2")).innerHTML = '<img src = "./images/BlackElephant.gif"/>';
	document.getElementById(getDiv("WE1")).innerHTML = '<img src = "./images/elephantW.gif"/>';
	document.getElementById(getDiv("WE2")).innerHTML = '<img src = "./images/elephantW.gif"/>';
	document.getElementById(getDiv("BL1")).innerHTML = '<img src = "./images/BlackLion.gif"/>';
	document.getElementById(getDiv("BR1")).innerHTML = '<img src = "./images/BlackMouse.gif"/>';
	document.getElementById(getDiv("BR2")).innerHTML = '<img src = "./images/BlackMouse.gif"/>';
	document.getElementById(getDiv("BL2")).innerHTML = '<img src = "./images/BlackLion.gif"/>';
	document.getElementById(getDiv("WL1")).innerHTML = '<img src = "./images/lionW.gif"/>';
	document.getElementById(getDiv("WR1")).innerHTML = '<img src = "./images/mouseW.gif"/>';
	document.getElementById(getDiv("WR2")).innerHTML = '<img src = "./images/mouseW.gif"/>';
	document.getElementById(getDiv("WL2")).innerHTML = '<img src = "./images/lionW.gif"/>';
}


function placeChessImages(){
	document.getElementById(getDiv("BE1")).innerHTML = '<img src = "./images/ChessBlackElephant.gif"/>';
	document.getElementById(getDiv("BE2")).innerHTML = '<img src = "./images/ChessBlackElephant.gif"/>';
	document.getElementById(getDiv("WE1")).innerHTML = '<img src = "./images/ChessElephantWhite.gif"/>';
	document.getElementById(getDiv("WE2")).innerHTML = '<img src = "./images/ChessElephantWhite.gif"/>';
	document.getElementById(getDiv("BL1")).innerHTML = '<img src = "./images/ChessBlackKing.gif"/>';
	document.getElementById(getDiv("BR1")).innerHTML = '<img src = "./images/ChessBlackPawn.gif"/>';
	document.getElementById(getDiv("BR2")).innerHTML = '<img src = "./images/ChessBlackPawn.gif"/>';
	document.getElementById(getDiv("BL2")).innerHTML = '<img src = "./images/ChessBlackKing.gif"/>';
	document.getElementById(getDiv("WL1")).innerHTML = '<img src = "./images/ChessWhiteKing.gif"/>';
	document.getElementById(getDiv("WR1")).innerHTML = '<img src = "./images/ChessWhitePawn.gif"/>';
	document.getElementById(getDiv("WR2")).innerHTML = '<img src = "./images/ChessWhitePawn.gif"/>';
	document.getElementById(getDiv("WL2")).innerHTML = '<img src = "./images/ChessWhiteKing.gif"/>';
}

function changePieceTypeToAnimals(){

	if(piece_type != "animals"){

		placeElephantLionMouseImages();
		placeImageForScaredAndTrappedPieces();
		placeImageForWateringHolesIfEmpty();
		placeCrownOnWinningPieces();
		piece_type = "animals";

	}

}

function changePieceTypeToRPS(){

	if(piece_type != "rps"){

		placeRockPaperScissorImages();
		placeImageForScaredAndTrappedPieces();
		placeImageForWateringHolesIfEmpty();
		placeCrownOnWinningPieces();
		piece_type = "rps";

	}


}

function changePieceTypeToChess(){

		if(piece_type != "chess"){

		placeChessImages();
		placeImageForScaredAndTrappedPieces();
		placeImageForWateringHolesIfEmpty();
		placeCrownOnWinningPieces();
		piece_type = "chess";

	}

}
