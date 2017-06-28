import tkinter as tk
import PIL.ImageTk
from PIL import Image, ImageTk
import time
import math
import threading

########################Initialization stuff
exists_victory = False                      ##This is all for interaction between center and human and cpu                    
centerturn = False                            
centerturnmoves = None
whitetomove=True                            
humantomove=True


SelectedSquare = None                       ##This is part of registering GUI clicks from human


ROWS = 10                                   ##Board information
COLS = 10
tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]  
pieces=["wl", "wm", "we", "bl", "bm", "be"]
tiles[3][8] = tiles[6][8] = "wl"
tiles[4][8] = tiles[5][8] = "wm"
tiles[4][9] = tiles[5][9] = "we"
tiles[3][1] = tiles[6][1] = "bl"
tiles[4][1] = tiles[5][1] = "bm"
tiles[4][0] = tiles[5][0] = "be"
whitepieces=[(3,8), (6,8), (4,8), (5,8), (4,9), (5,9)]
blackpieces=[(3,1), (6,1), (4,1), (5,1), (4,0), (5,0)]
wateringholes=[(3,3), (3,6), (6,3), (6,6)]



last_piece_checked_trapped = False            ##Trapped/Afraid Information
afraid_pieces = set()
afraid_and_trapped = set()
moves=[]







   
#########################################################  Helper Functions


def otherpieces(piecess):
    global whitepieces, blackpieces
    if piecess==whitepieces:
        return blackpieces
    else:
        return whitepieces

def totalmovesblack():
    global blackpieces
    counter=0
    for (col, row) in blackpieces:
        counter+=len(validmoves(col, row))
    return counter

def totalmoveswhite():
    global whitepieces
    counter=0
    for (col, row) in whitepieces:
        counter+=len(validmoves(col, row))
    return counter

def totalmoves(piecess):
    counter=0
    for (col, row) in piecess:
        counter+=len(validmoves(col, row))
    return counter


def getcolor(col, row): 
    global whitepieces, blackpieces
    if tiles[col][row]:
        if tiles[col][row][0]=='w':
            return whitepieces
        elif tiles[col][row][0]=='b':
            return blackpieces
    else:
        return None

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
    global tiles
    for [c, r] in adjacentsquares(col, row):
        if tiles[c][r]==fears(piece):
            return True
    return False

def have_fear(whitetomove = True):
    global blackpieces, whitepieces,tiles
    for i in afraid_pieces:
        tile = tiles[i[0]][i[1]]
        if (tile[0]== ('w' if whitetomove else 'b')):
            return True

def adjacentsquares(col, row):#This also has to check the current square too!- becuz of fear_update()
    squares=[]
    for cols in range(col-1,col+2):
        for rows in range(row-1, row+2):
            if cols in range(COLS) and rows in range(ROWS):
                squares.append([cols, rows])
    return squares


#########################################################  More specific/detailed functions

def validmoves(col, row):
    global afraid_pieces,tiles, last_piece_checked_trapped                      
    if len(afraid_pieces.intersection(set(getcolor(col,row)))) != 0: ###Checks if piece is not afraid and there exists other afraid piece; If there is another afraid piece that can move, that is priority
        if ((col,row) not in afraid_pieces) and tiles[col][row]:
            return []

    moves=[]                                    ##Checks all valid moves
    afraid_moves = [] 
    piece=tiles[col][row]
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
                    if (not infear(piece, colt, rowt)):
                        moves.append([colt, rowt])
                    else:
                        afraid_moves.append( [colt, rowt]) 
                    colt+=cold
                    rowt+=rowd
            colt = col
            rowt = row
            
    if (len(moves) == 0) and (len(afraid_moves) !=0 ) and infear(piece, col, row): ##Checks if piece is trapped; in this case, all of those bad/afraid moves become valid
         last_piece_checked_trapped = True
         return afraid_moves
    return moves

def boardeval(piecess):
    #How many watering holes you have:
    global wateringholes, tiles, afraid_pieces
    score=0
    holes=len(set(piecess).intersection(set(wateringholes)))
    if holes==1:
        score=score+20
    elif holes==2:
        score=score+50
    elif holes==3:
        score=score+10000
    maxfearcount=0

    for (col, row) in piecess:
        for (coll, roww) in wateringholes:
            if [col, row] in adjacentsquares(coll, roww):
                score=score+5
        #Can you intimitade an opponent's piece?
        for [coll,roww] in validmoves(col,row):
            score+=0.2
            fearcount=0
            for (co, ro) in adjacentsquares(coll, roww):
                if tiles[co][ro]==intimidates(tiles[col][row]):
                    fearcount+=1
                    if (co, ro) in wateringholes: 
                        score+=10 #If you can scare a watering hole occupent, +10
                    if fearcount>maxfearcount:
                        maxfearcount=fearcount
           #Can you get a hole next turn?:
            if (coll, roww) in wateringholes:
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
    score-=5*len(set(afraid_pieces).intersection(set(piecess)))

    return score

def AImakemove():                                        #AI turn
    global blackpieces, whitepieces,tiles, whitetomove
    starttime=time.time()
    bestmove=((0,0), (0,0), -1000)
    for (col,row) in (whitepieces if whitetomove else blackpieces):
        for (coll, roww) in validmoves(col, row):
            makemove(col, row, coll, roww)
            value=(boardeval(blackpieces)-boardeval(whitepieces)) if not whitetomove else (boardeval(whitepieces)-boardeval(blackpieces))
            if value>bestmove[2]:
                bestmove=((col,row), (coll,roww), value)
            makemove(coll, roww, col, row)
    (coll, roww)=bestmove[1]
    (col,row)=bestmove[0]
    #print(time.time()-starttime)
    return (col,row, coll, roww)

