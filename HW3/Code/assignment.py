from importlib.resources import contents
import time
from turtle import position

class Sudoku():
  def __init__(self, dim, fileDir):
    self.dim = dim
    self.expandedNode = 0
    with open(fileDir) as f:
      content = f.readlines()
      self.board = [list(x.strip().split(' ')) for x in content]
    self.rv = self.getRemainingValues()
  
  def solveSimpleBackTracking(self):
    location = self.getNextLocation('SBT')
    i = location[0]
    j = location[1]
    if (i == -1):
      return True
    else:
      self.expandedNode += 1
      for choice in range(1, self.dim + 1):
        if (self.isSafe(i, j, str(choice))):
          self.board[i][j] = str(choice)
          if (self.solveSimpleBackTracking()):
            return True
          self.board[i][j] = '0'
    return False

  def CSP(self):
    location = self.getNextLocation('CSP')
    i = location[0]
    j = location[1]
    if (i == -1):
      return True
    else:
      self.expandedNode += 1
      position = i * self.dim + j
      for choice in self.rv[position]:
        self.board[i][j] = str(choice)
        # self.getRemainingValues()
        self.remove_inconsistenct_values(i, j, choice)
        if (self.CSP()):
          return True
        self.board[i][j] = '0'
        self.getRemainingValues()
    return False

  def remove_inconsistenct_values(self, row, col, choice):
    for i in range(self.dim):
      if (self.board[row][i] == '0' and choice in self.rv[row * self.dim + i]):
        self.rv[row * self.dim + i].remove(choice)
    
    for i in range(self.dim):
      if (self.board[i][col] == '0' and choice in self.rv[i * self.dim + col]):
        self.rv[i * self.dim + col].remove(choice)

    boxRow = row - row % 3
    boxCol = col - col % 3

    for i in range(3):
      for j in range(3):
        if (self.board[boxRow + i][boxCol + j] == '0' and choice in self.rv[(boxRow + i) * self.dim + (boxCol + j)]):
          self.rv[(boxRow + i) * self.dim + (boxCol + j)].remove(choice)

  def getNextLocation(self, type):
    location = [-1,-1]
    minDomain = self.dim + 1
    for i in range(self.dim):
      for j in range(self.dim):
        if (type == 'SBT'):
          if (self.board[i][j] == '0'):
            location[0] = i
            location[1] = j
            return location
        elif (type == 'CSP'):
          if (self.board[i][j] == '0' and len(self.getDomain(i, j)) < minDomain):
            minDomain = len(self.getDomain(i, j))
            location[0] = i
            location[1] = j

    return location

  def isSafe(self, x, y, choice):
    if (choice in self.getDomain(x, y)):
      return True
    return False

  def getDomain(self, row, col):
    RVCell = [str(i) for i in range(1, self.dim + 1)]
    for i in range(self.dim):
      if (self.board[row][i] != '0'):
        if (self.board[row][i] in RVCell):
          RVCell.remove(self.board[row][i])
    
    for i in range(self.dim):
      if (self.board[i][col] != '0'):
        if (self.board[i][col] in RVCell):
          RVCell.remove(self.board[i][col])

    boxRow = row - row % 3
    boxCol = col - col % 3

    for i in range(3):
      for j in range(3):
        if (self.board[boxRow + i][boxCol + j] != '0'):
          if (self.board[boxRow + i][boxCol + j] in RVCell):
            RVCell.remove(self.board[boxRow + i][boxCol + j])
    
    return RVCell

  def getRemainingValues(self):
    RV = []
    for row in range(self.dim):
      for col in range(self.dim):
        if (self.board[row][col] != '0'):
          RV.append(['x'])
        else:
          RV.append(self.getDomain(row, col))
    
    return RV


if __name__ == '__main__':
  result = Sudoku(9, fileDir='fileDir.txt')
  now = time.time()
  result.solveSimpleBackTracking()
  # result.CSP()
  end = time.time()
  print(int((end - now) * 1000), 'ms')
  print(result.expandedNode, 'nodes expanded')
  for i in range(result.dim):
    print(result.board[i])