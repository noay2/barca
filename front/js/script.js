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
var AIsmove = false;
var gameStarted = false;
var resetState = {};

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
		document.getElementById('turnDiv').innerHTML = "Player :" + player_TURN;

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
	if(player_TURN === "WHITE"){
		document.getElementById('tile_0,4').innerHTML = '<img src = "./images/BlackElephant.gif"/>';
		document.getElementById('tile_0,5').innerHTML = '<img src = "./images/BlackElephant.gif"/>';
		document.getElementById('tile_9,4').innerHTML = '<img src = "./images/elephantW.gif"/>';
		document.getElementById('tile_9,5').innerHTML = '<img src = "./images/elephantW.gif"/>';
		document.getElementById('tile_1,3').innerHTML = '<img src = "./images/BlackLion.gif"/>';
		document.getElementById('tile_1,4').innerHTML = '<img src = "./images/BlackMouse.gif"/>';
		document.getElementById('tile_1,5').innerHTML = '<img src = "./images/BlackMouse.gif"/>';
		document.getElementById('tile_1,6').innerHTML = '<img src = "./images/BlackLion.gif"/>';
		document.getElementById('tile_8,3').innerHTML = '<img src = "./images/lionW.gif"/>';
		document.getElementById('tile_8,4').innerHTML = '<img src = "./images/mouseW.gif"/>';
		document.getElementById('tile_8,5').innerHTML = '<img src = "./images/mouseW.gif"/>';
		document.getElementById('tile_8,6').innerHTML = '<img src = "./images/lionW.gif"/>';
	}
	else{
		document.getElementById('tile_0,4').innerHTML = '<img src = "./images/elephantW.gif"/>';
		document.getElementById('tile_0,5').innerHTML = '<img src = "./images/elephantW.gif"/>';
		document.getElementById('tile_9,4').innerHTML = '<img src = "./images/BlackElephant.gif"/>';
		document.getElementById('tile_9,5').innerHTML = '<img src = "./images/BlackElephant.gif"/>';
		document.getElementById('tile_1,3').innerHTML = '<img src = "./images/lionW.gif"/>';
		document.getElementById('tile_1,4').innerHTML = '<img src = "./images/mouseW.gif"/>';
		document.getElementById('tile_1,5').innerHTML = '<img src = "./images/mouseW.gif"/>';
		document.getElementById('tile_1,6').innerHTML = '<img src = "./images/lionW.gif"/>';
		document.getElementById('tile_8,3').innerHTML = '<img src = "./images/BlackLion.gif"/>';
		document.getElementById('tile_8,4').innerHTML = '<img src = "./images/BlackMouse.gif"/>';
		document.getElementById('tile_8,5').innerHTML = '<img src = "./images/BlackMouse.gif"/>';
		document.getElementById('tile_8,6').innerHTML = '<img src = "./images/BlackLion.gif"/>';
	}
}

