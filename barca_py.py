import time
import random
import copy

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
    
    def __init__(self, piece_arr, board, team_pieces,piece_type,scared_of_pieces):
        self.color   = piece_arr[0]
        self.type    = piece_arr[1]
        self.row     = piece_arr[2]
        self.col     = piece_arr[3]
        self.infear  = piece_arr[4]
        self.trapped = piece_arr[5]
        self.board = board
        self.board[self.row][self.col]  = self
        self.piece_type = piece_type
        self.piece_type.add(self)
        self.piece_type_directions = Piece.piece_type_direction[self.type]
        self.team_pieces = team_pieces
        self.team_pieces.append(self)
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
    piece_type_direction = {"MOUSE": [ [i,j] for j in range(-1,2,1) for i in range(-1,2,1) if (abs(i) ==abs(j) )       and not(i==0 and j==0)   ],
                            "LION":  [ [i,j] for j in range(-1,2,1) for i in range(-1,2,1) if (i==0 or j==0 )and not(i==0 and j==0)   ],
                            "ELEPHANT":[[i,j]for j in range(-1,2,1) for i in range(-1,2,1) if                    not(i==0 and j==0)   ]
                            }

    
    def __init__(self,whitetomove, pieces,watering_holes_value, adjacent_watering_holes_value, scared_pieces_value, center_encouragement_value):
        piece_array = [[set() for j in range(3)]for i in range(2)]
        self.whitetomove = whitetomove
        self.board = [[None for j in range(10)] for i in range(10) ]
        self.black_pieces = []
        self.white_pieces = []
        for piece in pieces:
                piece_instance = Piece(piece, self.board,self.black_pieces if piece[0] == "BLACK" else self.white_pieces,
                piece_array[Board.piece_color_val[piece[0]] ][Board.piece_type_val[piece[1]]],
                piece_array[(Board.piece_color_val[piece[0]] + 1)%2][(Board.piece_type_val[piece[1]] + 1)%3])
        self.white_pieces_on_watering_holes = 0
        self.black_pieces_on_watering_holes = 0


        self.score = 0
        self.watering_holes_value = watering_holes_value
        self.adjacent_watering_holes_value = adjacent_watering_holes_value
        self.scared_pieces_value = scared_pieces_value
        self.center_encouragement_value = center_encouragement_value


        self.hash_number = self.initial_hash()
        self.positions_counter = {}
        self.positions = {}

        
        self.initial_board_evaluation()
        self.add_position()


    def initial_hash(self):
        number = 0
        for piece in self.all_pieces():
            number   +=  ( Piece.piece_color_val[piece.color] * 3 + Piece.piece_type_val[piece.type] +1   ) *  (8  **  (piece.row * 10 + piece.col))
        return number

    def undo_hash(self, color, ptype,row,col,number):
        return  number- ( Piece.piece_color_val[color] * 3 + Piece.piece_type_val[ptype] +1   ) *  (8  **  (row * 10 + col))

    def update_hash(self, color, ptype,row,col,number):
        return number + ( Piece.piece_color_val[color] * 3 + Piece.piece_type_val[ptype] +1   ) *  (8  **  (row * 10 + col))
         
    def add_position(self):
        if self.hash_number in self.positions_counter:
            self.positions_counter[self.hash_number] +=1

        else:
            self.positions_counter[self.hash_number] = 1
            self.positions[self.hash_number] =  [self.score ,
                                                [self.white_pieces_on_watering_holes, self.black_pieces_on_watering_holes],
                                                [ (piece.infear, piece.trapped) for piece in self.all_pieces()]]

    def remove_position(self):
        self.positions_counter[self.hash_number]  -= 1


    def recover_fear(self):
        self.fear_information = self.positions[self.hash_number][2]
        for index, piece in enumerate(self.all_pieces()):
            piece.infear = self.fear_information[index][0]
            piece.trapped = self.fear_information[index][1]

    def recover_score(self):
        stuff = self.positions[self.hash_number]
        self.score = stuff[0]
        self.white_pieces_on_watering_holes =  stuff[1][0]
        self.black_pieces_on_watering_holes =  stuff[1][1]

        
        
    def initial_board_evaluation(self):

