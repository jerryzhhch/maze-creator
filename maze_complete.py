#Authors:
#Brian Cabantug: bcabantug@csu.fullerton.edu
#Hancheng Zhou: jerryzhhch@csu.fullerton.edu
#Mason Guzman-Sanchez: masongs@csu.fullerton.edu

#Description: This python script generates a 2d maze using binary space partitioning
#User inputs size of the maze (ideally equivalent row and columns) and the maze is generated and outputted
#with the marked starting and end points 

# library imports
import math
import sys
import random

# introduction
welcome = "Welcome to the maze generation. \n"

# ask for user input
row_num = input("enter number of row: ")
col_num = input("enter number of col: ")
while row_num == '0' or col_num == '0':
        print("Wrong maze. Try some other numbers.")
        row_num = input("enter number of row: ")
        col_num = input("enter number of col: ")
row_line = 2 * int(row_num) + 1
col_line = 2 * int(col_num) + 1

# change input to 2n for algorithm reasons
rowsI = row_line - 1
columnsI = col_line - 1
# initial maze with 0s
maze = []
for x in range(row_line):
    maze.append(["O"] * col_line)
# marks the cells of the maze
for x in range(row_line):
    for y in range(col_line):
        if (x % 2 != 0) and (y % 2 != 0):
            maze[x][y] = ' '
# mark corners
for x in range(row_line):
    for y in range(col_line):
        if (x % 2 == 0) and (y % 2 == 0):
            maze[x][y] = '+'
# marks the walls/borders in the maze
for i in range(row_line):
    for j in range(col_line):
        if i%2 == 0 and j%2 !=0:
            maze[i][j] = "-"
        elif i%2 !=0 and j%2 == 0:
            maze[i][j] = "|"
# mark starting point and ending point
for row in maze:
    maze[1][1] = 'S'
    maze[row_line - 2][col_line - 2] = 'X'


# defined function for printing the maze
def print_maze(maze):
    for row in maze:
        print(" ".join(row))

print_maze(maze)
# variable to hold coordinates for portals when generating maze
mazePortals = []


# node class for the Binary space partition tree (eventually all leaves will be in order and will be able to draw out the maze)
class Node:
    #node constructor
    def __init__(self, beginHRange, endHRange, beginVRange, endVRange, left=None, right=None):
        self.coordinates = [[beginHRange,endHRange], [beginVRange,endVRange]]
        self.split1 = left #left child 
        self.split2 = right #right child



#recursive function to construct the BSP tree
def binarySP(rows, columns, currNode, pList):
    #choose direction of partition
    selectRandSplit = random.randint(1,2)

    #if split happens horizontally
    if selectRandSplit == 1:
       #call horizontal split            
       horizontalSplit(currNode,pList)     
       

    #if split happens vertically    
    elif selectRandSplit == 2:
        #call vertical split
        verticalSplit(currNode,pList)
       


#function to define horizontal split
def horizontalSplit(nodeToSplit, portalList):            
            
    #if there is only one possible split between the current section (cell length = 4)
    if nodeToSplit.coordinates[0][1]-nodeToSplit.coordinates[0][0] == 4:
        
        #set it so that the split is equivalent of to have the cell coordinate be size 2 for piurpose of maze output
        #lower child
        nodeToSplit.split1=Node(nodeToSplit.coordinates[0][0], nodeToSplit.coordinates[0][0]+2, nodeToSplit.coordinates[1][0], nodeToSplit.coordinates[1][1])
        #upper child
        nodeToSplit.split2=Node(nodeToSplit.coordinates[0][0]+2, nodeToSplit.coordinates[0][1], nodeToSplit.coordinates[1][0], nodeToSplit.coordinates[1][1])
        #find the cross section of wall to remove to act as the portal
        port = random.randrange(nodeToSplit.coordinates[1][0]+1, nodeToSplit.coordinates[1][1],2)
        #sets the portal coordinate
        portalCoord = [port,nodeToSplit.coordinates[0][0]+2]
        #adds it to the list of portals
        portalList.append(portalCoord)


        #start the recursive calls for the child nodes to develop the granchildren
        binarySP(nodeToSplit.split1.coordinates[0][1], nodeToSplit.split1.coordinates[1][1], nodeToSplit.split1, portalList)
        binarySP(nodeToSplit.split2.coordinates[0][1], nodeToSplit.split2.coordinates[1][1], nodeToSplit.split2, portalList)



    #if the split selected is no longer possible
    elif nodeToSplit.coordinates[0][1]-nodeToSplit.coordinates[0][0]==2:
        #check if the current node still has range to split for opposite direction
        if nodeToSplit.coordinates[1][1] - nodeToSplit.coordinates[1][0] != 2:
            #call split function to split opposite direction for region (horizontal -> vertical)
            verticalSplit(nodeToSplit, portalList)


            
            
    #covers final case where cell can no longer be split upon itself
    elif nodeToSplit.coordinates[0][1]-nodeToSplit.coordinates[0][0]==2 and nodeToSplit.coordinates[1][1]-nodeToSplit.coordinates[1][0]==2:
        #then stop the split and return to previous parent node to continue the split function
        return

    #covers other case for general range    
    else:
        #check to make sure that origin line coordinate ranges are not selected for the split (ex: [0][0])
        tmpLower = 2 #2 selected as default to avoid selecting borders/origin
        if(nodeToSplit.coordinates[0][0]!=0): #otherwise set lower as the regular lower region
            tmpLower = nodeToSplit.coordinates[0][0]

        #split the region
        randSplit = random.randrange(tmpLower, nodeToSplit.coordinates[0][1],2)
        while randSplit == tmpLower: #if split coordinate is the same the lowest range ie 2 == 2
            #reinitialize the split until it finds it otherwise
            randSplit = random.randrange(tmpLower, nodeToSplit.coordinates[0][1],2)        

        #picking the portal to open in between the two regions and push to the portals list
        port = random.randrange(nodeToSplit.coordinates[1][0]+1, nodeToSplit.coordinates[1][1],2)

        #assign it and then append it to the portalList
        portalCoord = [port, randSplit]
        portalList.append(portalCoord)

        #set the two nodes child nodes
        #lower
        nodeToSplit.split1 = Node(nodeToSplit.coordinates[0][0],randSplit,nodeToSplit.coordinates[1][0] ,nodeToSplit.coordinates[1][1])
        #upper
        nodeToSplit.split2 = Node(randSplit, nodeToSplit.coordinates[0][1],nodeToSplit.coordinates[1][0] ,nodeToSplit.coordinates[1][1])

        #start the recursive calls for the child nodes to develop the granchildren
        #left child
        binarySP(nodeToSplit.split1.coordinates[0][1], nodeToSplit.split1.coordinates[1][1], nodeToSplit.split1, portalList)
        #right child
        binarySP(nodeToSplit.split2.coordinates[0][1], nodeToSplit.split2.coordinates[1][1], nodeToSplit.split2, portalList)


