#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools



# this creates an array of tuples
def all_pairs(V1,V2):
    out = [] # will be array of tuples
    for d1 in V1.domain():
        for d2 in V2.domain():
            if (d1 != d2):
                out.append((d1,d2))
    return out

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a -1 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    
    #INITIALIZE VARS
    G,LR = initial_tenner_board
    #print("LR ",LR)
    V_array = [[0 for x in range(10)] for j in range(len(G))] # N of rows
    #print(V_array)
    #V_array[3][0] = 2000
    for i in range(len(G)):
        for j in range(10):
            if G[i][j] == -1: # domain should be 0-9
                V = Variable(str(i) + ' '+str(j),[x for x in range(10)])
                V_array[i][j] = V
            else:
               # print(i,j)
                V = Variable(str(i) + ' '+str(j),[G[i][j]]) #Domain is what's there
                V.assign(G[i][j])
                V_array[i][j] = V
    CS = CSP("Tenner Model 1",[V_array[z][y] for z in range(len(G)) for y in range(10)])
    # DO constraints
    #Start with differences
    N = len(G)
    for i in range(N):
        for j in range(10):
            #ADJ VER
            if i!= (N-1):
                C = Constraint("ADJ_VERT",[V_array[i][j],V_array[i+1][j]])
                C.add_satisfying_tuples(all_pairs(V_array[i][j],V_array[i+1][j]))
                CS.add_constraint(C)
            # ADJ DIAG
            if ((i!= (N-1)) and (j!= 9)):
                C = Constraint("DIAG",[V_array[i][j],V_array[i+1][j+1]])
                C.add_satisfying_tuples(all_pairs(V_array[i][j],V_array[i+1][j+1]))
                CS.add_constraint(C)
            #DIAG OTHER SIDE
            if ( (i!= (N-1)) and (j!= 0)):
                C = Constraint("DIAG",[V_array[i][j],V_array[i+1][j-1]])
                C.add_satisfying_tuples(all_pairs(V_array[i][j],V_array[i+1][j-1]))
                CS.add_constraint(C)
            #THIS DEALS WITH ROW CONSTRAINTS
            for k in range(j+1,10):
                C = Constraint("ROWS",[V_array[i][j],V_array[i][k]])
                # ADD ALL POSSIBLE VALUES
                C.add_satisfying_tuples(all_pairs(V_array[i][j],V_array[i][k]))
                CS.add_constraint(C)
    #SUM CONSTRAINT
    #GEN FUNCTION

    for I in range(10): # I Is column number
        #GEN_ALL(LR[I],[],0)
        L= [V_array[x][I].cur_domain() for x in range(N)]
        #print(L)
        C = Constraint("Sum of Col " + str(I),[V_array[i][I] for i in range(N)])
        for P in itertools.product(*L):
            if sum(P) == LR[I]:
                #print(P,LR[I])
                C.add_satisfying_tuples([P])
        CS.add_constraint(C)
        
    #print("mamatsh")
    # Now we have all the possibilityes
    return CS,V_array
    
    
##############################

def tenner_csp_model_2(initial_tenner_board):
    
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary 
       all-different constraints and binary not-equal constraints: all-different 
       constraints for the variables in each row, binary constraints for  
       contiguous cells (including diagonally contiguous cells), and n-nary sum 
       constraints for each column. 
       Each n-ary all-different constraint has more than two variables (some of 
       these variables will have a single value in their domain). 
       model_2 should create these all-different constraints between the relevant 
       variables.
    '''
    #INITIALIZE VARS
    G,LR = initial_tenner_board
    #print("LR ",LR)
    V_array = [[0 for x in range(10)] for j in range(len(G))] # N of rows
    #print(V_array)
    #V_array[3][0] = 2000
    for i in range(len(G)):
        for j in range(10):
            if G[i][j] == -1: # domain should be 0-9
                V = Variable(str(i) + ' '+str(j),[x for x in range(10)])
                V_array[i][j] = V
            else:
               # print(i,j)
                V = Variable(str(i) + ' '+str(j),[G[i][j]]) #Domain is what's there
                V.assign(G[i][j])
                V_array[i][j] = V
    CS = CSP("Tenner Model 2",[V_array[z][y] for z in range(len(G)) for y in range(10)])
    # DO constraints
    #Start with differences
    N = len(G)
    # function that generates all possible rows given domains, j specifies column
   # i=0, I may uncomment this
    POSSIB = []
    def all_rows(j,L):
        #print(j,L)
        if (j==10):
            POSSIB.append(tuple(L))
            return
        for d in V_array[i][j].domain():
            if ((d not in L) and (j<=9)): # check that the domain is not in row already
                L.append(d)
                all_rows(j+1,L)
                L.pop()
        return
    for i in range(N):
        all_rows(0,[]) # GENERATE ALL POSSIBLE ROWS (N-ARY)
        C = Constraint("ROW_N-ARY of " + str(i),[V_array[i][k] for k in range(10)])
        C.add_satisfying_tuples(POSSIB)
        #print(POSSIB)
        CS.add_constraint(C)
        POSSIB = []
        for j in range(10):
            #ADJ VER
            if i!= (N-1):
                C = Constraint("ADJ_VERT",[V_array[i][j],V_array[i+1][j]])
                C.add_satisfying_tuples(all_pairs(V_array[i][j],V_array[i+1][j]))
                CS.add_constraint(C)
            # ADJ DIAG
            if ((i!= (N-1)) and (j!= 9)):
                C = Constraint("DIAG",[V_array[i][j],V_array[i+1][j+1]])
                C.add_satisfying_tuples(all_pairs(V_array[i][j],V_array[i+1][j+1]))
                CS.add_constraint(C)
            #DIAG OTHER SIDE
            if ( (i!= (N-1)) and (j!= 0)):
                C = Constraint("DIAG",[V_array[i][j],V_array[i+1][j-1]])
                C.add_satisfying_tuples(all_pairs(V_array[i][j],V_array[i+1][j-1]))
                CS.add_constraint(C)
            
    #SUM CONSTRAINT
    #GEN FUNCTION
    for I in range(10): # I Is column number
        #GEN_ALL(LR[I],[],0)
        L= [V_array[x][I].cur_domain() for x in range(N)]
        #print(L)
        C = Constraint("Sum of Col " + str(I),[V_array[i][I] for i in range(N)])
        for P in itertools.product(*L):
            if sum(P) == LR[I]:
                #print(P,LR[I])
                C.add_satisfying_tuples([P])
        CS.add_constraint(C)
        
        
    return CS,V_array
        