##        #Is this already a tied game??
##        if self.hash_number in self.positions_counter.keys():
##            if self.positions_counter[self.hash_number] >= 5:
##                self.score = 0
##                return
            

        for piece in self.all_pieces():
                
            #How many watering holes you have
            if (piece.row, piece.col) in Board.watering_holes:
                if piece.color == "WHITE":
                    self.score -= self.watering_holes_value[self.white_pieces_on_watering_holes]
                    self.white_pieces_on_watering_holes += 1
                    self.score += self.watering_holes_value[self.white_pieces_on_watering_holes]
                    
                elif piece.color == "BLACK":
                    self.score += self.watering_holes_value[self.black_pieces_on_watering_holes]
                    self.black_pieces_on_watering_holes += 1
                    self.score -= self.watering_holes_value[self.black_pieces_on_watering_holes]
                        
            #Are you next to a watering hole:
            for watering_hole_row, watering_hole_col in Board.watering_holes:
                if piece.adjacent_to(watering_hole_row, watering_hole_col):
                    self.score += self.adjacent_watering_holes_value * (1 if piece.color == 'WHITE' else -1)
                    
            #How close are you to the center 
            self.score += self.center_encouragement_value * (        (40.5 - ((4.5 - piece.row)**2 +(4.5-piece.col)**2    ))/40.5) * (1 if piece.color == 'WHITE' else -1)
        
            #How many pieces do you have in fear
            if piece.infear:
                self.score -=self.scared_pieces_value * (1 if piece.color == 'WHITE' else -1)
            

        
    def remove_piece_board_evaluation(self,piece):

        #How many watering holes you have
        if (piece.row, piece.col)  in Board.watering_holes:
                if piece.color == "WHITE":
                    self.score -= self.watering_holes_value[self.white_pieces_on_watering_holes]
                    self.white_pieces_on_watering_holes -= 1
                    self.score += self.watering_holes_value[self.white_pieces_on_watering_holes]
                    
                elif piece.color == "BLACK":
                    self.score += self.watering_holes_value[self.black_pieces_on_watering_holes]
                    self.black_pieces_on_watering_holes -= 1
                    self.score -= self.watering_holes_value[self.black_pieces_on_watering_holes]


        #Are you next to a watering hole:
        for watering_hole_row, watering_hole_col in Board.watering_holes:                           
            if piece.adjacent_to(watering_hole_row, watering_hole_col):
                self.score -= self.adjacent_watering_holes_value * (1 if piece.color == 'WHITE' else -1)

                
        #How close are you to the center 
        self.score -= self.center_encouragement_value * (        (40.5 - ((4.5 - piece.row)**2 +(4.5-piece.col)**2    ))/40.5) * (1 if piece.color == 'WHITE' else -1)
    
        #How many pieces do you have in fear
        for piece in self.all_pieces():
            if piece.infear:
                self.score +=self.scared_pieces_value * (1 if piece.color == 'WHITE' else -1)
        

        

                
    def update_board_evaluation(self,piece):


        #Is this already a tied game??
        if self.hash_number in self.positions_counter.keys():
            if self.positions_counter[self.hash_number] >= 5:
                self.score = 0
                return


        #How many watering holes you have:
        if (piece.row, piece.col) in Board.watering_holes:
            if piece.color == 'WHITE':
                self.score -= self.watering_holes_value[self.white_pieces_on_watering_holes]
                self.white_pieces_on_watering_holes += 1
                self.score += self.watering_holes_value[self.white_pieces_on_watering_holes]

            elif piece.color == "BLACK":
                self.score += self.watering_holes_value[self.black_pieces_on_watering_holes]
                self.black_pieces_on_watering_holes += 1
                self.score -= self.watering_holes_value[self.black_pieces_on_watering_holes]

        #Are you next to a watering hole:               
        for watering_hole_row, watering_hole_col in Board.watering_holes:
            if piece.adjacent_to(watering_hole_row, watering_hole_col):
                self.score += self.adjacent_watering_holes_value * (1 if piece.color == 'WHITE' else -1)
                
        #How close are you to the center 
        self.score += self.center_encouragement_value * (        (40.5 - ((4.5 - piece.row)**2 +(4.5-piece.col)**2    ))/40.5) * (1 if piece.color == 'WHITE' else -1)

        #How many pieces do you have in fear
        for piece in self.all_pieces():
            if piece.infear:
                self.score -=self.scared_pieces_value * (1 if piece.color == 'WHITE' else -1)
               


    
                                                
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

                
                
    def fear_update(self,moving_piece):
        for piece in self.all_pieces():
            if (piece.infear) or (piece.infear_of(moving_piece)) :
                piece.modify_fear()

        
    def switch_turn(self): 
        self.whitetomove = not self.whitetomove
    

                
    def update(self, source, dest):
        piece = self.board[source[0]][source[1]]
        temp_undo_hash = self.undo_hash(piece.color,piece.type,source[0],source[1],self.hash_number)
        temp_redo_hash = self.update_hash(piece.color,piece.type,dest[0],dest[1],temp_undo_hash)



        
        if temp_redo_hash in self.positions:
            self.reoccuring_update(temp_undo_hash,temp_redo_hash, source, dest)

        else:
            self.new_update(temp_undo_hash,temp_redo_hash, source, dest)



    def new_update(self,temp_undo_hash,temp_redo_hash, source, dest):
        piece = self.board[source[0]][source[1]]


        self.remove_piece_board_evaluation(piece)
        self.hash_number = temp_undo_hash
        self.board[source[0]][source[1]] = None
        piece.row = None
        piece.col = None

        piece.row = dest[0]
        piece.col = dest[1]
        self.board[dest[0]][dest[1]] = piece
        self.hash_number = temp_redo_hash


        self.fear_update(piece)        
        self.update_board_evaluation(piece)
        self.switch_turn()



        self.add_position()


    def reoccuring_update(self, temp_undo_hash  ,temp_redo_hash, source, dest):
        piece = self.board[source[0]][source[1]]



        self.hash_number = temp_undo_hash
        self.board[source[0]][source[1]] =None
        piece.row = None
        piece.col = None

        
        piece.row = dest[0]
        piece.col = dest[1]
        self.board[dest[0]][dest[1]] = piece
        self.hash_number = temp_redo_hash

        
        self.recover_fear()
        self.recover_score()
        self.switch_turn()


        self.add_position()


        
    def undo_update(self, source, dest):
        piece = self.board[dest[0]][dest[1]]


        self.remove_position()

        
        self.hash_number = self.undo_hash(piece.color, piece.type, piece.row, piece.col,self.hash_number)
        self.board[dest[0]][dest[1]] = None
        piece.row = None
        piece.col = None

        
        piece.row = source[0]
        piece.col = source[1]
        self.board[source[0]][source[1]] = piece
        self.hash_number = self.update_hash(piece.color, piece.type, piece.row, piece.col,self.hash_number)

        
        self.recover_fear()
        self.recover_score()
        self.switch_turn()


    def check_victory(self):
        return (self.white_pieces_on_watering_holes >= 3 )or (self.black_pieces_on_watering_holes >= 3)
    
    def check_draw(self):
        return self.positions_counter[self.hash_number] >= 5
        

    def send_updated_data(self):
        return [self.whitetomove ]+ [[ piece.send_updated_data() for piece in self.all_pieces()]]
            
        
