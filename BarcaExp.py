import tkinter as tk


# Set number of rows and columns
ROWS = 10
COLS = 10
SelectedSquare= None
# Create a grid of None to store the references to the tiles
tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]
pieces=["wl", "wm", "we", "bl", "bm", "be"]
tiles[3][8] = tiles[6][8] = "wl"
tiles[4][8] = tiles[5][8] = "wm"
tiles[4][9] = tiles[5][9] = "we"

tiles[3][1] = tiles[6][1] = "bl"
tiles[4][1] = tiles[5][1] = "bm"
tiles[4][0] = tiles[5][0] = "be"

def callback(event):
    global SelectedSquare
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
        else:
            SelectedSquare=col, row
            print(validmoves(col, row))
    else:
         if [col, row] in validmoves(SelectedSquare[0], SelectedSquare[1]):
         #if not tiles[col][row]:
            tiles[col][row]=tiles[SelectedSquare[0]][SelectedSquare[1]]
            tiles[SelectedSquare[0]][SelectedSquare[1]]=None
            #print("Coloring Coloumn, row" +str(col)+str(row)+tiles[col][row])
            colorsquare(col, row)
            colorsquare(SelectedSquare[0], SelectedSquare[1])
            SelectedSquare=None
         else:
             print("Invalid Move.\n")
             SelectedSquare=None

def validmoves(col, row):
    moves=[]
    piece=tiles[col][row]
    colt=col
    rowt=row
    #Lion's valid moves:::::::::::::::::
    if piece=="wl" or piece=="bl" or piece=="be" or piece=="we":
        colt+=1
        rowt+=1
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            colt+=1
            rowt+=1
        colt=col-1
        rowt=row+1
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            colt-=1
            rowt+=1

        colt=col+1
        rowt=row-1
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            colt+=1
            rowt-=1
        colt=col-1
        rowt=row-1
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            colt-=1
            rowt-=1
        colt=col+1
        rowt=row
    #Mouse's Valid Moves::::::::::::;
    if piece=="wm" or piece=="bm" or piece=="be" or piece=="we":
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            colt+=1
        colt=col-1
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            colt-=1
        colt=col
        rowt=row-1
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            rowt-=1
        rowt=row+1
        while colt in range(COLS) and rowt in range(ROWS) and not tiles[colt][rowt]:
            moves.append([colt, rowt])
            rowt+=1

    return moves

def colorsquare(col, row):
    col_width = c.winfo_width()//COLS
    row_height = c.winfo_height()//ROWS
    if not tiles[col][row]:
        if (row+col)%2==0:
            c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="black")
        else:
            c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="white")
        return 
    if(tiles[col][row]=="wl"):
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="green")
    elif(tiles[col][row]=="wm"):
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="red")
    elif(tiles[col][row]=="we"):
        c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="blue")
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
c.pack()
checkerboard(c)
c.bind("<Button-1>", callback)

root.mainloop()