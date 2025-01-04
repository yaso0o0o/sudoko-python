import pygame

from game import findEmptyCell

def validBoard(board ,num ,cell):
    for i in range (len(board[0])) :
        if board[cell[0]][i] == num and cell[1] != i:
            return pygame.error 
  
    for i in range (len(board)):
        if board[i][cell[1]] == num and cell[0] != i :
            return pygame.error
            
    boxA = cell[0]
    boxB = cell[1]

    for i in range (boxA*3 , boxA*3+3):
        for j in range (boxB*3 , boxB*3+3):
            if board [i][j] == num and (i,j) != cell :
                return pygame.error

    return True                




def solveSudoko (board) :
    find = findEmptyCell(board)
    if not find :
        return True
    else:
        row ,col = find

    for i in range (1 ,10):
        if validBoard(board , i , (row,col))    :
            board [row][col]=i
            if solveSudoko(board):
                return True
            board[row][col]=0
    return False            