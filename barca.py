import time
import math
import copy
from  random     import randint
from collections import defaultdict
from collections import OrderedDict
from queue       import PriorityQueue
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

    
    def send_updated_data(self):

        return ([self.color, self.type, self.row, self.col, self.infear, self.trapped])       


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

    def update_piece(self, source, dest):
        self.row = dest[0]
        self.col = dest[1]
        self.board_coord[source[0]][source[1]] = None
        self.board_coord[dest[0]][dest[1]]     = self
##########################################              
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

    def send_updated_data(self):
        return [self.whitetomove  ,  [ piece.send_updated_data() for piece in self.all_pieces()] , self.previous_moves]
            
        
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
              for piece in sorted(piece_type,key = lambda piece: str(piece.row) + str(piece.col )):
                    yield piece
              

    def other_pieces(self):
          for piece_type in self.pieces[(self.whitetomove +1) %2 ]: 
              for piece in sorted(piece_type,key = lambda piece: str(piece.row) + str(piece.col )):
                    yield piece
                
    def all_pieces(self):
        for piece_color in self.pieces:
            for piece_type in piece_color: 
                for piece in sorted(piece_type,key = lambda piece: str(piece.row) + str(piece.col )):
                    yield piece

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
                            
        score += future_watering_hole_value[min(3,white_counter + 1)] * future_white_counter
        score -= future_watering_hole_value[min(3, black_counter + 1)] * future_black_counter
        


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



        for piece, counter in zip(self.all_pieces(), range(12)): piece.infear,piece.trapped = old_infear_trapped[counter][0], old_infear_trapped[counter][1]         
        self.switch_turn()


