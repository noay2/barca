import tkinter as tk
import PIL.ImageTk
from PIL import Image, ImageTk
import time
import math

whitetomove=True
# Set number of rows and columns
ROWS = 10
COLS = 10
SelectedSquare= None
# Create a grid of None to store the references to the tiles
tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]
pieces=["wl", "wm", "we", "bl", "bm", "be"]
afraid_pieces = set()
afraid_and_trapped = set()
stuck = set()
whitepieces=[(3,8), (6,8), (4,8), (5,8), (4,9), (5,9)]
blackpieces=[(3,1), (6,1), (4,1), (5,1), (4,0), (5,0)]
wateringholes=[(3,3), (3,6), (6,3), (6,6)]

moves=[]

tiles[3][8] = tiles[6][8] = "wl"
tiles[4][8] = tiles[5][8] = "wm"
tiles[4][9] = tiles[5][9] = "we"

tiles[3][1] = tiles[6][1] = "bl"
tiles[4][1] = tiles[5][1] = "bm"
tiles[4][0] = tiles[5][0] = "be"

def callback(event):
    global SelectedSquare
    global whitepieces, blackpieces, wateringholes
    global whitetomove, c
    global moves

    # Get rectangle diameters
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    # Calculate column and row number
    col = event.x//col_width
    row = event.y//row_height

    ############################################################
    #AI Moves for black::
    if not whitetomove:
        move1=AImakemove()
        colorsquare(move1[0][0], move1[0][1])
        colorsquare(move1[1][0], move1[1][1])
        for (cc, rr) in adjacentsquares(move1[0][0], move1[0][1]):
            if True:
                if infear(tiles[cc][rr], cc, rr):
                    c.create_image(cc*col_width, rr*row_height, image=c.fear, anchor='nw')
                    if validmovesA(cc, rr) != []: #Checks trapped pieces or not
                        afraid_and_trapped.discard( (cc, rr) )
                        afraid_pieces.add( (cc,rr) ) 
                    else:
                        afraid_pieces.discard( (cc,rr) ) 
                        afraid_and_trapped.add( (cc, rr) )
                else:
                    afraid_and_trapped.discard( (cc, rr) )
                    afraid_pieces.discard( (cc,rr) ) 
                    colorsquare(cc, rr)                                               
        for (cc, rr) in adjacentsquares(move1[1][0], move1[1][1]):
            if True:
                if infear(tiles[cc][rr], cc, rr):
                    c.create_image(cc*col_width, rr*row_height, image=c.fear, anchor='nw')
                    if validmovesA(cc, rr) != []: #Checks trapped pieces or not
                        afraid_and_trapped.discard( (cc, rr) )
                        afraid_pieces.add( (cc,rr) ) 
                    else:
                        afraid_pieces.discard( (cc,rr) ) 
                        afraid_and_trapped.add( (cc, rr) )
                else:
                    afraid_and_trapped.discard( (cc, rr) )
                    afraid_pieces.discard( (cc,rr) ) 
                    colorsquare(cc, rr)  
            if len(set(wateringholes) & set(whitepieces))==3:
                   victory("white")
            elif len(set(wateringholes) & set(blackpieces))==3:
                   victory("black")
            SelectedSquare=None
            whitetomove=True
        return
    #########################################################
     
    # If the tile is not filled, create a rectangle
    #print("Row:: " + str(row) + "\nCol:: " + str(col) +'\n')
    if not SelectedSquare:
        if not tiles[col][row]:
            print("Invalid Selection. Please select a piece.\n")
        elif (whitetomove and not (col, row) in whitepieces) :
            print("Invalid Selection. Please select a white piece.\n")
        elif (not whitetomove and not (col, row) in blackpieces) :
            print("Invalid Selection. Please select a black piece.\n")
        else:
            SelectedSquare=col, row
            #print(validmoves(col, row))
            print("White can make "+ str(totalmoves(whitepieces)) + " moves")
            print("Black can make "+ str(totalmoves(blackpieces)) + " moves")
        
        if ((col,row) not in afraid_pieces) and tiles[col][row]:
            for i in afraid_pieces:
                row1 = tiles[i[0]]
                if (row1[i[1]][0]== ('w' if whitetomove else 'b')):
                    print('You must move a newly scared piece first')
                    SelectedSquare = None
        
        
    else:

         if [col, row] in validmoves(SelectedSquare[0], SelectedSquare[1]):
            tiles[col][row]=tiles[SelectedSquare[0]][SelectedSquare[1]]
            tiles[SelectedSquare[0]][SelectedSquare[1]]=None
            if whitetomove:
                whitepieces[whitepieces.index((SelectedSquare[0],SelectedSquare[1]))]=(col, row)
                whitetomove=False
                moves.append(totalmoves(whitepieces))
            else:
                blackpieces[blackpieces.index((SelectedSquare[0],SelectedSquare[1]))]=(col, row)
                whitetomove=True
                moves.append(totalmoves(whitepieces))
            colorsquare(col, row)
            colorsquare(SelectedSquare[0], SelectedSquare[1])
            print("Average number of valid moves: " + str(sum(moves)/float(len(moves))))
            print("White Board Eval " + str(boardeval(whitepieces)))
            print("Black Board Eval " + str(boardeval(blackpieces)))
            #See if move casts fear::
            for (cc, rr) in adjacentsquares(col, row):
                if infear(tiles[cc][rr], cc, rr):
                    c.create_image(cc*col_width, rr*row_height, image=c.fear, anchor='nw')
                    if validmoves(cc, rr) != []: #Checks trapped pieces or not
                        afraid_and_trapped.discard( (cc, rr) )
                        afraid_pieces.add( (cc,rr) ) 
                    else:
                        afraid_pieces.discard( (cc,rr) ) 
                        afraid_and_trapped.add( (cc, rr) )
                else:
                    afraid_and_trapped.discard( (cc, rr) )
                    afraid_pieces.discard( (cc,rr) ) 
                    colorsquare(cc, rr)                                               
            for (cc, rr) in adjacentsquares(SelectedSquare[0], SelectedSquare[1]):
                if infear(tiles[cc][rr], cc, rr):
                    c.create_image(cc*col_width, rr*row_height, image=c.fear, anchor='nw')
                    if validmoves(cc, rr) != []: #Checks trapped pieces or not
                        afraid_and_trapped.discard( (cc, rr) )
                        afraid_pieces.add( (cc,rr) ) 
                    else:
                        afraid_pieces.discard( (cc,rr) ) 
                        afraid_and_trapped.add( (cc, rr) )
                else:
                    afraid_and_trapped.discard( (cc, rr) )
                    afraid_pieces.discard( (cc,rr) ) 
                    colorsquare(cc, rr)  
            if len(set(wateringholes) & set(whitepieces))==3:
                   victory("white")
            elif len(set(wateringholes) & set(blackpieces))==3:
                   victory("black")
            SelectedSquare=None
            
         else:
             print("Invalid Move.\n")
             SelectedSquare=None

