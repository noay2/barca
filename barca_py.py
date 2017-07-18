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
        if (self.color != piece.color) and
            (  ((self.type == "ELEPHANT")and (piece.type == "LION"))\
            or ((self.type == "LION")   and (piece.type == "MOUSE"))\
            or ((self.type == "MOUSE")  and (piece.type == "ELEPHANT"))\
            ):
            return True
        else:
            return False


    def scared_of(self, piece):
        return piece.scares(self)
    
    def fears(self, piece):
        if self.scares(piece)
        and (abs(self.row - piece.row) <=1)
        and (abs(self.col - piece.col) <=1):
            return True
        else:
            return False

    def infear_of(self, piece):
        return piece.fears(self)


    def potential_infear(self,row,col):
        for piece in self.pieces:
            if pieces.fears(self)
            and (abs(row- piece.row) <=1)
            and (abs(col- piece.col) <=1):
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
                            yield [self.row, self.col, rowt , colt]
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
                            self.trapped = False
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
                    pieces.append([piece.color, piece.type, piece.row, piece.col, piece.infear, piece.trapped])
        return [self.whitetomove, self.humantomove,self.victory, pieces]

    def all_valid_moves(self):
        for piece in self.pieces:
            if (piece.color == "WHITE" and self.whitetomove) or (piece.color == "BLACK" and not self.whitetomove):
                for validmoves in piece.validmoves():
                    yield [piece.row, piece.col, validmoves[0], validmoves[1]]

    def watering_hole_counter(self):
        white_counter = 0
        black_counter = 0
        for watering_hole in Board.watering_holes:
            if (self.board[int(watering_hole[0])][int(watering_hole[1])]!= None):
                if (self.board[int(watering_hole[0])][int(watering_hole[1])]).color == "BLACK":
                    black_counter +=1
                else:
                    white_counter +=1
        return [white_counter, black_counter]

    def board_evaluation(self):
        score=0
        maxfearcount=0

        #How many watering holes you have:
        acquired_holes= self.watering_hole_counter()
        holes = acquired_holes[0] if self.whitetomove else acquired_holes[1]
        if holes==1:
            score=score+20
        elif holes==2:
            score=score+50
        elif holes==3:
            score=score+1000000

        #Are you next to a watering hole:
        for piece in self.pieces:
            if (piece.color == "WHITE" and self.whitetomove) or (piece.color == "BLACK" and not self.whitetomove):
                for watering_hole in Board.watering_holes:
                    if watering_hole in piece.adjacent_squares(piece.row, piece.col):
                        score=score+5

        #How many pieces do you fear the current turn
        for piece in self.pieces:
            if (not ((piece.color == "WHITE" and self.whitetomove) or (piece.color == "BLACK" and not self.whitetomove)) )and piece.infear:
                score +=4

        #Going Through All Validmoves
        for piece in self.pieces:
            if  (piece.color == "WHITE" and self.whitetomove) or (piece.color == "BLACK" and not self.whitetomove):
                for valid_move in piece.validmoves():
                    score+=0.2
                    fearcount=0
                    #Going Through Adjacent Cells to All Validmoves
                    for adjacent_square in piece.adjacent_squares(valid_move[2], valid_move[3]):
                        #Does one of you pieces fear another piece the next turn
                        if (self.board[adjacent_square[0]][adjacent_square[1]] != None) and ((self.board[valid_move[0]][valid_move[1]]).scares(self.board[adjacent_square[0]][adjacent_square[1]]))\
                        and (abs(valid_move[2] -adjacent_square[0])<=1) and (abs(valid_move[3] - adjacent_square[1]) <=1):
                            fearcount+=1
                            if adjacent_square in Board.watering_holes: 
                                score+=10 #If you can scare a watering hole occupent, +10
                                if fearcount>maxfearcount:
                                    maxfearcount=fearcount
                   #Can you get a hole next turn?:
                    if (valid_move[2], valid_move[3]) in Board.watering_holes:
                        if holes==0:
                            score+=5
                        elif holes==1:
                            score+=20
                        elif holes==2: 
                            score+=50
            if maxfearcount==1:
                score+=5 #can scare one piece 
            if maxfearcount==2:
                score+=15 #can scare two pieces

        #Are your pieces Afraid?
        for piece in self.pieces:
            if ((piece.color == "WHITE" and self.whitetomove) or (piece.color == "BLACK" and not self.whitetomove) )and piece.infear:
            	score-=5

        return score

    
    def fear_update(self,moving_piece):
        for piece in self.pieces:
            if (piece.infear) or \
               (piece.scared_of(moving_piece) and abs(piece.row -moving_piece.row)<=1 and abs(piece.col -moving_piece.col)<=1) :
                piece.modify_fear()
                
                
    def check_victory(self):
        counter = self.watering_hole_counter()
        if counter[0] >= 3:
            self.victory = "WHITE"
            return "WHITE"
        elif counter[1] >=3:
            self.victory = "BLACK"
            return "BLACK"
        else:
            return None

        
    def switch_turn(self):
        if not self.victory:
            self.whitetomove = not self.whitetomove
    

                
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
class AI:
    def __init__(self, board):
        self.board = board
        
    def AI_decide_self(self):                                        #AI turn
        bestmove= ([0,0],[0,0], -1000)
        current_evaluation = self.board.board_evaluation()
        infear_array = [ piece.infear for piece in self.board.pieces]
        trapped_array= [ piece.trapped for piece in self.board.pieces]
        for piece in self.board.pieces:
            if  (piece.color == "WHITE" and self.board.whitetomove) or (piece.color == "BLACK" and not self.board.whitetomove):
                print(piece.color)
                print(self.board.whitetomove)
                for valid_move in piece.validmoves():
                    self.board.update([valid_move[0], valid_move[1]], [valid_move[2], valid_move[3]])
                    value=current_evaluation - self.board.board_evaluation()
                    if value>bestmove[2]:
                        bestmove=([valid_move[0],valid_move[1]], [valid_move[2],valid_move[3]] , value)
                    self.board.update([valid_move[2], valid_move[3]], [valid_move[0], valid_move[1]])
                    for piece in range(len(self.board.pieces)):
                        self.board.pieces[piece].infear = infear_array[piece]
                        self.board.pieces[piece].trapped = trapped_array[piece]

        
        return [bestmove[0], bestmove[1]]
    	
        
