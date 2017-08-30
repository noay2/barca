import time
import math
import random
import copy
from collections import defaultdict
from collections import OrderedDict
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
        for piece in pieces: Piece(piece, self.board_coord, self.pieces)
        self.previous_moves = defaultdict(int, previous_moves)
        self.current_hash = self.initial_hash()


    def initial_hash(self):
        string = ''
        for piece in self.all_pieces():
            string += str(piece.row)+ str(piece.col)
        return string          

    def update_hash(self):
        string = ''
        for piece in self.all_pieces():
            string += str(piece.row)+ str(piece.col)
        self.current_hash = string
        
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
            score += center_encouragement_value * (          ((float(Board.rows-1)/2 )**2 + (float(Board.cols-1)/2 )**2) - ((float(Board.rows-1)/2 - piece.row)**2 +(float(Board.cols-1)/2-piece.col)**2)        )/((float(Board.rows-1)/2 )**2 + (float(Board.cols-1)/2 )**2) * (1 if piece.color == 'WHITE' else -1)
            


            
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
        return self.previous_moves[self.current_hash] >=3
    
    def switch_turn(self): 
        self.whitetomove = not self.whitetomove
    

                
    def update(self, source, dest):
        piece = self.board_coord[source[0]][source[1]]
        piece.update_piece(source,dest)
        self.update_hash()

        
        self.fear_update(piece)
        self.switch_turn()


        self.previous_moves[self.current_hash] +=1




    def undo_update(self, source, dest, old_infear_trapped):
        self.previous_moves[self.current_hash] -=1


        piece = self.board_coord[dest[0]][dest[1]]
        piece.update_piece(dest, source)
        self.update_hash()


        counter = 0
        for piece in self.all_pieces():
            piece.infear = old_infear_trapped[counter][0]
            piece.trapped = old_infear_trapped[counter][1]
            counter +=1          
        self.switch_turn()




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

        self.board_position_dict      = OrderedDict()
        
    def receive_data(self, whitetomove, pieces, previous_moves, temp_recurse):
  
        
        self.board = Board(whitetomove, pieces, previous_moves)
        self.execute(temp_recurse)
	
      
    def execute(self, temp_recurse):
        if (not self.board.victory() and not self.board.draw()):
        
            self.ai_move= (self.AI_alpha_beta(temp_recurse))[0:2]
            self.board.update(self.ai_move[0], self.ai_move[1])
            

    def send_updated_data(self):
        return self.board.send_updated_data()


    def AI_alpha_beta(self, recurse,alpha =-1000000000.0, beta = 1000000000.0 ):

        ai_board_hash = self.board.current_hash + str(int(self.board.whitetomove))

        draw = self.board.draw()
        if draw:
            return [None, None, 0]

        
        victory = self.board.victory()
        if victory:
            return [None, None, 1000000 * (1 if victory== 'WHITE' else -1) ]
        
        if ai_board_hash in self.board_position_dict:
            data = self.board_position_dict.pop(ai_board_hash)
            if recurse <= data[0]:
                self.board_position_dict[ai_board_hash] = data
                return data[1:]

        if recurse == 0: 
            score = self.board.board_evaluation(self.watering_holes_value,self.future_watering_hole_value, self.adjacent_watering_holes_value, self.scared_pieces_value, self.teammate_value, self.center_encouragement_value)

            self.board_position_dict[ai_board_hash] = [recurse, None, None,score]
            if len(self.board_position_dict) == 10000: self.board_position_dict.popitem()
            
            return [None, None, score]



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

            self.board_position_dict[ai_board_hash] = [recurse, current_best_source, current_best_dest,current_best_score]
            if len(self.board_position_dict) == 10000: self.board_position_dict.popitem()                           

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
                            
            self.board_position_dict[ai_board_hash] = [recurse, current_worst_source, current_worst_dest,current_worst_score]
            if len(self.board_position_dict) == 10000: self.board_position_dict.popitem()                           

            return [current_worst_source, current_worst_dest, current_worst_score]




        



##########################################
class Backend:
    def __init__(self, watering_holes_value = [0,20,80,1000000],future_watering_hole_value = [0,5,20,400], adjacent_watering_holes_value = 5, scared_pieces_value = 5,teammate_value =3,   center_encouragement_value = .4):
        self.watering_holes_value =  watering_holes_value 
        self.future_watering_hole_value = future_watering_hole_value
        self.adjacent_watering_holes_value = adjacent_watering_holes_value
        self.scared_pieces_value = scared_pieces_value
        self.teammate_value = teammate_value
        self.center_encouragement_value = center_encouragement_value
        self.AI = AI(self.watering_holes_value,self.future_watering_hole_value , self.adjacent_watering_holes_value, self.scared_pieces_value, self.teammate_value, self.center_encouragement_value)


    def receive_data(self, whitetomove, pieces, previous_moves = {}, temp_recurse = 3 ):
        self.AI.receive_data(whitetomove,pieces, previous_moves, temp_recurse)



    def send_updated_data(self):
        updated_data = self.AI.send_updated_data()
        return updated_data

if __name__ == "__main__":
    backend = Backend()
    backend.receive_data(True, \
     [
     ["BLACK","ELEPHANT",9,4,True,False],
     ["BLACK","ELEPHANT",9,5,False,False],
     ["BLACK","MOUSE",8,4,False,False],
     ["BLACK","MOUSE",8,5,False,False],
     ["BLACK","LION",8,6,False,False],
     ["BLACK","LION",8,3,False,False],
     ["WHITE","MOUSE",1,4,False,False],
     ["WHITE","MOUSE",1,5,False,False],
     ["WHITE","LION",1,6,False,False],
     ["WHITE","LION",1,3,False,False],
     ["WHITE","ELEPHANT",0,4,False,False],
     ["WHITE","ELEPHANT",0,5,False,False]
     ])