function placeWateringHoles() {
	document.getElementById('tile_3,3').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_0"/>';
	document.getElementById('tile_3,6').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_1"/>';
	document.getElementById('tile_6,3').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_2"/>';
	document.getElementById('tile_6,6').innerHTML += '<img src = "./images/well.gif" id = "wateringhole_3"/>';

	wateringHoleCounter = 4;
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

/*Initializes the initial valid clicks on the board*/
function initValidClicks(){
		valid_clicks.push(83);
		valid_clicks.push(84);
		valid_clicks.push(85);
		valid_clicks.push(86);
		valid_clicks.push(94);
		valid_clicks.push(95);

	if(player_TURN === "BLACK"){
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
	else{
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
	}

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
	player_TURN = (player_TURN === "WHITE") ? "BLACK" : "WHITE";
	printTurn();
}

function printTurn(){
	if(mode === "PLAYER V. PLAYER" || AIsmove === false){
		document.getElementById('turnDiv').innerHTML = "TURN: " + player_TURN;
	}
	else if(AIsmove){
		var turn = (player_TURN === "WHITE") ? "BLACK" : "WHITE";
		document.getElementById('turnDiv').innerHTML = "TURN: " +turn + ". AI is thinking...";
	}
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

/*Checks if a valid move exists for elephant*/
function checkIfASingleValidMoveExistsForElephant(value){
	var obstacles = [false,false,false,false,false,false,false,false];
	var move_adv = 0;
	var location_piece = piece_locations[value];
	var row = getRow(value);
	var col = getCol(value);
	singleMoveExists[value] = false;

	while(!(obstacles[0] && obstacles[1] && obstacles[2] && obstacles[3] &&
		obstacles[4] && obstacles[5] && obstacles[6] && obstacles[7]))
	{
		move_adv++;
		/*Check a move in up direction*/
		if(!obstacles[0] && (row - move_adv) >= 0){
			setIfSingleMoveExists(value,row-move_adv,col);
			if(barca_array[row-move_adv][col] === "." &&
				checkIfPieceIsScared(value,row-move_adv,col) == false)
			{
				return true;
			}
			obstacles[0] = (barca_array[row-move_adv][col] != ".") ? true : obstacles[0];
		}
		/*Check one move in diagonal upper right*/
		if(!obstacles[1] && (row - move_adv) >= 0 && (col + move_adv) < 10){
			setIfSingleMoveExists(value,row-move_adv,col+move_adv);
			if(barca_array[row-move_adv][col+move_adv] === "." &&
				checkIfPieceIsScared(value,row-move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[1] = (barca_array[row-move_adv][col+move_adv] != ".") ? true : obstacles[1];
		}
		/*Check a move in right direction*/
		if(!obstacles[2] && (col + move_adv) < 10){
			setIfSingleMoveExists(value,row,col+move_adv);
			if(barca_array[row][col+move_adv] === "." &&
				checkIfPieceIsScared(value,row,col+move_adv) == false)
			{
				return true;
			}
			obstacles[2] = (barca_array[row][col+move_adv] != ".") ? true : obstacles[2];
		}
		/*Check one move in diagonal bottom right*/
		if(!obstacles[3] && (row + move_adv) < 10 && (col + move_adv) < 10){
			setIfSingleMoveExists(value,row+move_adv,col+move_adv);
			if(barca_array[row+move_adv][col+move_adv] === "." &&
				checkIfPieceIsScared(value,row+move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[3] = (barca_array[row+move_adv][col+move_adv] != ".") ? true : obstacles[3];
		}
		/*Check a move in down direction*/
		if(!obstacles[4] && (row + move_adv) < 10){
			setIfSingleMoveExists(value,row+move_adv,col);
			if(barca_array[row+move_adv][col] === "." &&
				checkIfPieceIsScared(value,row+move_adv,col) == false)
			{
				return true;
			}
			obstacles[4] = (barca_array[row+move_adv][col] != ".") ? true : obstacles[4];
		}
		/*Check one move in diagonal bottom left*/
		if(!obstacles[5] && (row + move_adv) < 10 && (col - move_adv) >= 0){
			setIfSingleMoveExists(value,row+move_adv,col-move_adv);
			if(barca_array[row+move_adv][col-move_adv] === "." &&
				checkIfPieceIsScared(value,row+move_adv,col-move_adv) == false)
			{
				return true;
			}
			obstacles[5] = (barca_array[row+move_adv][col-move_adv] != ".") ? true : obstacles[5];
		}
		/*Check a move in left direction*/
		if(!obstacles[6] && (col - move_adv) >= 0){
			setIfSingleMoveExists(value,row,col-move_adv);
			if(barca_array[row][col-move_adv] === "." &&
				checkIfPieceIsScared(value,row,col-move_adv) == false)
			{
				return true;
			}
			obstacles[6] = (barca_array[row][col-move_adv] != ".") ? true : obstacles[6];
		}
		/*Check one move in diagonal upper left*/
		if(!obstacles[7] && (row - move_adv) >= 0 && (col - move_adv) >= 0){
			setIfSingleMoveExists(value,row-move_adv,col-move_adv);
			if(barca_array[row-move_adv][col-move_adv] === "." &&
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
	singleMoveExists[value] = false;

//	console.log("Checking valid moves for lion");
	while(!(obstacles[0] && obstacles[1] && obstacles[2] && obstacles[3]))
	{
		move_adv++;
		/*Check one move in diagonal upper left*/
		if(!obstacles[0] && (row - move_adv) >= 0 && (col - move_adv) >= 0){
			setIfSingleMoveExists(value,row-move_adv,col-move_adv);
			if(barca_array[row-move_adv][col-move_adv] === "." &&
				checkIfPieceIsScared(value,row-move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[0] = (barca_array[row-move_adv][col+move_adv] != ".") ? true : obstacles[0];
		}
		/*Check one move in diagonal upper right*/
		if(!obstacles[1] && (row - move_adv) >= 0 && (col + move_adv) < 10){
			setIfSingleMoveExists(value,row-move_adv,col+move_adv);
			if(barca_array[row-move_adv][col+move_adv] === "." &&
				checkIfPieceIsScared(value,row-move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[1] = (barca_array[row-move_adv][col+move_adv] != ".") ? true : obstacles[1];
		}
		/*Check one move in diagonal bottom right*/
		if(!obstacles[2] && (row + move_adv) < 10 && (col + move_adv) < 10){
			setIfSingleMoveExists(value,row+move_adv,col+move_adv);
			if(barca_array[row+move_adv][col+move_adv] === "." &&
				checkIfPieceIsScared(value,row+move_adv,col+move_adv) == false)
			{
				return true;
			}
			obstacles[2] = (barca_array[row+move_adv][col+move_adv] != ".") ? true : obstacles[2];
		}
		/*Check one move in diagonal bottom left*/
		if(!obstacles[3] && (row + move_adv) < 10 && (col - move_adv) >= 0){
			setIfSingleMoveExists(value,row+move_adv,col=move_adv);
			if(barca_array[row+move_adv][col-move_adv] === "." &&
				checkIfPieceIsScared(value,row+move_adv,col-move_adv) == false)
			{
				return true;
			}
			obstacles[3] = (barca_array[row+move_adv][col-move_adv] != ".") ? true : obstacles[3];
		}
	}
	return false;
}

/*Checks if a valid move exists for mouse*/
function checkIfASingleValidMoveExistsForMouse(value){
//	console.log("Checking valid moves for mouse");
//	console.log("Checking valid moves for mouse");
	var obstacles = [false,false,false,false];
	var move_adv = 0;
	var location_piece = piece_locations[value];
	var row = Math.floor(location_piece/10);
	var col = location_piece%10;
	singleMoveExists[value] = false;

	while(!(obstacles[0] && obstacles[1] && obstacles[2] && obstacles[3]))
	{
		move_adv++;
		/*Check a move in up direction*/
		if(!obstacles[0] && (row - move_adv) >= 0){
			setIfSingleMoveExists(value,row-move_adv);
			if(barca_array[row-move_adv][col] === "." &&
				checkIfPieceIsScared(value,row-move_adv,col) == false)
			{
				return true;
			}
			obstacles[0] = (barca_array[row-move_adv][col] != ".") ? true : obstacles[0];
		}
		/*Check a move in right direction*/
		if(!obstacles[1] && (col + move_adv) < 10){
			setIfSingleMoveExists(value,row,col+move_adv);
			if(barca_array[row][col+move_adv] === "." &&
				checkIfPieceIsScared(value,row,col+move_adv) == false)
			{
				return true;
			}
			obstacles[1] = (barca_array[row][col+move_adv] != ".") ? true : obstacles[1];
		}
		/*Check a move in down direction*/
		if(!obstacles[2] && (row + move_adv) < 10){
			setIfSingleMoveExists(value,row+move_adv,col);
			if(barca_array[row+move_adv][col] === "." &&
				checkIfPieceIsScared(value,row+move_adv,col) == false)
			{
				return true;
			}
			obstacles[2] = (barca_array[row+move_adv][col] != ".") ? true : obstacles[2];
		}
		/*Check a move in left direction*/
		if(!obstacles[3] && (col - move_adv) >= 0){
			setIfSingleMoveExists(value,row,col-move_adv);
			if(barca_array[row][col-move_adv] === "." &&
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
//	console.log("Calculating scared pieces...");
	scared_pieces = new Set();
	for (var key in piece_locations){
		var piece_location_of_key = piece_locations[key];
		var r1 = Math.floor(piece_location_of_key/10);
		var c1 = piece_location_of_key%10;
		if(checkIfPieceIsScared(key,r1,c1)){
			scared_pieces.add(key);
		}
	}
	//console.log(scared_pieces.size);
}

/*Calculate new trapped pieces because of the move made and
also remove the pieces that are trapped from the scared pieces
list. Goal: just find one possible valid move for the piece,
if you find it, it is not trapped*/
function calculateTrappedPieces(){
//	console.log("Calculating trapped pieces...");
//	console.log("Calculating trapped pieces...");
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
	for(var i = 0; i < trapped_pieces.length; i++){
		var id = "fear_"+fear_counter;
		document.getElementById(getDiv(trapped_pieces[i])).innerHTML += '<img src = \''+"./images/cross.gif"+'\' id = \''+id+'\'/>';
		fear_counter++;
	}
	for(let i of scared_pieces){
		var id = "fear_"+fear_counter;
		document.getElementById(getDiv(i)).innerHTML += '<img src = \''+"./images/cross.gif"+'\' id = \''+id+'\'/>';
		fear_counter++;
	}
}

function removeImageForScaredAndTrappedPieces(){
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
	var piece = barca_array[from_row][from_col];
	var direction = directionMovedIn(from_row,from_col,to_row,to_col);
	var side = piece[0];
	/*Checks if the piece is moved in invalid direction*/
	if(direction == "INVALID")
	{
		return false;
	}
	else if(!checkIfInTrappedPieces(piece) &&
		checkIfPieceIsScared(piece,to_row,to_col))
	{
		return false;
	}
	else if(piece[1] == 'L')
	{
		if(direction !== "DIAGONAL" ||
			checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			return false;
		}
	}
	else if(piece[1] == 'E')
	{
		if(checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
			return false;
		}
	}
	else
	{
		if((direction !== "VERTICAL" && direction !== "HORIZONTAL") ||
			checkTheDirectionOfMoveForObstacles(from_row,from_col,to_row,to_col)){
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
	if(barca_array[3][3] != "." && barca_array[3][3][0] == barca_array[3][6][0] &&
		barca_array[3][6][0] == barca_array[6][6][0]){
		victory = true;
		who_won = (barca_array[3][3][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "Game is over.." + who_won + " won!";
		placeCrownOnWinningPieces();
		return true;
	}
	else if(barca_array[3][3] != "." && barca_array[3][3][0] == barca_array[6][3][0] &&
		barca_array[6][3][0] == barca_array[6][6][0]){
		victory = true;
		who_won = (barca_array[3][3][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "Game is over.." + who_won + " won!";
		placeCrownOnWinningPieces();
		return true;
	}
	else if(barca_array[3][3] != "." && barca_array[3][3][0] == barca_array[6][3][0] &&
		barca_array[6][3][0] == barca_array[3][6][0]){
		victory = true;
		who_won = (barca_array[3][3][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "Game is over..." + who_won + " won!";
		placeCrownOnWinningPieces();
		return true;
	}
	else if(barca_array[3][6] != "." && barca_array[3][6][0] == barca_array[6][3][0] &&
		barca_array[6][3][0] == barca_array[6][6][0]){
		victory = true;
		who_won = (barca_array[3][6][0] == 'W') ? "WHITE" : "BLACK";
		document.getElementById("message").innerHTML = "Game is over..." + who_won + " won!";
		placeCrownOnWinningPieces();
		return true;
	}
	return false;
}

function placeCrownOnWinningPieces() {

	if(who_won === "BLACK"){
			document.getElementById(getDiv("BE1")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("BE2")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("BL1")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("BL2")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("BR1")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("BR2")).innerHTML += '<img src = "./images/crown.gif" />';
	}
	else if(who_won === "WHITE"){

			document.getElementById(getDiv("WE1")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("WE2")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("WL1")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("WL2")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("WR1")).innerHTML += '<img src = "./images/crown.gif" />';
			document.getElementById(getDiv("WR2")).innerHTML += '<img src = "./images/crown.gif" />';
	}
}

function resetBoardScaredAndTrappedPieces(data){
	var pieces = data["pieces"];
	var ai_move = data["move"];
	var src = ai_move[0];
	var dest = ai_move[1];
	var piece_info = barca_array[src[0]][src[1]];
	document.getElementById("tile_"+src[0]+","+src[1]).innerHTML = "";
	movePiece(piece_info[0],piece_info[1],dest[0],dest[1]);
	barca_array[dest[0]][dest[1]] = barca_array[src[0]][src[1]];
	barca_array[src[0]][src[1]] = ".";
	piece_locations[barca_array[dest[0]][dest[1]]] = dest[0] * 10 + dest[1];
	scared_pieces = new Set();
	trapped_pieces = [];

	for(var i = 0; i < pieces.length; i++){
		if(pieces[i][5]){
			trapped_pieces.push(barca_array[pieces[i][2]][pieces[i][3]]);
		}
		if(pieces[i][4]){
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


/*Function that computes the pieces a certain user can move*/
function recomputeValidClicks(turn){
	valid_clicks = [];
	console.log("Scared pieces size: " + scared_pieces.size);
	scared_pieces.forEach(function(value){
		if(value[0] === turn[0]){
			valid_clicks.push(piece_locations[value]);
		}
	});

	if(valid_clicks.length == 0){
			if((checkIfInTrappedPieces(turn[0]+"E1") && singleMoveExists[turn[0]+"E1"]) ||
				checkIfASingleValidMoveExistsForElephant(turn[0]+"E1")){
				valid_clicks.push(piece_locations[turn[0]+"E1"]);
		 	}
			if((checkIfInTrappedPieces(turn[0]+"E2") && singleMoveExists[turn[0]+"E2"]) ||
				checkIfASingleValidMoveExistsForElephant(turn[0]+"E2")){
				valid_clicks.push(piece_locations[turn[0]+"E2"]);
		 	}
			if((checkIfInTrappedPieces(turn[0]+"L1") && singleMoveExists[turn[0]+"L1"]) ||
				checkIfASingleValidMoveExistsForLion(turn[0]+"L1")){
				valid_clicks.push(piece_locations[turn[0]+"L1"]);
		 	}
			if((checkIfInTrappedPieces(turn[0]+"L2") && singleMoveExists[turn[0]+"L2"]) ||
				checkIfASingleValidMoveExistsForLion(turn[0]+"L2")){
				valid_clicks.push(piece_locations[turn[0]+"L2"]);
		 	}
			if((checkIfInTrappedPieces(turn[0]+"R1") && singleMoveExists[turn[0]+"R1"]) ||
				checkIfASingleValidMoveExistsForMouse(turn[0]+"R1")){
				valid_clicks.push(piece_locations[turn[0]+"R1"]);
		 	}
			if((checkIfInTrappedPieces(turn[0]+"R2") && singleMoveExists[turn[0]+"R2"]) ||
				checkIfASingleValidMoveExistsForMouse(turn[0]+"R2")){
				valid_clicks.push(piece_locations[turn[0]+"R2"]);
		 	}
	}
}

/*Function that returns right image extension for the piece*/
function findImgName(side,type){
	switch(type){
		case 'E': return (side == 'W') ? "elephantW.gif" : "BlackElephant.gif";
		case 'L': return (side == 'W') ? "lionW.gif" : "BlackLion.gif";
		default: return (side == 'W') ? "mouseW.gif" : "BlackMouse.gif";
	}
}

/*Function set image to black*/
function movePiece(side,type,row,col){
	document.getElementById("tile_"+row+","+col).innerHTML = '<img src = \''+"./images/"+findImgName(side,type)+'\'/>';
}

function getAIMove(){
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
		info[0][4] = checkIfPieceIsScared(piece);
		info[0][5] = checkIfInTrappedPieces(piece);
		pieces = pieces.concat(info);
	}
	API_request["human_move"] = [[0,0],[0,5]];
	API_request["pieces"] = pieces;

	$.ajax({
			type: "POST",
			url: "https://serene-everglades-79780.herokuapp.com/api",
			data: JSON.stringify(API_request),
			dataType: "json",
			contentType: 'application/json',
			success: function(data){
				removeImageForScaredAndTrappedPieces();
				removeImageForWateringHoles();
				resetBoardScaredAndTrappedPieces(data);
				recomputeValidClicks(player_TURN);
				placeImageForScaredAndTrappedPieces();
				placeImageForWateringHolesIfEmpty();
			},
			error: function(data){
				alert("fail");
			}
		});
	/*Send API request*/
	/*Get the move from AI*/
}

/*Function that detects clicks and displays interactive user messages*/
function clickMade(row,col,id,val){
	row = parseInt(row);
	col = parseInt(col);
	var num = row*10 + col;

	if(!gameStarted){
		return;
	}

	if(victory){
		document.getElementById("message").innerHTML = "Game is over.."+who_won+" won.";
	}
	else if(verifyValidClick(num)){
		clicks_made = [];
		clicks_made.push(num);
		document.getElementById("message").innerHTML = "Choose where you want to move the piece to or select another piece to move...";
	}
	else if(clicks_made.length == 1){
		var r1 = Math.floor(clicks_made[0]/10);
		var c1 = clicks_made[0]%10;
		var value = verifyValidMove(r1,c1,row,col);

		if(value)
		{
			removeImageForScaredAndTrappedPieces();
			removeImageForWateringHoles();
			document.getElementById("tile_"+r1+","+c1).innerHTML = "";
			movePiece(barca_array[r1][c1][0],barca_array[r1][c1][1],row,col);
			barca_array[row][col] = barca_array[r1][c1];
			barca_array[r1][c1] = ".";
			piece_locations[barca_array[row][col]] = row * 10 + col;
			clicks_made = [];
			singleMoveExists = {};
			calculateScaredPieces();
			calculateTrappedPieces();
			placeImageForScaredAndTrappedPieces();
			placeImageForWateringHolesIfEmpty();
			AIsmove = true;

			if(checkVictory()){
				return;
			}
			/* IF MODE IS PLAYER V. AI*/
			else if(mode === "PLAYER V. AI"){
				printTurn();
				getAIMove();
				AIsmove = false;
				printTurn();
			}
			/* IF MODE IS PLAYER V. PLAYER */
			else{
				switchTurn();
				recomputeValidClicks(player_TURN);
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
		document.getElementById("message").innerHTML = "Invalid Move. Please select a valid move...";
	}
}

/*Initially does the move checking if it is AIs turn*/
function checkIfItIsAIsMove(){
	if(player_TURN === "BLACK"){
			AIsmove = true;
			printTurn();
			getAIMove();
			AIsmove = false;
			printTurn();
	}
}

/* Returns the div of the piece*/
function getDiv(piece){
	var location_piece = piece_locations[piece];
	var row = Math.floor(location_piece/10);
	var col = location_piece%10;
	return "tile_" + row + "," + col;
}

$(document).ready(function(){
	$("#playeroption").click(function(){
		if(!gameStarted){
			player_TURN = $("#playeroption").val();
			placeInitImage();
		}
	});
});


function startGame(){
	if(gameStarted){
		var value = confirm("Are you sure you want to start another game?");
		if(value){
			document.getElementById("barca_board").innerHTML = "";
			player_TURN = $("#playeroption").val();
			mode = $("#gametype").val();
			newBoard();
			placeInitImage();
			placeWateringHoles();
			gameStarted = true;
			initValidClicks();
		}
	}
	else{
		player_TURN = $("#playeroption").val();
		mode = $("#gametype").val();
		gameStarted = true;
		initValidClicks();
	}
}

function resetGame(){
	if(gameStarted){
		var value = confirm("Are you sure you want to reset the game back to its original state?");
		if(value){
			document.getElementById("barca_board").innerHTML = "";
			mode = $("#gametype").val();
			newBoard();
			placeInitImage();
			placeWateringHoles();
			gameStarted = true;
			initValidClicks();
		}
	}
}