##########################################       
class AI:

    def __init__(self,whitetomove, pieces,human_move,watering_holes_value, adjacent_watering_holes_value, scared_pieces_value, center_encouragement_value):
        self.board = Board(whitetomove, pieces,watering_holes_value, adjacent_watering_holes_value, scared_pieces_value, center_encouragement_value)
        self.human_move = human_move
        self.ai_move = [None, None]
        self.recurse = 3
                                  
    def AI_alpha_beta(self, recurse,alpha =-1000000000.0, beta = 1000000000.0 ):
        if recurse == 0 or self.board.check_victory() or self.board.check_draw() :
            return  [None, None,self.board.score]

        else:
            if (self.board.whitetomove):
                current_best_source,current_best_dest,current_best_score   = None,None,-1000000000.0
                for piece in self.board.current_pieces():
                    for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                        self.board.update([source_row, source_col], [dest_row, dest_col])
                        childs_worst_source, childs_worst_dest, childs_worst_score= self.AI_alpha_beta(  recurse-1,alpha, beta)
                        self.board.undo_update( [source_row, source_col],[dest_row, dest_col])
                        if  childs_worst_score> current_best_score:
                            current_best_source,current_best_dest,current_best_score = [source_row, source_col],[dest_row, dest_col ],childs_worst_score
                            alpha = max(alpha, childs_worst_score)
                            if (alpha>beta):
                                return [current_best_source, current_best_dest, current_best_score]

                            
                return [current_best_source, current_best_dest, current_best_score]



            else:
                current_worst_source,current_worst_dest,current_worst_score   = None,None,1000000000.0
                for piece in self.board.current_pieces():
                    for source_row, source_col, dest_row, dest_col in piece.valid_moves():
                        self.board.update([source_row, source_col], [dest_row, dest_col])
                        childs_best_source, childs_best_dest, childs_best_score = self.AI_alpha_beta(  recurse-1,alpha, beta)
                        self.board.undo_update( [source_row, source_col],[dest_row, dest_col])
                        if  childs_best_score< current_worst_score:
                            current_worst_source,current_worst_dest,current_worst_score = [source_row, source_col],[dest_row, dest_col ],childs_best_score
                            beta = min(beta, childs_best_score)
                            if (alpha>beta):
                                return [current_worst_source, current_worst_dest, current_worst_score]

                            
                return [current_worst_source, current_worst_dest, current_worst_score]


    def execute(self):
        if (not self.board.check_victory()):
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
##########################################

