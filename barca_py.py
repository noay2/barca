import time
##########################################
class Piece:
    colors = ["BLACK", "WHITE"]
    types  = ["ELEPHANT", "MOUSE", "LION"]
    rows = 10                                  
    cols = 10
    init_piece_position =\
            {
                                (int(rows -1),int(cols/2 -1)), (int(rows -1),int(cols/2)),(int(rows -2),int(cols/2 -1)),
                                (int(rows -2),int(cols/2)),   (int(rows -2),int(cols/2 -2)),(int(rows -2),int(cols/2 +1)),
           
                                (int(0),int(cols/2 -1)),(int(0),int(cols/2)), (int(1),int(cols/2 -1)),
                                (int(1),int(cols/2)), (int(1),int(cols/2 -2)), (int(1),int(cols/2 +1))
             }
    watering_holes      =\
            {
                              (int(rows/2 -2),int( cols/2 -2)),(int(rows/2 -2),int( cols/2 +1)),
                              (int(rows/2 +1),int( cols/2 -2)),(int(rows/2 +1),int( cols/2 +1))
                            
            }
    piece_color_val = {"BLACK": 0, "WHITE": 1}
    piece_type_val  = {"MOUSE":0, "LION":1, "ELEPHANT": 2}
    
    def __init__(self, piece_arr, board, team_pieces,piece_type,scared_of_pieces):
        self.color   = piece_arr[0]
        self.type    = piece_arr[1]
        self.row     = piece_arr[2]
        self.col     = piece_arr[3]
        self.infear  = piece_arr[4]
        self.trapped = piece_arr[5]
        self.board = board
        self.board[self.row][self.col]  = self
        self.team_pieces = team_pieces
        self.team_pieces.append(self)
        self.piece_type = piece_type
        self.piece_type.add(self)
        self.scared_of_pieces = scared_of_pieces

    def __repr__(self):
        return "*" +self.color[0] +self.type[0]+"*"

    def adjacent_to(self, row, col):
        return (abs(row- self.row) <=1) and (abs(col - self.col) <=1)
    
    def scares(self, piece):
        return piece.scared_of(self)

    def scared_of(self, piece):
        return piece in self.scared_of_pieces
    
    def intimidates(self, piece):
        if piece.scared_of(self) and self.adjacent_to(piece.row, piece.col):
            return True
        else:
            return False

    def infear_of(self, piece):
        if self.scared_of(piece) and self.adjacent_to(piece.row, piece.col):
            return True
        else:
            return False

    def potential_infear_of(self,row,col):
        for piece in self.scared_of_pieces:
            if piece.adjacent_to(row, col):
                return True
        return False      
    
    def valid_moves(self):
        if not(self.infear):
            for piece in self.team_pieces:
                if piece.infear and (not piece.trapped) and (piece.color ==self.color):
                    return
        rowt = self.row
        colt = self.col
        for rowd in range(-1,2,1):
            for cold in range(-1,2,1):
                if (rowd ==0) and (cold==0):
                    pass
                elif ( (abs(cold) == abs(rowd)) and (self.type == "LION" or self.type == "ELEPHANT")) \
                   or (( (cold ==0) or (rowd==0)) and (self.type == "MOUSE" or self.type == "ELEPHANT")):
                    colt += cold
                    rowt += rowd
                    while (rowt >=0) and (rowt < Piece.rows) and\
                          (colt >=0) and    (colt<Piece.cols) and self.board[rowt][colt] == None:
                        if (not self.potential_infear_of(rowt,colt)) or self.trapped:
                            yield [self.row, self.col, rowt , colt]
                        rowt+=rowd
                        colt+=cold
                rowt = self.row
                colt = self.col

    def modify_fear(self):
        if (not self.potential_infear_of(self.row, self.col)):
            self.infear = False
            self.trapped = False
            return
        rowt = self.row
        colt = self.col
        for rowd in range(-1,2,1):
            for cold in range(-1,2,1):
                if (rowd ==0) and (cold==0):
                    pass
                elif ( (abs(cold) == abs(rowd)) and (self.type == "LION" or self.type == "ELEPHANT")) \
                   or (( (cold ==0) or (rowd==0)) and (self.type == "MOUSE" or self.type == "ELEPHANT")):
                    colt += cold
                    rowt += rowd
                    while (rowt >=0) and (rowt < Piece.rows) and\
                          (colt >=0) and    (colt<Piece.cols) and self.board[rowt][colt] == None:
                        if (not self.potential_infear_of(rowt,colt)):
                            self.infear = True
                            self.trapped = False
                            return
                        rowt+=rowd
                        colt+=cold
                rowt = self.row
                colt = self.col
        self.infear = True
        self.trapped= True
        return

        
    def send_updated_data(self):

        return ([self.color, self.type, self.row, self.col, self.infear, self.trapped])
        