def boardeval(piecess):
    #How many watering holes you have:
    global waterinholes
    score=0
    holes=len(set(piecess).intersection(set(wateringholes)))
    if holes==1:
        score=score+20
    elif holes==2:
        score=score+50
    elif holes==3:
        score=score+10000
    #Can you get a hole next turn?:
    for (col, row) in piecess:
        for [coll,roww] in validmoves(col,row):
            if (coll, roww) in wateringholes:
                score=score+5**holes
    #Are your pieces adjacent to the watering holes?
    for (col,row) in piecess:
        for (coll, roww) in wateringholes:
            if [col, row] in adjacentsquares(coll, roww):
                score=score+5
    #Can you intimitade an opponent's piece?
    for (col,row) in piecess:
        maxfearcount=0
        for [coll, roww] in validmoves(col,row):
            fearcount=0
            for (co, ro) in adjacentsquares(coll, roww):
                if tiles[co][ro]==intimidates(tiles[col][row]):
                    fearcount+=1
                    if (co, ro) in wateringholes: 
                        score+=10 #If you can scare a watering hole occupent, +10
                    if fearcount>maxfearcount:
                        maxfearcount=fearcount
        if maxfearcount==1:
            score+=5 #can scare one piece 
        if maxfearcount==2:
            score+=15 #can scare two pieces
    #Are your pieces Afraid?
    score-=5*len(set(afraid_pieces).intersection(set(piecess)))
    return score

def otherpieces(piecess):
    if piecess==whitepieces:
        return blackpieces
    else:
        return whitepieces


def totalmoves(piecess):
    counter=0
    for (col, row) in piecess:
        counter+=len(validmoves(col, row))
    return counter

def totalmovesblack():
    counter=0
    for (col, row) in blackpieces:
        counter+=len(validmoves(col, row))
    return counter

def adjacentsquares(col, row):
    squares=[]
    for cols in range(col-1,col+2):
        for rows in range(row-1, row+2):
            if cols in range(COLS) and rows in range(ROWS):
                squares.append([cols, rows])
    return squares