def printboard(board):
    for col in range(0,10):
        for i in range(0,4):
            print()
            for row in range(0,10):
                if(board[col][row]==None):
                    if (col+row)%2==0:
                        print('------', end='')
                    else:
                        print('      ', end='')
                elif (board[col][row].color=="WHITE" and board[col][row].type=="ELEPHANT"):
                    if(i==0):
                        print("/()()\\", end='')
                    elif(i==1):
                        print("/ || \\", end='')
                    elif(i==2):
                        print("  ||  ", end='')
                    elif(i==3):
                        print("WHITE ", end='')
                elif (board[col][row].color=="BLACK" and board[col][row].type=="ELEPHANT"):
                    if(i==0):
                        print("/()()\\", end='')
                    elif(i==1):
                        print("/ || \\", end='')
                    elif(i==2):
                        print("  ||  ", end='')
                    elif(i==3):
                        print("BLACK ", end='')
                elif (board[col][row].color=="BLACK" and board[col][row].type=="MOUSE"):
                    if(i==0):
                        print("      ", end='')
                    elif(i==1):
                        print(" ^.^  ", end='')
                    elif(i==2):
                        print("      ", end='')
                    elif(i==3):
                        print("BLACK ", end='')
                elif (board[col][row].color=="WHITE" and board[col][row].type=="MOUSE"):
                    if(i==0):
                        print("      ", end='')
                    elif(i==1):
                        print(" ^.^  ", end='')
                    elif(i==2):
                        print("      ", end='')
                    elif(i==3):
                        print("WHITE ", end='')
                elif (board[col][row].color=="BLACK" and board[col][row].type=="LION"):
                    if(i==0):
                        print("<^^^^>", end='')
                    elif(i==1):
                        print("<O  O>", end='')
                    elif(i==2):
                        print(" <--> ", end='')
                    elif(i==3):
                        print("BLACK ", end='')
                elif (board[col][row].color=="WHITE" and board[col][row].type=="LION"):
                    if(i==0):
                        print("<^^^^>", end='')
                    elif(i==1):
                        print("<O  O>", end='')
                    elif(i==2):
                        print(" <--> ", end='')
                    elif(i==3):
                        print("WHITE ", end='')




