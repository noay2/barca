import time
import math



##########################################
class Piece:
    def __init__(self, piece_arr, board, pieces):
        self.color   = piece_arr[0]
        self.type    = piece_arr[1]
        self.row     = piece_arr[2]
        self.col     = piece_arr[3]
        self.infear  = piece_arr[4]
        self.trapped = piece_arr[5]
        self.board = board
        self.pieces = pieces

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


    def adjacent_squares(self,row,col):
        for rowt in range(row -1, row +2, 1):
            for colt in range(col -1, col +2, 1):
                if (rowt == row) and (colt == col):
                    pass
                elif (rowt <len(self.board)) and (rowt>=0) and (colt<len(self.board[0])) and (colt>=0):
                    yield [rowt, colt]

    def potential_infear(self,row,col):
        for square in self.adjacent_squares(row,col):
            piece = self.board[square[0]][square[1]]
            if (piece !=None) and (self.scared_of(piece)):
                return True
        return False

    
    def validmoves(self):
        if not(self.infear):
            for piece in self.pieces:
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
                    while (rowt >=0) and (rowt < len(self.board)) and\
                          (colt >=0) and    (colt<len(self.board[0])) and self.board[rowt][colt] == None:
                        if (not self.potential_infear(rowt,colt)) or self.trapped:
                            yield [rowt,colt]
                        rowt+=rowd
                        colt+=cold
                rowt = self.row
                colt = self.col

    def modify_fear(self):
        if (not self.potential_infear(self.row, self.col)):
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
                    while (rowt >=0) and (rowt < len(self.board)) and\
                          (colt >=0) and    (colt<len(self.board[0])) and self.board[rowt][colt] == None:
                        if (not self.potential_infear(rowt,colt)):
                            self.infear = True
                            self.infear_and_trapped = False
                            return
                        rowt+=rowd
                        colt+=cold
                rowt = self.row
                colt = self.col
        self.infear = True
        self.trapped= True
        
        
        
##########################################              
class Board:
    colors = ["BLACK", "WHITE"]
    types  = ["ELEPHANT", "MOUSE", "LION"]
    rows = 10                                  
    cols = 10
    init_piece_position =\
            [
                                [rows -1,cols/2 -1], [rows -1,cols/2],[rows -2,cols/2 -1],
                                [rows -2,cols/2 ],   [rows -2,cols/2 -2],[rows -2,cols/2 +1],
           
                                [0,cols/2 -1],[0,cols/2], [1,cols/2 -1],
                                [1,cols/2], [1,cols/2 -2], [1,cols/2 +1]
             ]
    watering_holes      =\
            [
                              [rows/2 -2, cols/2 -2],[rows/2 -2, cols/2 +1],
                              [rows/2 +1, cols/2 -2],[rows/2 +1, cols/2 +1]
                            
            ]

    @staticmethod
    def send_new_data(whitetomove, humantomove,victory, pieces):
        counter = 0
        for color in Board.colors:
            for type in Board.types:
                for i in range(2):
                    pieces.append([color,type, 
                        int(Board.init_piece_position[counter][0]), int(Board.init_piece_position[counter][1]),
                                  False, False])
                    counter +=1
        return [whitetomove, humantomove, victory, pieces]


    
    def __init__(self,whitetomove,humantomove,victory, pieces):
        self.whitetomove = whitetomove
        self.humantomove = humantomove
        self.victory = victory
        self.board = [[None for j in range(10)] for i in range(10) ]
        self.pieces = []
        for piece in pieces:
            self.pieces.append(Piece(piece, self.board, self.pieces))
        for piece in self.pieces:
            self.board[piece.row][piece.col]  = piece


    def send_updated_data(self):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != None:
                    pieces.append([piece.color, piece.type, piece.row, piece.col, piece.scared, piece.trapped])
        return [self.whitetomove, self.humantomove,self.victory, pieces]

         
        
    def all_valid_moves(self):
        for piece in self.pieces:
            for validmoves in piece.validmoves():
                yield [piece.row, piece.col, validmoves[0], validmoves[1]]


    def check_score(self):
        pass


    
    def fear_update(self,moving_piece):
        for piece in self.pieces:
            if (piece.infear) or \
               (piece.scared_of(moving_piece) and abs(piece.row -moving_piece.row)<=1 and abs(piece.col -moving_piece.col)<=1) :
                piece.modify_fear()
                
                
    def check_victory(self):
        white_counter = 0
        black_counter = 0
        for watering_hole in Board.watering_holes:
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

        
    def switch_turn(self):
        if not self.victory:
            if self.turn =="BLACK":
                self.turn == "WHITE"
            else:
                self.turn == "BLACK"

                
    def update(self, source, dest):
        piece = self.board[source[0]][source[1]]
        piece.row = dest[0]
        piece.col = dest[1]
        self.board[source[0]][source[1]] = None
        self.board[dest[0]][dest[1]] = piece

        
        self.fear_update(piece)
        self.check_victory()
        self.switch_turn()
        

##########################################      
class Game:
    @staticmethod
    def send_new_data(whitetomove, humantomove, victory, pieces, cpu_source, cpu_dest):
        return Board.send_new_data(whitetomove, humantomove, victory, pieces) + [cpu_source, cpu_dest]
    
    def __init__(self,whitetomove,humantomove, victory,pieces,source,dest):
        self.board = Board(whitetomove,humantomove, victory, pieces)
        self.human_source      = source
        self.human_dest        = dest
        
    def send_updated_data(self):
        return self.board.send_updated_data() + [self.human_source, self.human_dest]

    def execute(self):
        self.board.update(self.human_source, self.human_dest)
        ##FINISH OTHER STUFF, AI STUFF
        

##########################################
class Backend:
    def __init__(self):
        pass

    def send_new_data(self, whitetomove = True, humantomove = True,victory = False,pieces = [], cpu_source = None, cpu_dest = None):
        Game.send_new_data(whitetomove,humantomove,victory, pieces, cpu_source, cpu_dest)
    

    def receive_data(self, whitetomove,humantomove, victory, pieces,human_source,human_dest):
        self.game = Game(whitetomove,humantomove, victory, pieces,human_source,human_dest)
        self.game.execute()


    def send_updated_data(self):
        return self.game.get_updated_data()

##########################################
class rest:
    def __init__(self):
        pass





















#########################################
    
if __name__ == "__main__":
    pass
##    board = Board.send_new_data(True, True, False, [])
##    board = Board(True, True, False, board[3])
##    for i in board.board:
##        print(i)
##    for i in board.all_valid_moves():
##        print (i)
    
    
    
