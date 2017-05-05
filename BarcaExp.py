import tkinter as tk
import PIL.ImageTk
from PIL import Image, ImageTk

whitetomove=True
# Set number of rows and columns
ROWS = 10
COLS = 10
SelectedSquare= None
# Create a grid of None to store the references to the tiles
tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]
pieces=["wl", "wm", "we", "bl", "bm", "be"]
whitepieces=[[3,8], [6,8], [4,8], [5,8], [4,9], [5,9]]
blackpieces=[[3,1], [6,1], [4,1], [5,1], [4,0], [5,0]]

tiles[3][8] = tiles[6][8] = "wl"
tiles[4][8] = tiles[5][8] = "wm"
tiles[4][9] = tiles[5][9] = "we"

tiles[3][1] = tiles[6][1] = "bl"
tiles[4][1] = tiles[5][1] = "bm"
tiles[4][0] = tiles[5][0] = "be"

def callback(event):
    global SelectedSquare
    global whitepieces
    global blackpieces
    global whitetomove
    # Get rectangle diameters
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    # Calculate column and row number
    col = event.x//col_width
    row = event.y//row_height
 
    # If the tile is not filled, create a rectangle
    print("Row:: " + str(row) + "\nCol:: " + str(col) +'\n')
    if not SelectedSquare:
        if not tiles[col][row]:
            print("Invalid Selection. Please select a piece.\n")
        elif whitetomove and not [col, row] in whitepieces:
            print("Invalid Selection. Please select a white piece.\n")
        elif not whitetomove and not [col, row] in blackpieces:
            print("Invalid Selection. Please select a black piece.\n")
        else:
            SelectedSquare=col, row
            print(validmoves(col, row))
            #print("White can make "+ str(totalmoves(whitepieces)) + " moves")
            #print("Black can make "+ str(totalmoves(blackpieces)) + " moves")
    else:
         if [col, row] in validmoves(SelectedSquare[0], SelectedSquare[1]):

            tiles[col][row]=tiles[SelectedSquare[0]][SelectedSquare[1]]
            tiles[SelectedSquare[0]][SelectedSquare[1]]=None
            if whitetomove:
                whitepieces[whitepieces.index([SelectedSquare[0],SelectedSquare[1]])]=[col, row]
                whitetomove=False
            else:
                blackpieces[blackpieces.index([SelectedSquare[0],SelectedSquare[1]])]=[col, row]
                whitetomove=True
            colorsquare(col, row)
            colorsquare(SelectedSquare[0], SelectedSquare[1])
            SelectedSquare=None
         else:
             print("Invalid Move.\n")
             SelectedSquare=None

def totalmoves(pieces):
    counter=0
    for [col, row] in pieces:
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
def infear(piece, col, row):
    for [c, r] in adjacentsquares(col, row):
        if tiles[c][r]==fears(piece):
            return True
    return False
def validmoves(col, row):
    moves=[]
    piece=tiles[col][row]
    unafraid=True
    colt=col
    rowt=row
    #Lion's valid moves:::::::::::::::::
    for rowd in (-1,0,1):
        for cold in (-1,0,1):
            if (rowd ==0 == cold):
                pass
            elif (abs(cold) == abs(rowd) and piece=="wl" or piece=="bl" or piece=="be" or piece=="we") or\
                 ((cold ==0 or rowd ==0 ) and piece=="wm" or piece=="bm" or piece=="be" or piece=="we"):
                colt +=cold
                rowt += rowd
                while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]: 
                    if not infear(piece, colt, rowt):
                        moves.append([colt, rowt])
                    colt+=cold
                    rowt+=rowd
            unafraid=True
            colt = col
            rowt = row

    return moves
def loadgraphics():
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    img = Image.open("whitelionwhitesquare.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.whitelion=whitelion = ImageTk.PhotoImage(img)

    img = Image.open("whitemousewhitesquare.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.whitemouse=whitemouse = ImageTk.PhotoImage(img)

    img = Image.open("whiteelephantwhitesquare.gif")
    img = img.resize((col_width,row_height), Image.ANTIALIAS)
    c.whiteelephant=whiteelephant = ImageTk.PhotoImage(img)

def colorsquare(col, row):
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    #whitelion = tk.PhotoImage(file = './b185f0114f241d9bd5471f0c94c9d5a7.gif')
    #scale_w = col_width//whitelion.width()
    #scale_h = row_height//whitelion.height()

    if not tiles[col][row]:
        if (row+col)%2==0:
            c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="darkblue")  
        else:
            c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="lightblue")
       # return 
    if(tiles[col][row]=="wl"):
        c.create_image(col*col_width, row*row_height, image=c.whitelion, anchor='nw')
    elif(tiles[col][row]=="wm"):
        c.create_image(col*col_width, row*row_height, image=c.whitemouse, anchor='nw')
    elif(tiles[col][row]=="we"):
        c.create_image(col*col_width, row*row_height, image=c.whiteelephant, anchor='nw')
    elif(tiles[col][row]=="bl"):
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="yellow")
    elif(tiles[col][row]=="bm"):
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="brown")
    elif(tiles[col][row]=="be"):
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="purple")
# Create the window, a canvas and the mouse click event binding
def checkerboard(can):
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    for row in range(10):
        for col in range(10):
            colorsquare(col, row)
# Create the window, a canvas and the mouse click event binding
root = tk.Tk()
c = tk.Canvas(root, width=500, height=500, borderwidth=5, background='white')
c.grid(row=0,column=0)
root.update_idletasks()
loadgraphics()
c.pack()

checkerboard(c)

c.pack()
c.bind("<Button-1>", callback)
label=tk.Label()

root.mainloop()