def fears(piece):
    if piece == "wl":
        return "be"
    if piece == "bl":
        return "we"
    if piece == "we":
        return "bm"
    if piece == "be":
        return "wm"
    if piece == "wm":
        return "bl"
    if piece == "bm":
        return "wl"
    if piece==None:
        return "999"

def intimidates(piece):
    if piece == "we":
        return "bl"
    if piece == "be":
        return "wl"
    if piece == "wm":
        return "be"
    if piece == "bm":
        return "we"
    if piece == "wl":
        return "bm"
    if piece == "bl":
        return "wm"
    if piece==None:
        return "999"

def infear(piece, col, row):
    for [c, r] in adjacentsquares(col, row):
        if tiles[c][r]==fears(piece):
            return True
    return False

def victory(color):
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    if color=="white":
        print("WHITE WINS!")
        for (col,row) in whitepieces:
            c.create_image(col*col_width, row*row_height, image=c.coronet, anchor='nw')
    if color=="black":
        print("BLACK WINS!")
        for (col, row) in blackpieces:
            c.create_image(col*col_width, row*row_height, image=c.coronet, anchor='nw')

def validmoves(col, row):
    global afraid_pieces
    if len(afraid_pieces.intersection(set(getcolor(col,row)))) != 0: 
        if ((col,row) not in afraid_pieces) and tiles[col][row]:
            return []

    moves=[]
    temp_afraid_moves = [] 
    piece=tiles[col][row]
    unafraid=True
    colt=col
    rowt=row
    for rowd in (-1,0,1):
        for cold in (-1,0,1):
            if (rowd ==0 == cold):
                pass
            elif (abs(cold) == abs(rowd) and (piece=="wl" or piece=="bl" or piece=="be" or piece=="we")) or\
                 ((cold ==0 or rowd ==0 ) and (piece=="wm" or piece=="bm" or piece=="be" or piece=="we")):
                colt +=cold
                rowt += rowd
                while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]: 
                    if (not infear(piece, colt, rowt)) or (col, row) in afraid_and_trapped:
                        moves.append([colt, rowt])
                    else:
                        temp_afraid_moves.append( [colt, rowt]) 
                    colt+=cold
                    rowt+=rowd
            unafraid=True
            colt = col
            rowt = row
    if (len(moves) == 0) and (len(temp_afraid_moves) !=0 ): 
         return [] 

 #       temp_afraid_moves.append([col, row])
    return moves

def validmovesA(col, row): #Doesn't account for if other pieces are afraid
    moves=[]
    temp_afraid_moves = [] 
    piece=tiles[col][row]
    unafraid=True
    colt=col
    rowt=row
    for rowd in (-1,0,1):
        for cold in (-1,0,1):
            if (rowd ==0 == cold):
                pass
            elif (abs(cold) == abs(rowd) and (piece=="wl" or piece=="bl" or piece=="be" or piece=="we")) or\
                 ((cold ==0 or rowd ==0 ) and (piece=="wm" or piece=="bm" or piece=="be" or piece=="we")):
                colt +=cold
                rowt += rowd
                while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]: 
                    if (not infear(piece, colt, rowt)) or (col, row) in afraid_and_trapped:
                        moves.append([colt, rowt])
                    else:
                        temp_afraid_moves.append( [colt, rowt]) 
                    colt+=cold
                    rowt+=rowd
            unafraid=True
            colt = col
            rowt = row

    if (len(moves) == 0) and (len(temp_afraid_moves) !=0 ): 
         return [] 
    return moves

def getcolor(col, row): #returns the color of a piece at a certain square:
    global whitepieces, blackpieces
    if tiles[col][row]:
        if tiles[col][row][0]=='w':
            return whitepieces
        elif tiles[col][row][0]=='b':
            return blackpieces
    else:
        return None

def AImakemove():
    global blackpieces, whitepieces,tiles
    bestmove=((0,0), (0,0), -1000)
    for (col,row) in blackpieces:
        for (coll, roww) in validmoves(col, row):
            makemoveblack(col, row, coll, roww)
            value=boardeval(blackpieces)-boardeval(whitepieces)
            if value>bestmove[2]:
                bestmove=((col,row), (coll,roww), value)
            makemoveblack(coll, roww, col, row)
    (coll, roww)=bestmove[1]
    (col,row)=bestmove[0]
    tiles[coll][roww]=tiles[col][row]
    tiles[col][row]=None
    return ((col,row), (coll, roww))
 
