import time
import math



##########################################
class Piece:
    def __init__(self, piece_arr, board):
        self.color   = piece_arr[0]
        self.type    = piece_arr[1]
        self.row     = piece_arr[2]
        self.col     = piece_arr[3]
        self.infear  = piece_arr[4]
        self.trapped = piece_arr[5]
        self.board = board

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
            for piece in self.Pieces:
                if piece.infear and (not piece.trapped) and (piece.color ==self.color):
                    return
        rowt = len(self.board)
        colt = len(self.board[0])
        for rowd in range(-1,2,1):
            for cold in range(-1,2,1):
                if (rowd ==0) and (cold==0):
                    pass
                elif ( (abs(cold) == abs(rowd)) and (self.type == "LION" or self.type == "ELEPHANT")) \
                   or (( (cold ==0) or (rowd==0)) and (self.type == "MOUSE" or self.type == "ELEPHANT")):
                    colt += cold
                    rowt += rowd
                    while (rowt >=0) and (rowt < len(self.board)) and\
                          (colt >=0) and    (colt<len(self.board[0])):
                        if (not self.potential_infear(rowt,colt)) or self.trapped:
                            yield [rowt,colt]
                        rowt+=rowd
                        colt+=cold
                rowt = len(board)
                colt = len(board[0])
##########################################              
class Board:
     def __init__(self,whitetomove,humantomove,victory, Pieces):
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
        self.victory = victory
        self.board = [[None for j in range(10)] for i in range(10) ]
        self.Pieces = [ Piece(piece) for piece in Pieces]
        for piece in self.Pieces:
            self.board[piece.row][piece.col]  = piece



        
    def all_valid_moves(self):
        for piece in in self.Pieces:
            for validmoves in piece.validmoves():
                yield [piece.row, piece.col, validmoves[0], validmoves[1]]

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
        
    def switch_turn(self):
        if not self.victory:
            if self.turn =="BLACK":
                self.turn == "WHITE"
            else:
                self.turn == "BLACK"
                
    def update(self, source, dest):
        self.board = 
        
        


##########################################      
class Game(self):
    def __init__(self,whitetomove,humantomove, victory,Pieces,source,dest):
        self.board = Board(whitetomove,humantomove, victory, Pieces,source,dest)
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


    def send_new_data(self, whitetomove = True, humantomove = True,victory = False, source = None, dest = None):
        Pieces = []
        counter = 0
        for color in self.colors:
            for type in self.types:
                for i in range(2):
                    Pieces.append([color,type, 
                        int(self.init_piece_position[counter][0]), int(self.init_piece_position[counter][1]),
                                  False, False])
                    counter +=1
        return [whitetomove, humantomove, victory, Pieces, source, dest]
    

    def receive_data(self, whitetomove,humantomove, Pieces,source,dest):
        self.game = Game(whitetomove,humantomove, victory, Pieces,source,dest)



    def send_updated_data(self):
        Pieces = []
        for row in self.game.board.board:
            for piece in row:
                if piece != None:
                    Pieces.append([piece.color, piece.type, piece.row, piece.col, piece.scared, piece.trapped])
        return [self.game.board.whitetomove, self.game.board.humantomove,self.game.board.victory, Pieces, self.game.source, self.game.dest]


##########################################
class rest:
    def __init__(self):
        pass

    
    
    
    
    
    
   
Boardlength=10
Boardwidth=10



def adjacentTuples(location):
    list=[]
    for first in (-1,0,1):
        for second in (-1,0,1):
            a=location[0]+first
            b=location[1]+second
            if (((a,b)!=location) and a<Boardwidth and b<Boardlength and a>=0 and b>=0):
                list.append((a,b))
    return list

def areAdjacent(point1, point2):
    return abs(point1[0]-point2[0])<=1 and abs(point1[1]-point2[1])<=1




