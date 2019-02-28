#!/usr/bin/env python
# coding: utf-8

# # Sudoku Solver Exact Cover Problem Algorithm X

# EXAMPLES OF INITIAL SUDOKUS TO SOLVE
sudoku_ex1 = "001900008600085030007060100034090000000504000000010420005070900010840007700009200"
sudoku_ex2 = "2004403002411403"
sudoku_ex3 = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

# MODULES
import numpy as np
import matplotlib.pyplot as plt


# DEFINE VARIABLES
n = 9
sudoku = sudoku_ex3




# From the example, reshape it into a numpy array of 9x9
def reshape(inline_matrix):
    return np.array(list(inline_matrix), dtype=int).reshape((n,n))




# CREATE THE COVER MATRIX 
constrains = 4

# The columns are the constrains (in our case 4 constrains * 9*9 possibilities))
columns = constrains*n*n

# The rows are possible solutions (number,row,column,region)
rows = n*n*n

cover = np.zeros((rows,columns), dtype=int)




# Get the region of the element
def number_region(row, column, n):
    m = np.floor(np.sqrt(n))
    h = np.floor(row / m)
    w = np.floor(column / m)
    return int(m*h + w + 1)




# POPULATE THE COVER WITH ALL THE 1s
c = [0,n*n,2*n*n,3*n*n]
cover_row = -1
for row in range(n):
    for column in range(n):
        for number in range(n):
            cover_row += 1
            column1 = c[0] + column + row*n
            cover[cover_row, column1] = 1
            column2 = c[1] + number + row*n
            cover[cover_row, column2] = 1
            column3 = c[2] +number + column*n
            cover[cover_row, column3] = 1
            region = number_region(row,column,n)
            column4 = c[3] + number + (region-1)*n
            cover[cover_row, column4] = 1

def get_row(row,column,number):
    index = n*n*row + n*column + number - 1
    return index


# Removal of the kown elements in the inital matrix
# Get the row and column indexes of the elements different than 0
initial = reshape(sudoku)
matrix = np.meshgrid(range(n), range(n))
values = [get_row(i,j,initial[i,j]) for i,j  in zip(matrix[1].ravel(), matrix[0].ravel()) if initial[i,j] != 0]
print(values)


# ### ALGORITHM X IMPLEMENTATION

# Define the matrix
constraint = np.copy(cover)
solution = np.zeros_like(cover)
solution_values = []
solution_r = 0


# Add the known values to the solution and remove them from the constraint
for index_row in values:
    row = constraint[index_row,:]
    # Add the line to the solution
    solution[solution_r,:] = row
    solution_r += 1
    solution_values.append(index_row)
    # Delete all the rows that satisgy any of the constrains of the selected row
    ones = np.where(row > 0)[0]
    for one in ones:
        # Get the index of the rows with ones in the same columns
        partners = np.where(constraint[:,one]>0)[0]
        if(len(partners)>0):
            for partner in partners:
                constraint[partner,:] = 0
        constraint[:,one] = 0
    constraint[index_row,:] = 0


while(len(solution_values) < n*n):
    # Get the counter of the columns
    counter = np.sum(constraint, axis=0)
    # Get the columns where there are no ones in the solution
    sol_counter = np.sum(solution, axis=0)
    condition = np.where(sol_counter > 0)[0]
    if len(condition)==0:
        print("There is no condition")
        index_column = 0
    else:
        # from the possible solutions, get the one with less ones in its column
        if(np.max(counter)==0):
            print("Every column is empty")
            break
        min_col = np.min(counter[np.nonzero(counter)])
        possible = np.where(counter==min_col)[0]
        if(len(possible)==0):
            break
        else:
            for p in possible:
                if(p not in condition):
                    index_column = p
                    break
    # From that column, get the first row with a 1 in it
    column = constraint[:,index_column]
    row_condition = np.where(column > 0)[0]
    if(len(row_condition)>0):
        index_row = row_condition[0]
    else:
        print('row condition error')
        break
    row = constraint[index_row,:]
    # Add the line to the solution
    solution[solution_r,:] = row
    solution_r += 1
    solution_values.append(index_row)
    # Delete all the rows that satisgy any of the constrains of the selected row
    ones = np.where(row > 0)[0]
    for one in ones:
        # Get the index of the rows with ones in the same columns
        partners = np.where(constraint[:,one]>0)[0]
        if(len(partners)>0):
            for partner in partners:
                constraint[partner,:] = 0
        constraint[:,one] = 0
    constraint[index_row,:] = 0

# Transfrom index to value and position
def return_position(index):
    row = int(np.floor(index/(n*n)))
    column = int(np.floor(index/n)-row*n)
    value = int(index - n*n*row - n*column)+1
    return row,column,value

# Express the solution
sudoku_sol = np.zeros((n,n), dtype=int)
for element in solution_values:
    r,c,v = return_position(element)
    sudoku_sol[r,c] = v
print(sudoku_sol)

