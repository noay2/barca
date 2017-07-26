from flask import Flask, jsonify, request
from flask_cors import CORS,cross_origin
from barca import Backend

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return '<h1>Deployed to Heroku!!!</h1>'

@app.route('/api',methods = ['POST'])
@cross_origin()
def post_move():
	backend = Backend();
	json_response = dict()	
	array_pieces_info = []
	data = request.get_json(silent = True)
	
	for piece_info in data["pieces"]:
		array_pieces_info.append(piece_info)
	
	whitetomove = data["whitetomove"]
	human_move = data["human_move"]
	backend.receive_data(whitetomove,array_pieces_info,human_move)
	new_board = backend.send_updated_data()	
	json_response["whitetomove"] = new_board[0]
	json_response["pieces"] = new_board[1]
	json_response["move"] = new_board[2]
	return jsonify(json_response)
	
@app.route('/*')
@cross_origin()
def throw_error():
	return '<h1>404 not found!!!</h1>'
