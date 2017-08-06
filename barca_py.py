import time
import random
import copy
from collections import defaultdict


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
    piece_type_direction = {"MOUSE": { (i,j) for j in range(-1,2,1) for i in range(-1,2,1) if (abs(i) ==abs(j) )       and not(i==0 and j==0)   },
                            "LION":  { (i,j) for j in range(-1,2,1) for i in range(-1,2,1) if (i==0 or j==0 )and not(i==0 and j==0)   },
                            "ELEPHANT":{(i,j)for j in range(-1,2,1) for i in range(-1,2,1) if                    not(i==0 and j==0)   }
                            }
    
    def __init__(self, piece_arr, board_coord, pieces):
        self.color   = piece_arr[0]
        self.type    = piece_arr[1]
        self.row     = piece_arr[2]
        self.col     = piece_arr[3]
        self.infear  = piece_arr[4]
        self.trapped = piece_arr[5]
        self.board_coord = board_coord
        self.board_coord[self.row][self.col]  = self
        self.piece_type = pieces[Piece.piece_color_val[self.color] ][Piece.piece_type_val[self.type]]
        self.piece_type.append(self)
        self.piece_type_directions = Piece.piece_type_direction[self.type]
        self.team_pieces = pieces[Piece.piece_color_val[self.color] ]
        self.scared_of_pieces = pieces[  (Piece.piece_color_val[self.color] +1)%2][(Piece.piece_type_val[self.type] +1) %3]
        
        

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
            for piece_type in self.team_pieces:
                for piece in piece_type:
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
                          (colt >=0) and    (colt<Piece.cols) and self.board_coord[rowt][colt] == None:
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
                          (colt >=0) and    (colt<Piece.cols) and self.board_coord[rowt][colt] == None:
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

    def move_piece(self, source, dest):
        self.row = source[0]
        self.col = source[1]
        self.board_coord[dest[0]][dest[1]] = None
        self.board_coord[source[0]][source[1]] = self
        
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
    piece_type_direction = {"MOUSE": [ [i,j] for j in range(-1,2,1) for i in range(-1,2,1) if (abs(i) ==abs(j) )       and not(i==0 and j==0)   ],
                            "LION":  [ [i,j] for j in range(-1,2,1) for i in range(-1,2,1) if (i==0 or j==0 )and not(i==0 and j==0)   ],
                            "ELEPHANT":[[i,j]for j in range(-1,2,1) for i in range(-1,2,1) if                    not(i==0 and j==0)   ]
                            }

    
    def __init__(self,whitetomove, pieces):
        self.whitetomove = whitetomove
        self.board_coord = [[None for j in range(10)] for i in range(10) ]
        self.pieces = [[ [] for j in range(3)]for i in range(2)]
        for piece in pieces:
                Piece(piece, self.board_coord, self.pieces)



        self.current_hash =  self.initial_hash()
        self.position_counter = defaultdict(int)
        self.position_score   = defaultdict(int)



                

    def initial_hash(self):
        number = 0
        for piece in self.all_pieces():
            number +=  ( Piece.piece_color_val[piece.color] * 3 + Piece.piece_type_val[piece.type] +1   ) *  (8  **  (piece.row * 10 + piece.col))
        return number


    def undo_hash(self, piece):
        return  self.current_hash- ( Piece.piece_color_val[piece.color] * 3 + Piece.piece_type_val[piece.type] +1   ) *  (8  **  (piece.row * 10 + piece.col))


    def update_hash(self,piece):
        return  self.current_hash + ( Piece.piece_color_val[piece.color] * 3 + Piece.piece_type_val[piece.type] +1   ) *  (8  **  (piece.row * 10 + piece.col))
        
                                                
    def current_pieces(self):
          for piece_type in self.pieces[self.whitetomove]: 
              for piece in piece_type:
                    yield piece
              

    def other_pieces(self):
          for piece_type in self.pieces[(self.whitetomove +1) %2 ]: 
              for piece in piece_type:
                    yield piece
                
    def all_pieces(self):
        for piece_color in self.pieces:
            for piece_type in piece_color: 
                for piece in piece_type:
                    yield piece

    
    def board_evaluation(self, watering_holes_value, adjacent_watering_holes_value,center_encouragement_value, scared_pieces_value):
        score=0

        #Draw
        if self.position_counter[self.current_hash] >=3:
            return 0
        
        #How many watering holes you have:
        white_counter = 0
        black_counter = 0
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if (self.board_coord[int(watering_hole_row)][int(watering_hole_col)]!= None):
                if (self.board_coord[int(watering_hole_row)][int(watering_hole_col)]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
                    
        score += watering_holes_value[white_counter]
        score -= watering_holes_value[black_counter]

        for piece in self.all_pieces():
            #Are you next to a watering hole:
            for watering_hole_row, watering_hole_col in Board.watering_holes:
                if piece.adjacent_to(watering_hole_row, watering_hole_col):
                    score+=  adjacent_watering_holes_value * (1 if piece.color == 'WHITE' else -1)
            
            #How close are you to the center 
            score += center_encouragement_value * (        (40.5 - ((4.5 - piece.row)**2 +(4.5-piece.col)**2    ))/40.5) * (1 if piece.color == 'WHITE' else -1)
            
            #How many pieces do you fear the current turn
            if piece.infear:
                score -=scared_pieces_value * (1 if piece.color == 'WHITE' else -1)

        return score

    
    def fear_update(self,moving_piece):
        for piece in self.all_pieces():
            if (piece.infear) or (piece.infear_of(moving_piece)) :
                piece.modify_fear()

                
                
    def victory(self):
        white_counter = 0
        black_counter = 0
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if (self.board_coord[int(watering_hole_row)][int(watering_hole_col)]!= None):
                if (self.board_coord[int(watering_hole_row)][int(watering_hole_col)]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
        if black_counter >= 3:
            return "BLACK"
        elif white_counter >=3:
            return "WHITE"
        else:
            return None

    def draw(self):
        return self.position_counter[self.current_hash] >=3
    
    def switch_turn(self): 
        self.whitetomove = not self.whitetomove
    

                
    def update(self, source, dest):
        piece = self.board_coord[source[0]][source[1]]


        self.current_hash = self.undo_hash(piece)
        piece.move_piece(source, dest)
        self.current_hash  = self.update_hash(piece)
        self.position_counter[self.current_hash] +=1
        
        self.fear_update(piece)
        self.switch_turn()

    def undo_update(self, source, dest, old_infear_trapped):
        piece = self.board_coord[dest[0]][dest[1]]

        self.position_counter[self.current_hash] -=1
        self.current_hash = self.undo_hash(piece)
        piece.move_piece(dest, source)
        self.current_hash  = self.update_hash(piece)
        
        for index , piece in enumerate(self.all_pieces()):
            piece.infear, piece.trapped = old_infear_trapped[index]
        self.switch_turn()

    def send_updated_data(self):
        return [self.whitetomove ]+ [[ piece.send_updated_data() for piece in self.all_pieces()]]
            
        
##########################################       
class AI:

    def __init__(self,whitetomove, pieces,human_move,watering_holes_value, adjacent_watering_holes_value, scared_pieces_value, center_encouragement_value):
        self.board = Board(whitetomove, pieces,watering_holes_value, adjacent_watering_holes_value, scared_pieces_value, center_encouragement_value)
        self.watering_holes_value = watering_holes_value
        self.adjacent_watering_holes_value = adjacent_watering_holes_value
        self.scared_pieces_value = scared_pieces_value
        self.center_encouragement_value = center_encouragement_value
        self.recurse = 3
        self.ai_move = [None, None]



    def evaluate_other_board(self, board):
        return board.board_evaluation(self.watering_holes_value, self.adjacent_watering_holes_value,self.center_encouragement_value, self.scared_pieces_value) * 1 if board.whitetomove else -1



                                  
    def AI_alpha_beta(self, recurse,alpha =-1000000000.0, beta = 1000000000.0 ):
        if self.board.current_hash in self.board.position_score:
            return [None, None, self.board.position_score[self.board.current_hash]]
        
        elif recurse == 0 or self.board.victory() or self.board.draw():
            score = self.board.board_evaluation(self.watering_holes_value, self.adjacent_watering_holes_value,self.center_encouragement_value, self.scared_pieces_value)
            self.board.position_score[self.board.current_hash] = score
            return  [None, None,score]

        else:
   
  
            if (self.board.whitetomove):
                current_best_source,current_best_dest,current_best_score   = None,None,-1000000000.0
                for piece in self.board.current_pieces():
                    for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                        old_infear_trapped= [[piece.infear, piece.trapped] for piece in (self.board.all_pieces())]
                        self.board.update([source_row, source_col], [dest_row, dest_col])
                        childs_worst_source, childs_worst_dest, childs_worst_score= self.AI_alpha_beta(  recurse-1,alpha, beta)
                        self.board.undo_update( [source_row, source_col],[dest_row, dest_col],old_infear_trapped)
                        if  childs_worst_score> current_best_score:
                            current_best_source,current_best_dest,current_best_score = [source_row, source_col],[dest_row, dest_col ],childs_worst_score
                            alpha = max(alpha, childs_worst_score)
                            if (alpha>beta):
                                return [current_best_source, current_best_dest, current_best_score]

                self.board.position_score[self.board.current_hash] = current_best_score                           
                return [current_best_source, current_best_dest, current_best_score]



            else:
                current_worst_source,current_worst_dest,current_worst_score   = None,None,1000000000.0
                for piece in self.board.current_pieces():
                    for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                        old_infear_trapped = [[piece.infear, piece.trapped] for piece in (self.board.all_pieces())]
                        self.board.update([source_row, source_col], [dest_row, dest_col])
                        childs_best_source, childs_best_dest, childs_best_score = self.AI_alpha_beta(  recurse-1,alpha, beta)
                        self.board.undo_update( [source_row, source_col],[dest_row, dest_col],old_infear_trapped)
                        if  childs_best_score< current_worst_score:
                            current_worst_source,current_worst_dest,current_worst_score = [source_row, source_col],[dest_row, dest_col ],childs_best_score
                            beta = min(beta, childs_best_score)
                            if (alpha>beta):
                                return [current_worst_source, current_worst_dest, current_worst_score]

                self.board.position_score[self.board.current_hash] = current_worst_score 
                return [current_worst_source, current_worst_dest, current_worst_score]


    def execute(self):
        if (not self.board.victory()):
            self.ai_move= (self.AI_alpha_beta(self.recurse))[0:2]
            self.board.update(self.ai_move[0], self.ai_move[1])
            

    def send_updated_data(self):
        return self.board.send_updated_data() + [[self.ai_move[0], self.ai_move[1]]]

##########################################
class Backend:
    def __init__(self, watering_holes_value = [20,50], adjacent_watering_holes_value = 5, scared_pieces_value = 5, center_encouragement_value = .4 ):
        self.watering_holes_value = [0] + watering_holes_value + [1000000]
        self.adjacent_watering_holes_value = adjacent_watering_holes_value
        self.scared_pieces_value = scared_pieces_value
        self.center_encouragement_value = center_encouragement_value

    def receive_data(self, whitetomove, pieces,human_move):
        self.AI = AI(whitetomove, pieces, human_move, self.watering_holes_value, self.adjacent_watering_holes_value, self.scared_pieces_value, self.center_encouragement_value)
        self.AI.execute()



    def send_updated_data(self):
        updated_data = self.AI.send_updated_data()
        return updated_data