def fear_update(col,row, col1, row1):  #Checks selected and adjacent pieces to see what is afraid/trapped
    global tiles,last_piece_checked_trapped

    for column, row in ( (col, row) , (col1, row1) ):
        for cc,rr in adjacentsquares(column,  row):
            if infear(tiles[cc][rr], cc, rr):
                last_piece_checked_trapped = False
                validmoves(cc, rr)
                if last_piece_checked_trapped:
                    afraid_pieces.discard( (cc,rr) ) 
                    afraid_and_trapped.add( (cc, rr) )
                elif not last_piece_checked_trapped: 
                    afraid_and_trapped.discard( (cc, rr) )
                    afraid_pieces.add( (cc,rr) ) 
                last_piece_checked_trapped = False
            else:
                afraid_and_trapped.discard( (cc, rr) )
                afraid_pieces.discard( (cc,rr) ) 


def makemove(col,row, col1, row1): #Makes moves without finalizing 
    global whitepieces, blackpieces, tiles, whitetomove
    tiles[col1][row1]=tiles[col][row]
    tiles[col][row]=None
    if not whitetomove:
        blackpieces[blackpieces.index((col,row))]=(col1, row1)
    elif whitetomove:
        whitepieces[whitepieces.index((col,row))]=(col1, row1)


def makefullmove(col,row, col1, row1):#Makes moves and finalizes
    global humantomove, whitetomove
    makemove(col,row, col1, row1 )
    fear_update(col, row, col1, row1)
    whitetomove = not whitetomove
    humantomove = not humantomove



def checkvictory():                         #Just checks if victory
    global wateringholes, whitepieces
    if len(set(wateringholes) & set(whitepieces))==3:
        victory("white")
    elif len(set(wateringholes) & set(blackpieces))==3:
        victory("black")


def victory(color):                         #What to do if victory
    global exists_victory , whitepieces, blackpieces
    exists_victory = True
    col_width = c.winfo_width()#COLS
    row_height = c.winfo_height()#ROWS
    if color=="white":
        print("WHITE WINS!")
        for (col,row) in whitepieces:
            c.create_image(col*col_width, row*row_height, image=c.coronet, anchor='nw')
    if color=="black":
        print("BLACK WINS!")
        for (col, row) in blackpieces:
            c.create_image(col*col_width, row*row_height, image=c.coronet, anchor='nw')



    #########################################################   Main functions

def UI(event):                          ##Main function for human interaction/click
    global SelectedSquare
    global whitepieces, blackpieces, wateringholes
    global whitetomove, humantomove
    global moves
    global centerturn, centerturnmoves
    global exists_victory


    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    col = event.x//col_width
    row = event.y//row_height

    if exists_victory:
        return
    elif centerturn:
        return
    elif humantomove and not SelectedSquare:
        check_click(col,row)
        return
    elif humantomove and ([col, row] not in validmoves(SelectedSquare[0], SelectedSquare[1])):
        print("Invalid Move.\n")
        SelectedSquare=None
        return
    elif humantomove:
        centerturnmoves = (SelectedSquare[0], SelectedSquare[1], col, row)
        centerturn = True
        SelectedSquare=None
        return


                

def AIturn():                                  #Main AI thread function
    global centerturn, centerturnmoves, humantomove, exists_victory
    while True:
        time.sleep(1)
        if exists_victory:
            pass
        elif centerturn:
            pass
        elif not humantomove:
            centerturnmoves = AImakemove()
            centerturn = True
        
        
 
def Center():                                 #Main Center thread that is between AI and UI
    global centerturn, centerturnmoves, exists_victory
    while True:
        time.sleep(.25)
        if exists_victory:
            pass
        elif centerturn:
          makefullmove(centerturnmoves[0], centerturnmoves[1], centerturnmoves[2], centerturnmoves[3])
          colorsquare(centerturnmoves[0], centerturnmoves[1])
          colorsquare(centerturnmoves[2], centerturnmoves[3])
          checkvictory()
          centerturnmoves = None
          centerturn = False
    





################################################### GUI stuff

    
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

def check_click(col,row):
    global SelectedSquare
    global tiles

    if not tiles[col][row]:
        print("Invalid Selection. Please select a piece.\n")
    elif (whitetomove and not (col, row) in whitepieces) :
        print("Invalid Selection. Please select a white piece.\n")
    elif (not whitetomove and not (col, row) in blackpieces) :
        print("Invalid Selection. Please select a black piece.\n")
    elif ((col,row) not in afraid_pieces) and tiles[col][row] and have_fear():
        print('You must move a newly scared piece first. \n')
    else:
        SelectedSquare=col, row

if __name__ == "__main__":

        root = tk.Tk()                               ##Tkinter Initialization                                                       
        c = tk.Canvas(root, width=600, height=600, borderwidth=1, background='white')
        c.grid(row=0,column=0)
        root.update_idletasks()
        loadgraphics()
        c.pack()
        checkerboard(c)
        c.pack()
        label=tk.Label()


        c.bind("<Button-1>", UI)                        #Human
        AIthread = threading.Thread(target=AIturn)      #AI
        Centerthread = threading.Thread(target=Center)  #Center


        AIthread.start()
        Centerthread.start()
        root.mainloop()
######
