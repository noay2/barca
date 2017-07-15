import time
import math



##########################################
class Piece:
    def __init__(self, piece_arr):
        self.color   = piece_arr[0]
        self.type    = piece_arr[1]
        self.row     = piece_arr[2]
        self.col     = piece_arr[3]
        self.infear  = piece_arr[4]
        self.trapped = piece_arr[5]

    def __repr__(self):
        return "*" +self.color[0] +self.type[0]+"*"
    
    def scares(self, piece):
        if (  ((self.type == "ELEPHANT")and (piece.type == "LION"))\
            or ((self.type == "LION")   and (piece.type == "MOUSE"))\
            or ((self.type == "MOUSE")  and (piece.type == "ELEPHANT"))\
            ) and self.color != piece.color:
            return True
        else:
            return False


    def scared_of(self, piece):
        return piece.scares(self)


    def adjacent_squares(self,row,col,board):
        for rowt in range(row -1, row +2, 1):
            for colt in range(col -1, col +2, 1):
                if (rowt == row) and (colt == col):
                    pass
                elif (rowt <len(board)) and (rowt>=0) and (colt<len(board[0])) and (colt>=0):
                    yield [rowt, colt]

    def potential_infear(self,row,col,board):
        for square in self.adjacent_squares(row,col):
            piece = board[square[0]][square[1]]
            if (piece !=None) and (self.scared_of(piece)):
                return True
        return False

    
    def validmoves(self, board):
        if not(self.infear):
            for piece in self.Pieces:
                if piece.infear and (not piece.trapped) and (piece.color ==self.color):
                    return
        rowt = len(board)
        colt = len(board[0])
        for rowd in range(-1,2,1):
            for cold in range(-1,2,1):
                if (rowd ==0) and (cold==0):
                    pass
                elif ( (abs(cold) == abs(rowd)) and (self.type == "LION" or self.type == "ELEPHANT")) \
                   or (( (cold ==0) or (rowd==0)) and (self.type == "MOUSE" or self.type == "ELEPHANT")):
                    colt += cold
                    rowt += rowd
                    while (rowt >=0) and (rowt < len(board)) and\
                          (colt >=0) and    (colt<len(board[0])):
                        if (self.potential_infear(rowt,colt,board)) or self.trapped:
                            yield [rowt,colt]
                        rowt+=rowd
                        colt+=cold
                rowt = len(board)
                colt = len(board[0])
##########################################              
class Board:
     def __init__(self,whitetomove,humantomove, Pieces,source,dest):
        self.colors = ["BLACK", "WHITE"]
        self.types  = ["ELEPHANT", "MOUSE", "LION"]
        self.rows = 10                                  
        self.cols = 10
        self.init_piece_position =\
                [
                                    [self.rows -1,self.cols/2 -1], [self.rows -1,self.cols/2],[self.rows -2,self.cols/2 -1],
                                    [self.rows -2,self.cols/2 ],   [self.rows -2,self.cols/2 -2],[self.rows -2,self.cols/2 +1],
               
                                    [0,self.cols/2 -1],[0,self.cols/2], [1,self.cols/2 -1],
                                    [1,self.cols/2], [1,self.cols/2 -2], [1,self.cols/2 +1]
                 ]
        self.watering_holes      =\
                [
                                  [self.rows/2 -2, self.cols/2 -2],[self.rows/2 -2, self.cols/2 +1],
                                  [self.rows/2 +1, self.cols/2 -2],[self.rows/2 +1, self.cols/2 +1]
                                
                ]
        
        self.whitetomove = whitetomove
        self.humantomove = humantomove
        self.Pieces = Pieces
        self.board = [[None for j in range(10)] for i in range(10) ]
        for piece in self.Pieces:
            self.board[piece[2]][piece[3]]  = Piece(piece)
        self.piece = self.board[source][dest]
        
    def all_valid_moves(self):
        for piece in in self.Pieces:
            for validmoves in piece.validmoves():
                yield [piece.row, piece.col, validmoves[0], validmoves[1]]

    def update(self, source, dest):
        
        
        

    def check_score(self):
        pass
                
    def check_victory(self):
        white_counter = 0
        black_counter = 0
        for watering_hole in self.watering_holes:
            if (self.board[watering_hole[0]][watering_hole[1]]!= None):
                if (self.board[watering_hole[0]][watering_hole[1]]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
        if white_counter >= 3:
            return "WHITE"
        elif black_counter >=3:
            return "BLACK"
        else:
            return None
##########################################      
class Game(self):
    def __init__(self,whitetomove,humantomove, Pieces,source,dest):
        self.board = Board(whitetomove,humantomove, Pieces,source,dest)
        self.human_source      = source
        self.human_dest        = dest
##########################################
class Backend:
    def __init__(self):
        self.colors = ["BLACK", "WHITE"]
        self.types  = ["ELEPHANT", "MOUSE", "LION"]
        self.rows = 10                                  
        self.cols = 10
        self.init_piece_position =\
                [
                                    [self.rows -1,self.cols/2 -1], [self.rows -1,self.cols/2],[self.rows -2,self.cols/2 -1],
                                    [self.rows -2,self.cols/2 ],   [self.rows -2,self.cols/2 -2],[self.rows -2,self.cols/2 +1],
               
                                    [0,self.cols/2 -1],[0,self.cols/2], [1,self.cols/2 -1],
                                    [1,self.cols/2], [1,self.cols/2 -2], [1,self.cols/2 +1]
                 ]
        self.watering_holes      =\
                [
                                  [self.rows/2 -2, self.cols/2 -2],[self.rows/2 -2, self.cols/2 +1],
                                  [self.rows/2 +1, self.cols/2 -2],[self.rows/2 +1, self.cols/2 +1]
                                
                ]


    def send_new_data(self, whitetomove = True, humantomove = True, source = None, dest = None):
        Pieces = []
        counter = 0
        for color in self.colors:
            for type in self.types:
                for i in range(2):
                    Pieces.append([color,type, 
                        int(self.init_piece_position[counter][0]), int(self.init_piece_position[counter][1]),
                                  False, False])
                    counter +=1
        return [whitetomove, humantomove, Pieces, source, dest]
    

    def receive_data(self, whitetomove,humantomove, Pieces,source,dest):
        self.game = Game(whitetomove,humantomove, Pieces,source,dest)



    def send_updated_data(self):
        Pieces = []
        for row in self.game.board.board:
            for piece in row:
                if piece != None:
                    Pieces.append([piece.color, piece.type, piece.row, piece.col, piece.scared, piece.trapped])
        return [self.whitetomove, self.humantomove, Pieces, self.source, self.dest]


##########################################
class rest:
    def __init__(self):
        pass