#function to define vertical split
def verticalSplit(nodeToSplit, portalList):
    #if there is only one possible split between the current section (cell length = 2)
    if nodeToSplit.coordinates[1][1]-nodeToSplit.coordinates[1][0] == 4:
        #set it so that the split is equivalent of to have the cell coordinate be size 1
        #lower
        nodeToSplit.split1=Node(nodeToSplit.coordinates[0][0], nodeToSplit.coordinates[0][1], nodeToSplit.coordinates[1][0], nodeToSplit.coordinates[1][0]+2)
        #upper
        nodeToSplit.split2=Node(nodeToSplit.coordinates[0][0], nodeToSplit.coordinates[0][1], nodeToSplit.coordinates[1][0]+2, nodeToSplit.coordinates[1][1])
        
        #find the cross section of wall to remove to act as the portal
        port = random.randrange(nodeToSplit.coordinates[0][0]+1, nodeToSplit.coordinates[0][1],2)
        #set the portal 
        portalCoord = [nodeToSplit.coordinates[1][0]+2,port]
        #append the portal to the global portal list
        portalList.append(portalCoord)



        #start the recursive calls for generating the next child nodes
        #left child
        binarySP(nodeToSplit.split1.coordinates[0][1], nodeToSplit.split1.coordinates[1][1], nodeToSplit.split1,portalList)
        #right child
        binarySP(nodeToSplit.split2.coordinates[0][1], nodeToSplit.split2.coordinates[1][1], nodeToSplit.split2, portalList)

    #if the split selected causes it to split on itself/ no more possible splits
    elif nodeToSplit.coordinates[1][1]-nodeToSplit.coordinates[1][0]==2:
        #check if the current node still has range to split for opposite direction
        if nodeToSplit.coordinates[0][1] - nodeToSplit.coordinates[0][0] != 2:
            #call split function to split opposite direction for region (vertical -> horizontal)
            horizontalSplit(nodeToSplit, portalList)



    #if region is already minimum size/ no longer splittable
    elif nodeToSplit.coordinates[1][1]-nodeToSplit.coordinates[1][0] == 2 and nodeToSplit.coordinates[0][1]-nodeToSplit.coordinates[0][0]==2:
        #then stop the split and return to previous parent node to continue the split
        return
            
    else:
        #check to make sure that origin line coordinate ranges are not selected for the split (ex: [0][0])
        tmpLower = 2 #default set for 2 to avoid selecting border
        if(nodeToSplit.coordinates[1][0]!=0): #otherwise, set lower for region if not border
            tmpLower = nodeToSplit.coordinates[1][0]
            
        #get the random coordinate between the range of the current node to split between for the children
        randSplit = random.randrange(tmpLower, nodeToSplit.coordinates[1][1],2)
            #check to make sure the lower boundary is not selected as the split and repick split if it is selected
        while randSplit == tmpLower:
            randSplit = random.randrange(tmpLower, nodeToSplit.coordinates[1][1],2)
        

        #portal selection in the split
        port = random.randrange(nodeToSplit.coordinates[0][0]+1, nodeToSplit.coordinates[0][1],2)

        #assign it and then append it to the portalList
        portalCoord = [randSplit,port]
        portalList.append(portalCoord)

        #set left child
        nodeToSplit.split1 = Node(nodeToSplit.coordinates[0][0], nodeToSplit.coordinates[0][1],nodeToSplit.coordinates[1][0] ,randSplit)
        #set right child
        nodeToSplit.split2 = Node(nodeToSplit.coordinates[0][0], nodeToSplit.coordinates[0][1],randSplit,nodeToSplit.coordinates[1][1])

        #start the recursive calls for generating the next child nodes
        #left child
        binarySP(nodeToSplit.split1.coordinates[0][1], nodeToSplit.split1.coordinates[1][1], nodeToSplit.split1, portalList)
        #right child
        binarySP(nodeToSplit.split2.coordinates[0][1], nodeToSplit.split2.coordinates[1][1], nodeToSplit.split2,portalList)


#start of actual main function
#sets root node
treeRoot = Node(0, rowsI, 0, columnsI)
#calls the binary space partition function (input is # of rows, # of columns, root node, and global portal list)
binarySP(rowsI, columnsI, treeRoot, mazePortals)

#print the portal list
print("Portal list (reads as from 0 to 2n):")
for z in mazePortals:
    print(z)

print("")

#place the portals in the list of the maze to print
for coor in mazePortals:
    y = coor[0]
    x = coor[1]

    maze[x][y] = " "

#final output of the maze
print_maze(maze)
