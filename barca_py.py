import time
import math
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
             
    white_player_initial_hash =     419616483301654593334721783932067741879967698371037654176895614914325882259333160480768
    black_player_initial_hash =     209808241353657755148154874804759897695030898171462655505143703652773752188495670239232



    watering_holes      =\
            {
                              (int(rows/2 -2),int( cols/2 -2)),(int(rows/2 -2),int( cols/2 +1)),
                              (int(rows/2 +1),int( cols/2 -2)),(int(rows/2 +1),int( cols/2 +1))
                            
            }
    piece_color_val = {"BLACK": 0, "WHITE": 1}
    piece_type_val  = {"MOUSE":0, "LION":1, "ELEPHANT": 2}

    
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
    def can_move_to_square(self, direction, destination):
        #Made specifically for use in can_caputure_watering_hole function
        #Assuming that there are no obstructions between piece and destination in provided direction

        #Check if direction is appropriate to piece
        if(direction[0]==0 or direction[1]==0):
            if (piece.type=="LION"):
                return False
        elif (direction[0]==1 or direction[1]==1):
            if (piece.type=="MOUSE"):
                return False
        #Check if piece is deterred
        for fearsome_piece in piece.scared_of_pieces:
            if fearsome_piece.adjacent_to(destination[0], destination[1]):
                return False

        return True
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

    def update_piece(self, source, dest):
        self.row = dest[0]
        self.col = dest[1]
        self.board_coord[source[0]][source[1]] = None
        self.board_coord[dest[0]][dest[1]]     = self
        
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
    white_player_initial_hash =     419616483301654593334721783932067741879967698371037654176895614914325882259333160480768
    black_player_initial_hash =     209808241353657755148154874804759897695030898171462655505143703652773752188495670239232



    watering_holes      =\
            {
                              (int(rows/2 -2),int( cols/2 -2)),(int(rows/2 -2),int( cols/2 +1)),
                              (int(rows/2 +1),int( cols/2 -2)),(int(rows/2 +1),int( cols/2 +1))
                            
            }
    piece_color_val = {"BLACK": 0, "WHITE": 1}
    piece_type_val  = {"MOUSE":0, "LION":1, "ELEPHANT": 2}


    
    def __init__(self,whitetomove, pieces, previous_moves):
        self.whitetomove = whitetomove
        self.board_coord = [[None for j in range(Board.cols)] for i in range(Board.rows) ]
        self.pieces = [[ [] for j in range(3)]for i in range(2)]
        for piece in pieces:
                Piece(piece, self.board_coord, self.pieces)
        self.find_current_hash()

        self.position_counter = defaultdict(int)
        self.previous_moves = previous_moves
        self.hash_previous_moves()



    def hash_previous_moves(self):
        current_hash= Board.white_player_initial_hash
        self.position_counter[current_hash] +=1

        for previous_move in self.previous_moves:
            piece_color, piece_type, source_row, source_col, dest_row, dest_col = previous_move
            current_hash = self.undo_hash_previous_move(current_hash, piece_color, piece_type, source_row, source_col)
            current_hash = self.update_hash_previous_move(current_hash, piece_color, piece_type, dest_row, dest_col)
            self.position_counter[current_hash] +=1
            
          
    
                
    def undo_hash_previous_move(self,hash, color, type, row, col):
        return  hash- ( Piece.piece_color_val[color] * 3 + Piece.piece_type_val[type] +1   ) *  (8  **  (row * Board.rows + col))


    def update_hash_previous_move(self,hash, color, type, row, col):
        return  hash + ( Piece.piece_color_val[color] * 3 + Piece.piece_type_val[type] +1   ) *  (8  **  (row * Board.rows + col))

    def find_current_hash(self):
        number = 0
        for piece in self.all_pieces():
            number +=  ( Piece.piece_color_val[piece.color] * 3 + Piece.piece_type_val[piece.type] +1   ) *  (8  **  (piece.row * Board.rows + piece.col))
        self.current_hash = number        

    def undo_hash(self, piece):
        self.current_hash=  self.current_hash- ( Piece.piece_color_val[piece.color] * 3 + Piece.piece_type_val[piece.type] +1   ) *  (8  **  (piece.row * Board.rows + piece.col))


    def update_hash(self,piece):
        self.current_hash=  self.current_hash + ( Piece.piece_color_val[piece.color] * 3 + Piece.piece_type_val[piece.type] +1   ) *  (8  **  (piece.row * Board.rows + piece.col))
        
                                                
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
    
    def board_evaluation(self,watering_holes_value, future_watering_hole_value, adjacent_watering_holes_value,\
                               scared_pieces_value, teammate_value, center_encouragement_value):
        score=0
        

        #How many watering holes you have:
        white_counter = 0
        black_counter = 0
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if (self.board_coord[watering_hole_row][watering_hole_col]!= None):
                if (self.board_coord[watering_hole_row][watering_hole_col]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
                    
        score += watering_holes_value[white_counter]
        score -= watering_holes_value[black_counter]


	#How many watering holes you can get the next turn
        future_white_counter=0
        future_black_counter=0
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if (self.board_coord[watering_hole_row][watering_hole_col] == None):
                for x in (-1,2):
                    for y in (-1,2):
                        if ((x,y)!=(0,0)):
                            temp=[watering_hole_row+x, watering_hole_col+y] 
                            for i in range(3): 
                                if (temp[0], temp[1]) in Board.watering_holes:
                                    break
                                if self.board_coord[temp[0]][temp[1]]!=None:
                                    piece = self.board_coord[temp[0]][temp[1]]
                                    if ((piece.type == 'ELEPHANT') or (piece.type == 'MOUSE' and (x ==0 or y == 0)) or (piece.type == 'LION' and ( abs(x) ==1 and abs(y) == 1)))\
                                       and not ( piece.scared_of_pieces[0].adjacent_to(x,y) or  piece.scared_of_pieces[1].adjacent_to(x,y)):
                                        if (piece.color=="WHITE"):
                                            future_white_counter+=1
                                        else:
                                            future_black_counter+=1
                                    break
                                    
                            temp=[temp[0]+x, temp[1]+y]
                            
        score += future_watering_hole_value[white_counter + 1] * future_white_counter
        score -= future_watering_hole_value[black_counter + 1] * future_black_counter
        


        for piece in self.all_pieces():
            #Are you next to a watering hole:
            for watering_hole_row, watering_hole_col in Board.watering_holes:
                if piece.adjacent_to(watering_hole_row, watering_hole_col):
                    score+=  adjacent_watering_holes_value * (1 if piece.color == 'WHITE' else -1)
                    
            #How many pieces do you fear the current turn
            if piece.infear:
                score -=scared_pieces_value * (1 if piece.color == 'WHITE' else -1)
            
            #Do you have a teammate that can protect you
            for teammate in  self.pieces[Piece.piece_color_val[piece.color]][(Piece.piece_type_val[piece.type] +2 )%3]:
              if teammate.adjacent_to(piece.row, piece.col):
              	score += teammate_value * (1 if piece.color == 'WHITE' else -1)
                
            #How close are you to the center 
            score += center_encouragement_value * (        (      ((float(Board.rows-1)/2 )**2 + (float(Board.cols-1)/2 )**2)    - ((float(Board.rows-1)/2 - piece.row)**2 +(float(Board.cols-1)/2-piece.col)**2)    )/40.5) * (1 if piece.color == 'WHITE' else -1)
            


            
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
            return False

    def draw(self):
        return self.position_counter[self.current_hash] >=3
    
    def switch_turn(self): 
        self.whitetomove = not self.whitetomove
    

                
    def update(self, source, dest):
        piece = self.board_coord[source[0]][source[1]]


        self.undo_hash(piece)
        piece.update_piece(source,dest)
        self.update_hash(piece)
        self.position_counter[self.current_hash] +=1

        
        self.fear_update(piece)
        self.switch_turn()


        self.previous_moves.append( [piece.color, piece.type, source[0], source[1], dest[0], dest[1]] )



    def undo_update(self, source, dest, old_infear_trapped):
        piece = self.board_coord[dest[0]][dest[1]]


        self.position_counter[self.current_hash] -=1
        self.undo_hash(piece)
        piece.update_piece(dest, source)
        self.update_hash(piece)


        counter = 0
        for piece in self.all_pieces():
            piece.infear = old_infear_trapped[counter][0]
            piece.trapped = old_infear_trapped[counter][1]
            counter +=1
        self.switch_turn()


        self.previous_moves.pop( -1)


    def send_updated_data(self):
        return [self.whitetomove  ,  [ piece.send_updated_data() for piece in self.all_pieces()] , self.previous_moves]
            
        
##########################################       
class AI:

    def __init__(self, watering_holes_value,future_watering_hole_value , adjacent_watering_holes_value, scared_pieces_value, teammate_value,center_encouragement_value):
        self.watering_holes_value = watering_holes_value
        self.future_watering_hole_value = future_watering_hole_value
        self.adjacent_watering_holes_value = adjacent_watering_holes_value
        self.scared_pieces_value = scared_pieces_value 
        self.teammate_value = teammate_value
        self.center_encouragement_value = center_encouragement_value
        self.recurse = 3
        
        
    def receive_data(self, whitetomove, pieces, previous_moves):
  
        
        self.board = Board(whitetomove, pieces, previous_moves)
        
        self.board_position_base_score   = {}
        
        self.board_position_black_recurse = {}
        self.board_position_black_score = {}
        self.board_position_black_move  = {}
        
        
        self.board_position_white_recurse = {}
        self.board_position_white_score = {}
        self.board_position_white_move = {}
        
        self.execute()
      
    def execute(self):
        if (not self.board.victory() and not self.board.draw()):
        
            self.ai_move= (self.AI_alpha_beta(self.recurse))[0:2]
            self.board.update(self.ai_move[0], self.ai_move[1])
            

    def send_updated_data(self):
        return self.board.send_updated_data() 

    def AI_alpha_beta(self, recurse,alpha =-1000000000.0, beta = 1000000000.0 ):

        draw = self.board.draw()
        if draw:
            return [None, None, 0]

        
        victory = self.board.victory()
        if victory:
            return [None, None, 1000000 * (1 if victory== 'WHITE' else -1) ]


        if recurse == 0:
            if self.board.current_hash  in self.board_position_base_score:
                return [None, None, self.board_position_base_score[self.board.current_hash]]


            score = self.board.board_evaluation(self.watering_holes_value,self.future_watering_hole_value, self.adjacent_watering_holes_value, self.scared_pieces_value, self.teammate_value, self.center_encouragement_value)
            self.board_position_base_score[self.board.current_hash] = score
            return [None, None, score]



        if (self.board.whitetomove):
            if self.board.current_hash in self.board_position_white_recurse\
            			and recurse <= self.board_position_white_recurse[self.board.current_hash]:
                return self.board_position_white_move[self.board.current_hash] + [self.board_position_white_score[self.board.current_hash]]
        		
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
                            
            self.board_position_white_recurse[self.board.current_hash] = recurse
            self.board_position_white_move[self.board.current_hash] =  [current_best_source, current_best_dest]
            self.board_position_white_score[self.board.current_hash] =   current_best_score
            return [current_best_source, current_best_dest, current_best_score]



        else:
        
            if self.board.current_hash in self.board_position_black_recurse\
            			and recurse <= self.board_position_black_recurse[self.board.current_hash]:
                  return self.board_position_black_move[self.board.current_hash] + [self.board_position_black_score[self.board.current_hash]]
        
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
                            
            self.board_position_black_recurse[self.board.current_hash] = recurse
            self.board_position_black_move[self.board.current_hash] =  [current_worst_source, current_worst_dest]
            self.board_position_black_score[self.board.current_hash] =   current_worst_score
            return [current_worst_source, current_worst_dest, current_worst_score]



##########################################
class Backend:
    def __init__(self, watering_holes_value = [0,20,80,1000000],future_watering_hole_value = [0,5,20,250000], adjacent_watering_holes_value = 5, scared_pieces_value = 5,teammate_value =3,   center_encouragement_value = .4):
        self.watering_holes_value =  watering_holes_value 
        self.future_watering_hole_value = future_watering_hole_value
        self.adjacent_watering_holes_value = adjacent_watering_holes_value
        self.scared_pieces_value = scared_pieces_value
        self.teammate_value = teammate_value
        self.center_encouragement_value = center_encouragement_value
        self.AI = AI(self.watering_holes_value,self.future_watering_hole_value , self.adjacent_watering_holes_value, self.scared_pieces_value, self.teammate_value, self.center_encouragement_value)


    def receive_data(self, whitetomove, pieces, previous_moves = [ ] ):
        self.AI.receive_data(whitetomove,pieces, previous_moves)



    def send_updated_data(self):
        updated_data = self.AI.send_updated_data()
        return updated_data

if __name__ == "__main__":
    false = False
    backend = Backend()
    backend.receive_data(
            false,[["BLACK","ELEPHANT",2,2,false,false],
            ["BLACK","ELEPHANT",0,5,false,false],
            ["BLACK", "LION", 3, 5, false, false],
            ["BLACK", "MOUSE", 4, 2, false, false],
            ["BLACK", "MOUSE", 1, 5, false, false],
            ["BLACK", "LION", 2, 5, false, false],
            ["WHITE", "LION", 6, 1, false, false],
            ["WHITE", "MOUSE", 8, 4, false, false],
            ["WHITE", "MOUSE", 8, 5, false, false],
            ["WHITE", "LION", 2, 0, false, false],
            ["WHITE", "ELEPHANT", 9, 4, false, false],
            ["WHITE", "ELEPHANT", 9, 5, false, false]],
            [["WHITE", "LION", 8, 6, 7, 7],
            ["BLACK", "LION", 1, 6, 2, 5],
            ["WHITE", "LION", 7, 7, 3, 3],
            ["BLACK", "LION", 1, 3, 3, 5],
            ["WHITE", "LION", 3, 3, 2, 4],
            ["BLACK", "MOUSE", 1, 4, 1, 2],
            ["WHITE", "LION", 2, 4, 0, 2],
            ["BLACK", "MOUSE", 1, 2, 4, 2],
            ["WHITE", "LION", 8, 3, 6, 1],
            ["BLACK", "ELEPHANT", 0, 4, 1, 3],
            ["WHITE", "LION", 0, 2, 2, 0],
            ["BLACK", "ELEPHANT", 1, 3, 3, 1],
            ["WHITE", "LION", 2, 0, 1, 1],
            ["BLACK", "ELEPHANT", 3, 1, 2, 2],
            ["WHITE", "LION", 1, 1, 2, 0],
            ["BLACK", "ELEPHANT", 2, 2, 3, 1],
            ["WHITE", "LION", 2, 0, 1, 1],
            ["BLACK", "ELEPHANT", 3, 1, 2, 2],
            ["WHITE", "LION", 1, 1, 2, 0],
            ["BLACK", "ELEPHANT", 2, 2, 3, 1],
            ["WHITE", "LION", 2, 0, 1, 1],
            ["BLACK", "ELEPHANT", 3, 1, 2, 2],
            ["WHITE", "LION", 1, 1, 2, 0],
            ["BLACK", "ELEPHANT", 2, 2, 3, 1],
            ["WHITE", "LION", 2, 0, 1, 1],
            ["BLACK", "ELEPHANT", 3, 1, 2, 2],
            ["WHITE", "LION", 1, 1, 2, 0]])