##########################################       
class Game:

    def __init__(self,whitetomove,humantomove, victory,pieces,source,dest):
        self.board = Board(whitetomove,humantomove, victory, pieces)
        self.human_source      = source
        self.human_dest        = dest
        self.ai =               AI(self.board)
        self.ai_sourece        = None
        self.ai_dest           = None
        self.execute()
        
    def send_updated_data(self):
        return self.board.send_updated_data() + [self.ai_sourece, self.ai_dest]

    def execute(self):
        if (not self.board.victory) and self.human_source != None) and (self.human_dest != None):
            self.board.update(self.human_source, self.human_dest)
        if (not self.board.victory):
            self.ai_source, self.ai_dest = self.ai.AI_decide_self()
            self.board.update(self.ai_source, self.ai_dest)

##########################################
class Backend:
    def __init__(self):
        pass

    def receive_data(self, whitetomove,humantomove, victory, pieces,human_source,human_dest):
        self.game = Game(whitetomove,humantomove, victory, pieces,human_source,human_dest)


    def send_updated_data(self):
        return self.game.send_updated_data()

##########################################
class rest:
    def __init__(self):
        pass





















#########################################
    
if __name__ == "__main__":
    backend = Backend()
    output = backend.send_new_data()
    backend.receive_data(True, True, False, [['BLACK', 'ELEPHANT', 9, 4, False, False],
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
                                                                   ['WHITE', 'LION', 1, 6, False, False]], [1,4], [4,4])

    
    output = backend.send_updated_data()
    backend.receive_data(True, True, False, [['WHITE', 'ELEPHANT', 0, 4, False, False],
                         ['WHITE', 'ELEPHANT', 0, 5, False, False],
                         ['WHITE', 'LION', 1, 3, False, False],
                         ['WHITE', 'MOUSE', 1, 5, False, False],
                         ['WHITE', 'LION', 1, 6, False, False],
                         ['WHITE', 'MOUSE', 4, 4, True, False],
                         ['BLACK', 'LION', 5, 3, False, False],
                         ['BLACK', 'LION', 8, 3, False, False],
                         ['BLACK', 'MOUSE', 8, 4, False, False],
                         ['BLACK', 'MOUSE', 8, 5, False, False],
                         ['BLACK', 'ELEPHANT', 9, 4, False, False],
                         ['BLACK', 'ELEPHANT', 9, 5, False, False]], [4, 4], [2, 4])
    
    output = backend.send_updated_data()
    backend.receive_data(True, True, False,
                         [['WHITE', 'ELEPHANT', 0, 4, False, False],
                          ['WHITE', 'ELEPHANT', 0, 5, False, False],
                          ['WHITE', 'LION', 1, 3, False, False],
                          ['WHITE', 'MOUSE', 1, 5, True, False],
                          ['WHITE', 'LION', 1, 6, False, False],
                          ['WHITE', 'MOUSE', 2, 4, False, False],
                          ['BLACK', 'LION', 2, 6, False, False],
                          ['BLACK', 'LION', 8, 3, False, False],
                          ['BLACK', 'MOUSE', 8, 4, False, False],
                          ['BLACK', 'MOUSE', 8, 5, False, False],
                          ['BLACK', 'ELEPHANT', 9, 4, False, False],
                          ['BLACK', 'ELEPHANT', 9, 5, False, False]], [1, 5], [6, 5])
    output = backend.send_updated_data()


    