##
##    j  = time.time()
##    backend = Backend()
##    backend.receive_data(True, [['BLACK', 'ELEPHANT', 9, 4, False, False],
##                                                                   ['BLACK', 'ELEPHANT', 9, 5, False, False],
##                                                                   ['BLACK', 'MOUSE', 4, 4, False, False],
##                                                                   ['BLACK', 'MOUSE', 4, 5, False, False],
##                                                                   ['BLACK', 'LION', 8, 3, False, False],
##                                                                   ['BLACK', 'LION', 8, 6, False, False],
##                                                                   ['WHITE', 'ELEPHANT', 0, 4, False, False],
##                                                                   ['WHITE', 'ELEPHANT', 0, 5, False, False],
##                                                                   ['WHITE', 'MOUSE', 1, 4, False, False],
##                                                                   ['WHITE', 'MOUSE', 1, 5, False, False],
##                                                                   ['WHITE', 'LION', 1, 3, False, False],
##                                                                   ['WHITE', 'LION', 1, 6, False, False]], [[1,3], [3,5]])
##
##    print(backend.send_updated_data())
##
##
##    for i in backend.AI.board.board:
##        print(i)
##    print()
##    output = backend.send_updated_data()
##    backend.receive_data(True, [['WHITE', 'ELEPHANT', 0, 4, False, False],
##                         ['WHITE', 'ELEPHANT', 0, 5, False, False],
##                         ['WHITE', 'LION', 1, 3, False, False],
##                         ['WHITE', 'MOUSE', 1, 5, False, False],
##                         ['WHITE', 'LION', 1, 6, False, False],
##                         ['WHITE', 'MOUSE', 1, 4, True, False],
##                         ['BLACK', 'LION', 5, 3, False, False],
##                         ['BLACK', 'LION', 7, 4, False, False],
##                         ['BLACK', 'MOUSE', 8, 4, False, False],
##                         ['BLACK', 'MOUSE', 8, 5, False, False],
##                         ['BLACK', 'ELEPHANT', 9, 4, False, False],
##                         ['BLACK', 'ELEPHANT', 9, 5, False, False]],[[1,3], [3,5]])
##
##    output = backend.send_updated_data()
##    print(output)
##    backend.receive_data(True,
##                                                                     [['BLACK', 'ELEPHANT', 9, 5, False, False],
##                                                                   ['BLACK', 'MOUSE', 8, 4, False, False],
##                                                                   ['BLACK', 'MOUSE', 5, 5, False, False],
##                                                                   ['BLACK', 'LION', 8, 3, False, False],
##                                                                   ['BLACK', 'LION', 8, 6, False, False],
##                                                                   ['WHITE', 'ELEPHANT', 0, 4, False, False],
##                                                                   ['WHITE', 'ELEPHANT', 0, 5, False, False],
##                                                                   ['WHITE', 'MOUSE', 1, 4, False, False],
##                                                                   ['WHITE', 'MOUSE', 1, 5, False, False],
##                                                                   ['WHITE', 'LION', 1, 3, False, False],
##                                                                   ['WHITE', 'LION', 1, 6, False, False]],[[1,3], [3,5]])
##
##
##    for i in backend.AI.board.board:
##        print(i)
##    print()
##    output = backend.send_updated_data()
##    print(time.time() -j)
 
