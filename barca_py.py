import time
import random
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

    
    def board_evaluation(self):
        score=0



        #How many watering holes you have:
        white_counter = 0
        black_counter = 0
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if (self.board[int(watering_hole_row)][int(watering_hole_col)]!= None):
                if (self.board[int(watering_hole_row)][int(watering_hole_col)]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
        holes = white_counter if self.whitetomove else black_counter
        score += [0,20,50,1000000,1000000][holes]

        for piece in self.current_pieces():
            #Are you next to a watering hole:
            for watering_hole_row, watering_hole_col in Board.watering_holes:
                if piece.adjacent_to(watering_hole_row, watering_hole_col):
                    score=score+5
            #How close are you to the center 
            score += .4 * (        (40.5 - ((4.5 - piece.row)**2 +(4.5-piece.col)**2    ))/40.5)
            
        #How many pieces do you fear the current turn
        for piece in self.other_pieces():
            if piece.infear:
                score +=5

                

        #Are your pieces Afraid?
        for piece in self.current_pieces():
            if  piece.infear:
                score-=5

        #Random element
        score += random.randint(0,5)

        return score

    
    def fear_update(self,moving_piece):
        for piece in self.all_pieces():
            if (piece.infear) or (piece.infear_of(moving_piece)) :
                piece.modify_fear()
                
                
    def victory(self):
        white_counter = 0
        black_counter = 0
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if (self.board[int(watering_hole_row)][int(watering_hole_col)]!= None):
                if (self.board[int(watering_hole_row)][int(watering_hole_col)]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
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

    def __init__(self,whitetomove, pieces,human_move):
        self.board = Board(whitetomove, pieces)
        self.original_turn = whitetomove
        self.human_move = human_move
        self.ai_move = [None, None]
        self.recurse = 3
                                  
    def AI_alpha_beta(self, recurse,alpha =-1000000000.0, beta = 1000000000.0 ):
        if recurse == 0:
            return  [None, None,self.board.board_evaluation()]

        else:
   
  
            if ((self.recurse%2 ==0 and self.original_turn == self.board.whitetomove) or (self.recurse%2 ==1 and self.original_turn != self.board.whitetomove)):
                current_best_source   = None
                current_best_dest   = None
                current_best_score = -1000000000.0
                for piece in self.board.current_pieces():
                    for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                        self.board.update([source_row, source_col], [dest_row, dest_col])
                        childs_worst_source, childs_worst_dest, childs_worst_score= self.AI_alpha_beta(  recurse-1,alpha, beta)
                        self.board.update( [dest_row, dest_col],[source_row, source_col])
                        if  childs_worst_score> current_best_score:
                            current_best_source = [source_row, source_col]
                            current_best_dest = [dest_row, dest_col ]
                            current_best_score=childs_worst_score
                            alpha = max(alpha, childs_worst_score)
                            if (alpha>beta):
                                return [current_best_source, current_best_dest, current_best_score]

                            
                return [current_best_source, current_best_dest, current_best_score]



            else:
                current_worst_source   = None
                current_worst_dest   = None
                current_worst_score = 1000000000.0
                for piece in self.board.current_pieces():
                    for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                        self.board.update([source_row, source_col], [dest_row, dest_col])
                        childs_best_source, childs_best_dest, childs_best_score = self.AI_alpha_beta(  recurse-1,alpha, beta)
                        self.board.update( [dest_row, dest_col],[source_row, source_col])
                        if  childs_best_score< current_worst_score:
                            current_worst_source = [source_row, source_col]
                            current_worst_dest = [dest_row, dest_col ]
                            current_worst_score=childs_best_score
                            beta = min(beta, childs_best_score)
                            if (alpha>beta):
                                return [current_worst_source, current_worst_dest, current_worst_score]

                            
                return [current_worst_source, current_worst_dest, current_worst_score]


    def execute(self):
        if (not self.board.victory()):
            self.ai_move= (self.AI_alpha_beta(self.recurse))[0:2]
            self.board.update(self.ai_move[0], self.ai_move[1])
            

    def send_updated_data(self):
        return self.board.send_updated_data() + [self.ai_move[0], self.ai_move[1]]

##########################################
class Backend:
    def __init__(self):
        pass

    def receive_data(self, whitetomove, pieces,human_move):
        self.AI = AI(whitetomove, pieces, human_move)
        self.AI.execute()



    def send_updated_data(self):
        updated_data = self.AI.send_updated_data()
        return updated_data
##########################################


















#########################################
    
if __name__ == "__main__":
    pass
