import time
t0= time.clock()

def printGrid(grid):
    for c in range(9):
        for r in range(9):
            print(grid[c][r], end = " ")
            if((r+1)%3==0 and r+1<9):
                print("|| ", end = "")
        print()
        if((c+1)%3==0 and c+1<9):
                print("-----------------------")

def inCol(grid, col, num):
    for cell in range(9):
        if(isinstance(grid[col][cell], list)):
            for val in grid[col][cell]:
                if(val == num):
                    return True 
        else:
            if(grid[col][cell] == num):
                return True
    return False

def inRow(grid, row, num):
    for cell in range(9):
        if(isinstance(grid[cell][row], list)):
            for val in grid[cell][row]:
                if(val == num):
                    return True
        else:
            if(grid[cell][row] == num):
                return True
    return False

def inBlock(grid, row, col, num):
    row = row // 3
    col = col // 3
    for c in range(3):
        for r in range(3):
            if(isinstance(grid[(col*3) + c][(row*3) + r], list)):
                for val in grid[(col*3) + c][(row*3) + r]:
                    if(val == num):
                        return True
            else:
                if(grid[(col*3) + c][(row*3) + r] == num):
                 return True
    return False

def fillWithPencil(grid):
    newgrid = [[0 for x in range(9)]for y in range(9)]
    for col in range(9):
        for row in range(9):
            if(grid[col][row] == 0):
                newgrid[col][row] = []
                for i in range(9):
                    if(not inCol(grid, col, i+1) and not inRow(grid, row, i+1) and not inBlock(grid, row, col, i+1)):
                        newgrid[col][row].append(i+1)
            else:
                newgrid[col][row] = grid[col][row]
    return newgrid

def delInCol(grid, col, num):
    for cell in range(9):
        if(isinstance(grid[col][cell], list)):
            for val in grid[col][cell]:
                if(val == num):
                    grid[col][cell].remove(val)
                    break

def delInRow(grid, row, num):
    for cell in range(9):
        if(isinstance(grid[cell][row], list)):
            for val in grid[cell][row]:
                if(val == num):
                    grid[cell][row].remove(val)
                    break

def delInBlock(grid, row, col, num):
    row = row // 3
    col = col // 3
    for c in range(3):
        for r in range(3):
            if(isinstance(grid[(col*3) + c][(row*3) + r], list)):
                for val in grid[(col*3) + c][(row*3) + r]:
                    if(val == num):
                        grid[(col*3) + c][(row*3) + r].remove(val)
                        break

def isSolved(grid):
    for col in range(9):
        for row in range(9):
            if(isinstance(grid[col][row], list)):
                return False
            else:
                val = grid[col][row]
                grid[col][row] = 0
                if(inCol(grid, col, val) or inRow(grid, row, val) or inBlock(grid, row, col, val)):
                    grid[col][row] = val
                    return False
                else:
                    grid[col][row] = val
    return True

def updateAndClear(newgrid, col, row, val):
    newgrid[col][row] = val
    delInCol(newgrid, col, val)
    delInRow(newgrid, row, val)
    delInBlock(newgrid, row, col, val)
    if(not isSolved(newgrid)):
        fixWithPen(newgrid)

def fixWithPen(grid):
    for col in range(9):
        for row in range(9):
            if(isinstance(grid[col][row], list)):
                if(len(grid[col][row]) == 1):
                    val = grid[col][row][0]
                    updateAndClear(grid, col, row, val)
                else:
                    possible = grid[col][row]
                    grid[col][row] = 0
                    for val in possible:
                        if(not inCol(grid, col, val) or not inRow(grid, row, val) or not inBlock(grid, row, col, val)):
                            updateAndClear(grid, col, row, val)
                    if(grid[col][row] == 0):
                        grid[col][row] = possible

def setColVal(grid, col, at, val):
    for cell in range(9):
        if(grid[col][cell] == at):
            grid[col][cell] = val

def setRowVal(grid, row, at, val):
    for cell in range(9):
        if(grid[cell][row] == at):
            grid[cell][row] = val

def setBlockVal(grid, row, col, at, val):
    row = row // 3
    col = col // 3
    for c in range(3):
        for r in range(3):
            if(grid[(col*3) + c][(row*3) + r] == at):
                grid[(col*3) + c][(row*3) + r] = val

def fixPossibleWithPencil(grid):
    for col in range(9):
        for row in range(9):
            if(isinstance(grid[col][row], list)):
                preemtiveSet = grid[col][row][:]
                lenOfPreemptive = len(grid[col][row])
                cCount = 0
                for cell in range(9):
                    if(grid[col][cell] == preemtiveSet):
                        cCount += 1
                rCount = 0
                for row in range(9):
                    if(grid[cell][row] == preemtiveSet):
                        rCount += 1
                bCol = col//3
                bRow = row//3
                bCount = 0
                for c in range(3):
                    for r in range(3):
                        if(grid[(bCol*3) + c][(bRow*3) + r] == preemtiveSet):
                            bCount += 1
                if(cCount == lenOfPreemptive):
                    setColVal(grid, col, preemtiveSet, 0)
                    for val in preemtiveSet:
                        delInCol(grid, col, val)
                if(rCount == lenOfPreemptive):
                    setRowVal(grid, row, preemtiveSet, 0)
                    for val in preemtiveSet:
                        delInRow(grid, row, val)
                if(bCount == lenOfPreemptive):
                    setBlockVal(grid, row, col, preemtiveSet, 0)
                    for val in preemtiveSet:
                        delInBlock(grid, row, col, val)
                setColVal(grid, col, 0, preemtiveSet)
                setRowVal(grid, row, 0, preemtiveSet)
                setBlockVal(grid, row, col, 0, preemtiveSet)

def isLocationSafe(grid,row,col,num):
    return not inRow(grid,row,num) and not inCol(grid,col,num) and not inBlock(grid,row,col,num)

def findEmptyLocation(grid,cell): 
    for col in range(9): 
        for row in range(9): 
            if(grid[col][row]==0): 
                cell[0]=col 
                cell[1]=row 
                return True
    return False

def backTrace(grid):
    cell=[0,0]
    if(not findEmptyLocation(grid,cell)):
        return True
    col=cell[0]
    row=cell[1]
    for num in range(1,10):
        if(isLocationSafe(grid,row,col,num)):
            grid[col][row]=num
            if(backTrace(grid)):
                return True
            grid[col][row]=0
    return False

def sudokuSolve():
    grid=[[4,0,0,0,0,0,0,1,0],
	  [0,0,0,4,0,2,3,0,0],
	  [8,3,6,0,1,0,0,0,0], 
	  [2,0,0,0,6,0,0,5,7], 
	  [0,9,0,5,0,0,6,0,1], 
	  [0,0,7,1,0,0,0,0,0], 
	  [0,0,0,0,8,6,0,0,3], 
	  [7,0,0,0,0,0,0,0,0], 
	  [6,4,0,0,7,0,0,0,2]]

    newgrid = fillWithPencil(grid)
    fixPossibleWithPencil(newgrid)
    fixWithPen(newgrid)
    fixPossibleWithPencil(newgrid)
    fixWithPen(newgrid)
    fixPossibleWithPencil(newgrid)
    fixWithPen(newgrid)
    for c in range(9):
        for r in range(9):
            if(isinstance(newgrid[c][r], list)):
                newgrid[c][r] = 0
    if(backTrace(newgrid)):
        printGrid(newgrid)
    else:
        print("no solution exists")
    
sudokuSolve()
t1 = time.clock() - t0
print("Time elapsed: ", t1)