def match(eval_vector2):
    eval_vector=[20, 100, 5, 5, 0 ,1]
    vector1score=0
    vector2score=0
    backend = Backend(eval_vector[0:2], eval_vector[2], eval_vector[3], eval_vector[4])
    backend.receive_data(True,[["WHITE","MOUSE",1,4,False,False],
     ["BLACK","ELEPHANT",9,4,True,False],
     ["BLACK","ELEPHANT",9,5,False,False],
     ["BLACK","MOUSE",8,4,False,False],
     ["BLACK","MOUSE",8,5,False,False],
     ["BLACK","LION",8,6,False,False],
     ["BLACK","LION",8,3,False,False],
     ["WHITE","LION",1,6,False,False],
     ["WHITE","MOUSE",1,5,False,False],
     ["WHITE","LION",1,3,False,False],
     ["WHITE","ELEPHANT",0,4,False,False],
     ["WHITE","ELEPHANT",0,5,False,False]],
     [[9,3],[9,4]])
    
    backend1= Backend(eval_vector2[0:2], eval_vector2[2], eval_vector2[3], eval_vector2[4])
    while(True):
        temp=backend.send_updated_data()
        color=backend1.receive_data(temp[0], temp[1], temp[2])
        #printboard(backend.AI.board.board)
        if color=="WHITE":
            vector1score+=1
            break
        elif color=="BLACK":
            vector2score+=1
            break
        elif color=="DRAW":
            vector1score+=0.5
            vector2score+=0.5
            break
        temp=backend1.send_updated_data()
        color=backend.receive_data(temp[0], temp[1], temp[2])
        if color=="WHITE":
            vector1score+=1
            break
        elif color=="BLACK":
            vector2score+=1
            break
        elif color=="DRAW":
            vector1score+=0.5
            vector2score+=0.5
            break
        #printboard(backend1.AI.board.board)
        #print("\n\n")
    printboard(backend.AI.board.board)
    print("\n\n")
    printboard(backend1.AI.board.board)

    backend = Backend(eval_vector2[0:2], eval_vector2[2], eval_vector2[3], eval_vector2[4])
    backend.receive_data(True,[["WHITE","MOUSE",1,4,False,False],
     ["BLACK","ELEPHANT",9,4,True,False],
     ["BLACK","ELEPHANT",9,5,False,False],
     ["BLACK","MOUSE",8,4,False,False],
     ["BLACK","MOUSE",8,5,False,False],
     ["BLACK","LION",8,6,False,False],
     ["BLACK","LION",8,3,False,False],
     ["WHITE","LION",1,6,False,False],
     ["WHITE","MOUSE",1,5,False,False],
     ["WHITE","LION",1,3,False,False],
     ["WHITE","ELEPHANT",0,4,False,False],
     ["WHITE","ELEPHANT",0,5,False,False]],
     [[9,3],[9,4]])
    
    eval_vector[1]=50
    backend1= Backend(eval_vector[0:2], eval_vector[2], eval_vector[3], eval_vector[4])
    while(True):
        temp=backend.send_updated_data()
        color=backend1.receive_data(temp[0], temp[1], temp[2])
        #printboard(backend.AI.board.board)
        if color=="WHITE":
            vector2score+=1
            break
        elif color=="BLACK":
            vector1score+=1
            break
        elif color=="DRAW":
            vector1score+=0.5
            vector2score+=0.5
            break
        temp=backend1.send_updated_data()
        color=backend.receive_data(temp[0], temp[1], temp[2])
        if color=="WHITE":
            vector2score+=1
            break
        elif color=="BLACK":
            vector1score+=1
            break
        elif color=="DRAW":
            vector1score+=0.5
            vector2score+=0.5
            break
        #printboard(backend1.AI.board.board)
        #print("\n\n")
    printboard(backend.AI.board.board)
    printboard(backend1.AI.board.board)
    print("\n\n" + str(eval_vector) + "\nVS\n"+ str(eval_vector2))
    print(vector2score - vector1score)
    return vector2score - vector1score

def partial_derivative(func, dimension, delta, point):
    #Func take an n-dimensional vector as arugument, 0<=dimension<n, delta is a number, and point is an n-dimensional vector
    point2=copy.deepcopy(point)
    point2[dimension]*=delta
    return (func(point2)-func(point))/(point2[dimension]-point[dimension])

def gradient(func, delta, point):
    grad=[]
    for i in range(0,len(point)):
        grad.append(partial_derivative(func, i, delta, point))
    return grad

def descent(func, delta, rate, point):
    for j in range (0, 2):
        point1=[]
        grad=gradient(func, delta, point)
        #print("Function value: "+ str(func(point)))
        for i in range(0, len(point)):
            point1.append(point[i]+rate*grad[i])
        point=list(point1)
    print("\n\n")
    print(point)
    return point


if __name__ == "__main__":
    eval_vector=[20, 100, 5, 5, 0 ,1]
    eval_vector1=copy.deepcopy(eval_vector)
    eval_vector1[1]=50
    descent(match, 1.5, 0.1, eval_vector1)
    #print(match(eval_vector, eval_vector1))
    pass


"""
Elephants
/()()\
/ || \
WHITE
/()()\
/ || \
BLACK
 MICE
 
 ^.^
WHITE
   
 ^.^
BLACK
LION
z
"""










                    