#)#########################################              
class Board:
    colors = ["BLACK", "WHITE"]
    types  = ["ELEPHANT", "MOUSE", "LION"]
    rows = 10                                  
    cols = 10
    init_piece_position =\
            {
                                (int(rows -1),int(cols/2 -1)), (int(rows -1),int(cols/2)),(int(rows -2),int(cols/2 -1)),
                                (int(rows -2),int(cols/2)),   (int(rows -2),int(cols/2 -2)),(int(rows -2),int(cols/2 +1)),
           
                                (int(0),int(cols/2 -1)),(int(0),int(cols/2)), (int(1),int(cols/2 -1)),
                                (int(1),int(cols/2)), (int(1),int(cols/2 -2)), (int(1),int(cols/2 +1))
             }
    watering_holes      =\
            {
                              (int(rows/2 -2),int( cols/2 -2)),(int(rows/2 -2),int( cols/2 +1)),
                              (int(rows/2 +1),int( cols/2 -2)),(int(rows/2 +1),int( cols/2 +1))
                            
            }
    piece_color_val = {"BLACK": 0, "WHITE": 1}
    piece_type_val  = {"MOUSE":0, "LION":1, "ELEPHANT": 2}

    
    def __init__(self,whitetomove, pieces):
        piece_array = [[set() for j in range(3)]for i in range(2)]
        self.board = [[None for j in range(10)] for i in range(10) ]
        self.whitetomove = whitetomove
        self.black_pieces = []
        self.white_pieces = []
        for piece in pieces:
                piece_instance = Piece(piece, self.board,self.black_pieces if piece[0] == "BLACK" else self.white_pieces,
                piece_array[Board.piece_color_val[piece[0]] ][Board.piece_type_val[piece[1]]],
                piece_array[(Board.piece_color_val[piece[0]] + 1)%2][(Board.piece_type_val[piece[1]] + 1)%3])
                                                
    def current_pieces(self):
        if self.whitetomove:
            for piece in self.white_pieces:           
                yield piece
        else:
            for piece in self.black_pieces:
                yield piece

    def other_pieces(self):
        if not self.whitetomove:
            for piece in self.white_pieces:           
                yield piece
        else:
            for piece in self.black_pieces:
                yield piece
                
    def all_pieces(self):
        for piece in (self.white_pieces + self.black_pieces):
            yield piece

    def watering_hole_counter(self):
        white_counter = 0
        black_counter = 0
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if (self.board[int(watering_hole_row)][int(watering_hole_col)]!= None):
                if (self.board[int(watering_hole_row)][int(watering_hole_col)]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
        return [white_counter, black_counter]
    
    def board_evaluation(self):
        score=0

        #How many watering holes you have:
        acquired_holes_white, acquired_holes_black= self.watering_hole_counter()
        holes = acquired_holes_white if self.whitetomove else acquired_holes_black
        score += [0,20,50,1000000,1000000][holes]

        #Are you next to a watering hole:
        for piece in self.current_pieces():
            for watering_hole_row, watering_hole_col in Board.watering_holes:
                if piece.adjacent_to(watering_hole_row, watering_hole_col):
                    score=score+5

        #How many pieces do you fear the current turn
        for piece in self.other_pieces():
            if piece.infear:
                score +=4

        #Going Through All Validmoves
        for piece in self.current_pieces():
            for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                #Every Available Validmove is good
                score+=0.2
                for other_piece in self.other_pieces():
                    #If you can fear an opponent the next turn
                    if other_piece.scared_of(piece) and other_piece.adjacent_to(dest_row, dest_col):
                        score +=.4
                        #If you can fear a watering hole occupent the next turn, +10
                        if(other_piece.row, other_piece.col) in Board.watering_holes: 
                            score+=2 
                #Can you get a hole next turn, that is nice:)
                if (dest_row, dest_col) in Board.watering_holes:
                    score +=[5,10,20,10000000,1000000][holes]


        #Are your pieces Afraid?
        for piece in self.current_pieces():
            if  piece.infear:
                score-=5

        return score

    
    def fear_update(self,moving_piece):
        for piece in self.all_pieces():
            if (piece.infear) or (piece.infear_of(moving_piece)) :
                piece.modify_fear()
                
                
    def victory(self):
        black_counter, white_counter = self.watering_hole_counter()
        if black_counter >= 3:
            self.victory = "WHITE"
            return "WHITE"
        elif white_counter >=3:
            self.victory = "BLACK"
            return "BLACK"
        else:
            return None

        
    def switch_turn(self):
        if not self.victory():
            self.whitetomove = not self.whitetomove
    

                
    def update(self, source, dest):
        piece = self.board[source[0]][source[1]]
        piece.row = dest[0]
        piece.col = dest[1]
        self.board[source[0]][source[1]] = None
        self.board[dest[0]][dest[1]] = piece

        
        self.fear_update(piece)
        self.switch_turn()

    def send_updated_data(self):
        return [self.whitetomove ]+ [ piece.send_updated_data() for piece in self.all_pieces()]
            
        
##########################################       
class AI:

    def __init__(self,whitetomove, pieces):
        self.board = Board(whitetomove, pieces)
                                  
    def AI_decide_self(self):                                        
        current_worst_move = 100000000000
        current_source = [0,0]
        current_dest   = [0,0]                               
        for piece in self.board.current_pieces():
            for source_row, source_col, dest_row, dest_col in piece.valid_moves():            
 #               infear_array = [ piece.infear for piece in self.board.pieces]
#                trapped_array= [ piece.trapped for piece in self.board.pieces]
                
                self.board.update([source_row, source_col], [dest_row, dest_col])                               
                board_state = self.board.board_evaluation()
                if board_state<current_worst_move:
                    current_worst_move=board_state
                    current_source = [source_row, source_col]
                    current_dest = [dest_row, dest_col]
                self.board.update([dest_row, dest_col], [source_row, source_col])
                
 #               for piece in range(len(self.board.pieces)):
#                    self.board.pieces[piece].infear = infear_array[piece]
#                    self.board.pieces[piece].trapped = trapped_array[piece]
            
        return [current_source, current_dest]

    def execute(self):
        if (not self.board.victory()):
            ai_source, ai_dest = self.AI_decide_self()
            self.board.update(ai_source, ai_dest)
            

    def send_updated_data(self):
        return self.board.send_updated_data()

##########################################
class Backend:
    def __init__(self):
        pass

    def receive_data(self, whitetomove, pieces):
        self.AI = AI(whitetomove, pieces)
        self.AI.execute()



    def send_updated_data(self):
        updated_data = self.AI.send_updated_data()
        return updated_data
##########################################


















#########################################
    
if __name__ == "__main__":
    i  = time.time()
    backend = Backend()
    backend.receive_data(True, [['BLACK', 'ELEPHANT', 9, 4, False, False],
                                                                   ['BLACK', 'ELEPHANT', 9, 5, False, False],
                                                                   ['BLACK', 'MOUSE', 8, 4, False, False],
                                                                   ['BLACK', 'MOUSE', 8, 5, False, False],
                                                                   ['BLACK', 'LION', 8, 3, False, False],
                                                                   ['BLACK', 'LION', 8, 6, False, False],
                                                                   ['WHITE', 'ELEPHANT', 0, 4, False, False],
                                                                   ['WHITE', 'ELEPHANT', 0, 5, False, False],
                                                                   ['WHITE', 'MOUSE', 1, 4, False, False],
                                                                   ['WHITE', 'MOUSE', 1, 5, False, False],
                                                                   ['WHITE', 'LION', 1, 3, False, False],
                                                                   ['WHITE', 'LION', 1, 6, False, False]])

    
    output = backend.send_updated_data()
    backend.receive_data(True, [['WHITE', 'ELEPHANT', 0, 4, False, False],
                         ['WHITE', 'ELEPHANT', 0, 5, False, False],
                         ['WHITE', 'LION', 1, 3, False, False],
                         ['WHITE', 'MOUSE', 1, 5, False, False],
                         ['WHITE', 'LION', 1, 6, False, False],
                         ['WHITE', 'MOUSE', 1, 4, True, False],
                         ['BLACK', 'LION', 5, 3, False, False],
                         ['BLACK', 'LION', 7, 4, False, False],
                         ['BLACK', 'MOUSE', 8, 4, False, False],
                         ['BLACK', 'MOUSE', 8, 5, False, False],
                         ['BLACK', 'ELEPHANT', 9, 4, False, False],
                         ['BLACK', 'ELEPHANT', 9, 5, False, False]])
    
    output = backend.send_updated_data()
    backend.receive_data(True,
                                                                     [['BLACK', 'ELEPHANT', 9, 5, False, False],
                                                                   ['BLACK', 'MOUSE', 8, 4, False, False],
                                                                   ['BLACK', 'MOUSE', 5, 5, False, False],
                                                                   ['BLACK', 'LION', 8, 3, False, False],
                                                                   ['BLACK', 'LION', 8, 6, False, False],
                                                                   ['WHITE', 'ELEPHANT', 0, 4, False, False],
                                                                   ['WHITE', 'ELEPHANT', 0, 5, False, False],
                                                                   ['WHITE', 'MOUSE', 1, 4, False, False],
                                                                   ['WHITE', 'MOUSE', 1, 5, False, False],
                                                                   ['WHITE', 'LION', 1, 3, False, False],
                                                                   ['WHITE', 'LION', 1, 6, False, False]])


    output = backend.send_updated_data()
    print(time.time() -i)