class Piece:

    def __init__(self, board, color, location): #Confirmed
        self.color = color    #Piece initialized with color and location
        self.location=location
        self.board=board
    def oppositecolor(self, piece): #Confirmed
        return (piece.color!=self.color)
    def othercolor(self):
        if(self.color=='white'):
            return 'black'
        return 'white'
    def scares(self, piece): #Confirmed
        return ((type(piece) is self.piece_it_scares()) and self.oppositecolor(piece))
    validmoves=[]
    adjacenttovalidmoves=[]
    piecesToFear=[]


    #This is the gold standard for directional moves.
    def Nmoves(self):
        moves=[]
        point=self.location
        lowestYCoord=10
        #Check if there is a piece directly north: (12 comparisons)
        for location in self.board.pieceLocations:
            if (location[0]==point[0] and location[1]>point[1] and locations[1]<lowestYCoord):
                lowestYCoord=location[1]
        #If there is, than this obstruction is the stopping point
        #Compile all valid northerly moves: (<9 operations)
        for y in range(point[1], lowestYCoord):
            moves.append(point[0], y)

        #Check if there if there is a fearsome piece adjacent to any of these squares
        fearsomeLocations=self.board.fearsomeLocations(self) #get a list of the locations of the pieces it is scared of O(1)
        for fearpoint in fearsomeLocations:
            for move in moves:
                if areAdjacent(move, fearpoint): #(18 comparisons operations maximum)
                    del move[moves.index(move)]

        this.Northmoves=moves #update member
        return moves #Return them
        # All told, maximum of 40 operations. 


    def Smoves(self):
        #calulate Southerly moves
        self.Southmoves=[] #update member
        return [] #Return them
    def Emoves(this):
        #calulate Easterly moves
        return [] #Return them
    def Wmoves(this):
        #calulate Westerly moves
        return [] #Return them
    def NEmoves(this):
        #calulate NorthEasterly moves
        NorthEastmoves=[] #update the structure
        return [] #Return them
    def NWmoves(this):
        #calulate NorthWesterly moves
        NorthWestmoves=[] #update the structure
        return [] #Return them
    def SEmoves(this):
        #calulate SouthEasterly moves
        return [] #Return them
    def SWmoves(this):
        #calulate SouthWesterly moves
        return [] #Return them

class Lion(Piece):
    def is_afraid_of(piece):
        return (type(piece)==Elephant and oppositecolor(piece))
    def in_line_of_sight(location):
        return (location[0]-self.location[0]==location[1]-self.location[1] or location[0]-self.location[0]==-location[1]+ self.location[1])
    def piece_it_scares(self):
        return (self.othercolor, Mouse)
    NorthEastmoves=[]
    SouthEastmoves=[]
    SouthWestmoves=[]
    NorthWestmoves=[]
   

class Elephant(Piece): 
    def is_afraid_of(piece):
        return (type(piece)==Mouse and oppositecolor(piece))

    def in_line_of_sight(location):
        return location[0]==self.location[0] or location[1]==self.location[1] or location[0]-self.location[0]==location[1]-self.location[1] or location[0]-self.location[0]==-location[1]+ self.location[1]
    def piece_it_scares(self):
        return Lion
class Mouse(Piece):
    def is_afraid_of(piece):
        return (type(piece)==Lion and oppositecolor(piece))
    def in_line_of_sight(location):
        return location[0]==self.location[0] or location[1]==self.location[1] 
    def piece_it_scares(self):
        return Elephant
    Northmoves=[]
    Southmoves=[]
    Eastmoves=[]
    Westmoves=[]

defaultStartingPosition=[(4, 1), (5, 1), (4, 0), (5, 0), (3, 1), (6, 1), (4, 8), (5, 8), (4, 9), (5, 9), (3, 8), (6, 8)] #etc.