##########################################       
class AI:

    def __init__(self, watering_holes_value,future_watering_hole_value , adjacent_watering_holes_value, scared_pieces_value, teammate_value,center_encouragement_value):
        self.watering_holes_value = watering_holes_value
        self.future_watering_hole_value = future_watering_hole_value
        self.adjacent_watering_holes_value = adjacent_watering_holes_value
        self.scared_pieces_value = scared_pieces_value 
        self.teammate_value = teammate_value
        self.center_encouragement_value = center_encouragement_value
        self.easy_boards_dict = OrderedDict()
        self.medd_boards_dict = OrderedDict()
        self.hard_boards_dict = OrderedDict()

        
    def receive_data(self, whitetomove, pieces, previous_moves, recurse):
        self.board = Board(whitetomove, pieces, previous_moves)
        return self.execute(recurse)
      
    def execute(self, recurse):
        if (not self.board.victory() and not self.board.draw()):
            moves= self.AI_alpha_beta(recurse, recurse)
            move = self.decide_move_to_make(moves)
            self.board.update(move[0], move[1])
            
    

    def send_updated_data(self):
        return self.board.send_updated_data()



    def decide_move_to_make(self, moves):
        
        if not self.board.whitetomove:
            for move in moves:
                move[-1] *= -1


    
        moves.reverse()



        if moves[0][-1] <0 :
            const = moves[0][-1]
            for move in moves:
                move[-1] += const * -1


                
        for index in range(len(moves)):
            moves[index][-1] = moves[index][-1]  ** (index +1)  



        chances=[]
        counter=0
        for move in moves:
            chances.append(move[-1])
            counter+=move[-1]

        
        rand = randint(0, int(counter))
        temp=0
        for chance, move in zip(chances, moves):
            temp+=chance
            if (rand<temp):
                return move

            
        return moves[-1]
               
            
        

    def AI_alpha_beta(self,original_recurse, recurse,alpha =-1000000000.0, beta = 1000000000.0 ):

        draw = self.board.draw()
        if draw:
            return 0




        
        victory = self.board.victory()
        if victory:
            return self.watering_holes_value[3] * (1 if victory== 'WHITE' else -1) 
        

        values = self.retrieve_boards_dict(original_recurse, recurse)
        if values != None:
            if recurse == original_recurse:
                return values
            else:
                return values[0][-1]
                
        

        if recurse == 0:
            score = self.board.board_evaluation(self.watering_holes_value,self.future_watering_hole_value, self.adjacent_watering_holes_value, self.scared_pieces_value, self.teammate_value, self.center_encouragement_value)
            return score


    
        priority_queue = PriorityQueue()
        if (self.board.whitetomove):
            current_best_score   = -1000000000.0
            for piece in self.board.current_pieces():
                for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                    old_infear_trapped= [[piece.infear, piece.trapped] for piece in (self.board.all_pieces())]
                    self.board.update([source_row, source_col], [dest_row, dest_col])
                    childs_worst_score= self.AI_alpha_beta( original_recurse, recurse-1,alpha, beta)
                    priority_queue.put([-childs_worst_score, [[source_row, source_col],[dest_row, dest_col], childs_worst_score]])
                    self.board.undo_update( [source_row, source_col],[dest_row, dest_col],old_infear_trapped)
                    if  childs_worst_score> current_best_score:
                        current_best_score = childs_worst_score
                        alpha = max(alpha, childs_worst_score)
                        if (alpha>beta):
                            return priority_queue.get()[1][-1]
            values = [  priority_queue.get()[1]      for i in range(min(5, priority_queue.qsize())) ]
            self.update_boards_dict(values,original_recurse, recurse)
            if recurse == original_recurse:
                return values
            else:
                return values[0][-1]
            

        else:
            current_worst_score   = 1000000000.0
            for piece in self.board.current_pieces():
                for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                    old_infear_trapped = [[piece.infear, piece.trapped] for piece in (self.board.all_pieces())]
                    self.board.update([source_row, source_col], [dest_row, dest_col])
                    childs_best_score = self.AI_alpha_beta( original_recurse, recurse-1,alpha, beta)
                    priority_queue.put([childs_best_score,[ [source_row, source_col], [dest_row, dest_col], childs_best_score]])
                    self.board.undo_update( [source_row, source_col],[dest_row, dest_col],old_infear_trapped)
                    if  childs_best_score< current_worst_score:
                        current_worst_score = childs_best_score
                        beta = min(beta, childs_best_score)
                        if (alpha>beta):
                            return priority_queue.get()[1][-1]
            values = [  priority_queue.get()[1]      for i in range(min(5, priority_queue.qsize())) ]
            self.update_boards_dict(values,original_recurse, recurse)
            if recurse == original_recurse:
                return values
            else:
                return values[0][-1]

    def update_boards_dict(self, values, original_recurse, recurse):
        boards_dict = self.easy_boards_dict if original_recurse ==1 else self.medd_boards_dict if original_recurse == 2 else self.hard_boards_dict
        board_hash = self.board.current_hash + str(int(self.board.whitetomove))
        
        if board_hash in boards_dict:
            boards_dict.pop(board_hash)
        if len(boards_dict) > 1000000:
            boards_dict.popitem()
        boards_dict[board_hash] = (values, recurse)


    def retrieve_boards_dict(self, original_recurse, recurse):
        boards_dict = self.easy_boards_dict if original_recurse ==1 else self.medd_boards_dict if original_recurse == 2 else self.hard_boards_dict
        board_hash = self.board.current_hash + str(int(self.board.whitetomove))
        
        if board_hash in boards_dict:
            value, board_recurse = boards_dict[board_hash]
            if board_recurse >= recurse:
                return value
        return None
##########################################
class Backend:
    def __init__(self, watering_holes_value = [0,20,80,1000000],future_watering_hole_value = [0,5,20,400], adjacent_watering_holes_value = 5, scared_pieces_value = 5,teammate_value =3,   center_encouragement_value = .4):
        self.AI = AI(watering_holes_value,future_watering_hole_value , adjacent_watering_holes_value, scared_pieces_value, teammate_value, center_encouragement_value)

    def receive_data(self, whitetomove, pieces, previous_moves = {}, recurse = 3):
        return self.AI.receive_data(whitetomove,pieces, previous_moves, recurse)



    def send_updated_data(self):
        updated_data = self.AI.send_updated_data()
        return updated_data