def makemoveblack(col,row, col1, row1):
    global blackpieces, tiles
    tiles[col1][row1]=tiles[col][row]
    tiles[col][row]=None
    blackpieces[blackpieces.index((col,row))]=(col1, row1)
    if True:
        for (cc, rr) in adjacentsquares(col, row):
            if True:
                if infear(tiles[cc][rr], cc, rr):
                    c.create_image(cc*col_width, rr*row_height, image=c.fear, anchor='nw')
                    if validmovesA(cc, rr) != []: #Checks trapped pieces or not
                        afraid_and_trapped.discard( (cc, rr) )
                        afraid_pieces.add( (cc,rr) ) 
                    else:
                        afraid_pieces.discard( (cc,rr) ) 
                        afraid_and_trapped.add( (cc, rr) )
                else:
                    afraid_and_trapped.discard( (cc, rr) )
                    afraid_pieces.discard( (cc,rr) ) 
                                                                  
        for (cc, rr) in adjacentsquares(col1, row1):
            if True:
                if infear(tiles[cc][rr], cc, rr):
                    c.create_image(cc*col_width, rr*row_height, image=c.fear, anchor='nw')
                    if validmovesA(cc, rr) != []: #Checks trapped pieces or not
                        afraid_and_trapped.discard( (cc, rr) )
                        afraid_pieces.add( (cc,rr) ) 
                    else:
                        afraid_pieces.discard( (cc,rr) ) 
                        afraid_and_trapped.add( (cc, rr) )
                else:
                    afraid_and_trapped.discard( (cc, rr) )
                    afraid_pieces.discard( (cc,rr) ) 
                    

def loadgraphics():
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    img = Image.open("well.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.well=well = ImageTk.PhotoImage(img)

    img = Image.open("whitelion2.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.whitelion=whitelion = ImageTk.PhotoImage(img)

    img = Image.open("whitemouse2.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.whitemouse=whitemouse = ImageTk.PhotoImage(img)

    img = Image.open("whiteelephant2.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.whiteelephant=whiteelephant = ImageTk.PhotoImage(img)

    img = Image.open("blackelephant.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.blackelephant=blackelephant = ImageTk.PhotoImage(img)

    img = Image.open("blacklion.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.blacklion=blacklion = ImageTk.PhotoImage(img)

    img = Image.open("blackmouse.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.blackmouse=blackmouse = ImageTk.PhotoImage(img)

    img = Image.open("coronet.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.coronet=coronet = ImageTk.PhotoImage(img)

    img = Image.open("fear.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.fear=fear= ImageTk.PhotoImage(img)

def colorsquare(col, row):
    global wateringholes, c
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    #whitelion = tk.PhotoImage(file = './b185f0114f241d9bd5471f0c94c9d5a7.gif')
    #scale_w = col_width//whitelion.width()
    #scale_h = row_height//whitelion.height()

    if (row+col)%2==0:
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="darkblue")  
    else:
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="lightblue")
    if (col, row) in wateringholes:
        c.create_image(col*col_width, row*row_height, image=c.well, anchor='nw')
 
    if(tiles[col][row]=="wl"):
        c.create_image(col*col_width, row*row_height, image=c.whitelion, anchor='nw')
    elif(tiles[col][row]=="wm"):
        c.create_image(col*col_width, row*row_height, image=c.whitemouse, anchor='nw')
    elif(tiles[col][row]=="we"):
        c.create_image(col*col_width, row*row_height, image=c.whiteelephant, anchor='nw')
    elif(tiles[col][row]=="bl"):
        c.create_image(col*col_width, row*row_height, image=c.blacklion, anchor='nw')
    elif(tiles[col][row]=="bm"):
        c.create_image(col*col_width, row*row_height, image=c.blackmouse, anchor='nw')
    elif(tiles[col][row]=="be"):
        c.create_image(col*col_width, row*row_height, image=c.blackelephant, anchor='nw')

# Create the window, a canvas and the mouse click event binding
def checkerboard(can):
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    for row in range(10):
        for col in range(10):
            colorsquare(col, row)
def reset2():
    global whitepieces, blackpieces
    whitepieces=[(3,8), (6,8), (4,8), (5,8), (4,9), (5,9)]
    blackpieces=[(3,1), (6,1), (4,1), (5,1), (4,0), (5,0)]
    time.sleep(5)
    checkerboard(c)

# Create the window, a canvas and the mouse click event binding
root = tk.Tk()
c = tk.Canvas(root, width=600, height=600, borderwidth=1, background='white')
c.grid(row=0,column=0)
root.update_idletasks()
loadgraphics()
c.pack()

checkerboard(c)

c.pack()
c.bind("<Button-1>", callback)
label=tk.Label()

root.mainloop()