class Board: #Also make class copyBoard, which inherits everything, but with new init method
    def __init__(self, startingPostion=None):
        if(startingPosition==None):
            self.startingPose=defaultStartingPosition
        else:
            self.startPose=startingPosition
        self.whiteMouse1=Mouse(self, 'white', startPose[0])
        self.whiteMouse2=Mouse(self, 'white', startPose[1])
        self.whiteElephant1=Elephant(self, 'white', startPose[2])
        self.whiteElephant2=Elephant(self, 'white', startPose[3])
        self.whiteLion1=Lion(self, 'white', startPose[4])
        self.whiteLion2=Lion(self, 'white', startPose[5])

        self.blackMouse1=Mouse(self, 'black', startPose[6])
        self.blackMouse2=Mouse(self, 'black', startPose[7])
        self.blackElephant1=Elephant(self, 'black', startPose[8])
        self.blackElephant2=Elephant(self, 'black', startPose[9])
        self.blackLion1=Lion(self, 'black', startPose[10])
        self.blackLion2=Lion(self, 'black', startPose[11])

        # Keep a list of each type of piece:
        self.whitemice=[]
        self.whitemice.append(self.whiteMouse1)
        self.whitemice.append(self.whiteMouse2)
        self.whitelions=[]
        self.whitelions.append(self.whiteLion1)
        self.whitelions.append(self.whiteLion2)
        self.whiteelephants=[]
        self.whiteelephants.append(self.whiteElephant1)
        self.whiteelephants.append(self.whiteElephant2)

        self.blackmice=[]
        self.blackmice.append(self.blackMouse1)
        self.blackmice.append(self.blackMouse2)
        self.blacklions=[]
        self.blacklions.append(self.blackLion1)
        self.blacklions.append(self.blackLion2)
        self.blackelephants=[]
        self.blackelephants.append(self.blackElephant1)
        self.blackelephants.append(self.blackElephant2)

        #Keep list of all pieces: (Do we really need this)
        self.allPieces=[]
        self.allPieces.extend(self.whitemice)
        self.allPieces.extend(self.whitelions)
        self.allPieces.extend(self.whiteelephants)
        self.allPieces.extend(self.blackmice)
        self.allPieces.extend(self.blacklions)
        self.allPieces.extend(self.blackelephants)

        #Keep list of all piece locations: (Needs updating)
        self.pieceLocations=[]
        for i in range(0, 12):
            self.pieceLocations.append(allPieces[i].location())

    def makeMove(self, piece, endlocation):
        #update piece
        #update self.pieceLocations
        pass
    def fearsomeLocations(self, piece):
        if(type(piece)==Elephant):
            if(piece.color=='black'):
                return [self.pieceLocations[0], self.pieceLocations[1]]
            else:
                return [self.pieceLocations[6], self.pieceLocations[7]]
        if(type(piece)==Lion):
            if(piece.color=='black'):
                return [self.pieceLocations[2], self.pieceLocations[3]]
            else:
                return [self.pieceLocations[8], self.pieceLocations[9]]
        if(type(piece)==Mouse):
            if(piece.color=='black'):
                return [self.pieceLocations[4], self.pieceLocations[5]]
            else:
                return [self.pieceLocations[10], self.pieceLocations[11]]




# AI stuff below

def partial_derivative(func, dimension, delta, point):
    #Func take an n-dimensional vector as arugument, 0<=dimension<n, delta is a number, and point is an n-dimensional vector
    point2=list(point)
    point2[dimension]+=delta
    return (func(point2)-func(point))/delta

def gradient(func, delta, point):
    grad=[]
    for i in range(0,len(point)):
        grad.append(partial_derivative(func, i, delta, point))
    return grad

def descent(func, delta, rate, point):
    totalfuncevals=0
    for j in range (0, 1000):
        point1=[]
        grad=gradient(func, delta, point)
        print("Function value: "+ str(func(point)))
        for i in range(0, len(point)):
            point1.append(point[i]+rate*grad[i])
        point=list(point1)
        





def func1(point):
    return point[0]*point[0]
def func2(point):
    return 5-(point[0]**2+point[1]**2)**0.5

def func3(point):
    return -2*point[0]**2+4*point[0]-3*point[1]**2+8*point[1]-point[2]**2+7*point[2] 

#descent(func2, 0.1, 1.4, [6,6])
#descent(func3, 0.1, 0.009, [6,6,5])
#print(partial_derivative(func1, 0, 1, [1]))
#print(gradient(func2, 0.01, [1,1]))


""" Test of adjacentTuples
print( adjacentTuples((2,2)))
print( adjacentTuples((0,0)))
"""

""" Test of scares function:
whiteLion1=Lion('white', (3, 1))
blackMouse1=Mouse('black', (4, 8))
print(whiteLion1.scares(blackMouse1))
"""
