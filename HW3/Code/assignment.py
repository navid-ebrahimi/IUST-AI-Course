from importlib.resources import contents


class Sudoku():
  def __init__(self, dim, fileDir):
    self.dim = dim
    self.expandedNode = 0
    with open(fileDir) as f:
      content = f.readlines()
      self.board = [list(x.strip().split(' ')) for x in content]
    self.rv = self.getRemainingValues()
  
  def solveSimpleBackTracking(self):
    location = self.getNextLocation()
    if (location[0] == -1):
      return True
    else:
      self.expandedNode += 1
      for choice in range(1, self.dim + 1):
        if (self.isSafe(location[0], location[1], str(choice))):
          self.board[location[0]][location[1]] = str(choice)
          if (self.solveSimpleBackTracking()):
            return True
          self.board[location[0]][location[1]] = '0'
    return False

  def CSP(self):
    location = self.getNextLocation()
    if (location[0] == -1):
      return True
    else:
      self.expandedNode += 1
      for choice in self.rv[location[0] * 9 + location[1]]:
        self.board[location[0]][location[1]] = str(choice)
        self.rv = self.getRemainingValues()
        if (self.CSP()):
          return True
        self.board[location[0]][location[1]] = '0'
    return False

  def getNextLocation(self):
    location = [-1,-1]
    for i in range(self.dim):
      for j in range(self.dim):
        if (self.board[i][j] == '0'):
          location[0] = i
          location[1] = j
          return location

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
  result.solveSimpleBackTracking()
  result.CSP()
  for i in range(result.dim):
    print(result.board[i])