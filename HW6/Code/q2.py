from random import choice
import os
import math
import copy

player, opponent = 'X', 'O'
list_of_board = [(i,j) for i in range(3) for j in range(3)]

class state:
    def __init__(self, board, move=None, list_of_board=list_of_board):
        self.board = board
        self.children = []
        self.U = 0
        self.UCB = 0
        self.move = move
        self.N = 0
        self.parentN = 0
        self.parent = None
        self.list_of_moves = list_of_board
        self.win=0
        self.blank=0

def create_root_children(board, root):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                root.N += 1
                board[i][j] = opponent
                board_with_randomly_played = play_automatic(copy.deepcopy(board), opponent)
                child = state(copy.deepcopy(board), (i, j))
                child.list_of_moves = copy.deepcopy(root.list_of_moves)
                child.list_of_moves.remove((i, j))
                child.parent = root
                child.parentN = root.N
                child.N += 1
                if board_with_randomly_played or board_with_randomly_played == None:
                    child.U += 1
                elif not board_with_randomly_played:
                    child.U -= 1
                child.UCB = get_score(child)
                update_ucb_of_all_nodes(root)
                root.children.append(child)
                board[i][j] = '_'

def update_parents(node, num):
    if node.parent:
        node.parent.U += num
        node.parent.N += 1
        if (node.parent.parentN != 0):
            node.parent.UCB = get_score(node.parent)
        update_parents(node.parent, num)

def update_ucb_of_all_nodes(root):
    for i in range(len(root.children)):
        child = root.children[i]
        child.parentN = root.N
        child.UCB = get_score(child)
        if len(child.children) != 0:
            update_ucb_of_all_nodes(child)

def number_player_opponent(board):
    number_player = 0
    number_opponent = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == player:
                number_player += 1
            if board[i][j] == opponent:
                number_opponent += 1
            
    return number_player, number_opponent

def list_of_blanks(root):
    list_of_blanks = []
    for i in range(3):
        for j in range(3):
            if root.board[i][j] == '_':
                list_of_blanks.append((i, j))
    return list_of_blanks

def check_win(root, state):
    if (state == player):
        root.U -= 1
        update_parents(root, -1)
    elif (state == opponent):
        root.U += 1
        update_parents(root, 1)
    root.UCB = get_score(root)
    root.list_of_moves = []
    root.win = 1

def create_each_state(root):
    if (list_of_blanks(root) == []):
        root.blank = 1
        return
    if (determine_winner(root.board) == player and root.win == 0):
        check_win(root, player)
        return
    if (determine_winner(root.board) == opponent and root.win == 0):
        check_win(root, opponent)
        return
    number_player, number_opponent = number_player_opponent(root.board)
    if len(root.list_of_moves) == 0:
        try:
            n = 0
            for child in root.children:
                if (child.blank == 1 or child.win == 1):
                    n+=1
            if n == len(root.children):
                root.blank = 1
                root.win = 1
                return
            root.children = sorted(root.children, key=lambda x: x.UCB, reverse=True)
            for child in root.children:
                if (child.win == 0 and child.blank == 0):
                    if (len(list_of_blanks(child)) == 0):
                        if determine_winner(child.board) == player:
                            check_win(root, player)
                            return
                        elif determine_winner(child.board) == opponent:
                            check_win(root, opponent)
                            return
                    create_each_state(child)
                    break
        except:
            pass
        return
    else:
        child = state(copy.deepcopy(root.board))
        child.parent = root
        child.parentN = root.N
        child.N += 1
        sign = 0
        if (root.board[root.list_of_moves[0][0]][root.list_of_moves[0][1]] != '_'):
            child.move = list_of_blanks(root)[0]
            sign=1
        else:
            child.move = root.list_of_moves[0]
        num = 0
        if number_player == number_opponent:
            child.board[child.move[0]][child.move[1]] = player
            board_with_randomly_played = play_automatic(copy.deepcopy(child.board), player)
            if board_with_randomly_played and board_with_randomly_played != None:
                child.U -= 1
                num = -1
            elif not board_with_randomly_played or board_with_randomly_played == None:
                child.U += 1
                num = 1
        else:
            child.board[child.move[0]][child.move[1]] = opponent
            board_with_randomly_played = play_automatic(copy.deepcopy(child.board), opponent)
            if board_with_randomly_played or board_with_randomly_played == None:
                child.U += 1
                num=1
            elif not board_with_randomly_played and board_with_randomly_played != None:
                child.U -= 1
                num = -1

        child.list_of_moves = list_of_blanks(child)
        if (sign == 0):
            root.list_of_moves.remove(child.move)
        child.UCB = get_score(child)
        root.children.append(child)
        update_parents(child, num)
        return

def determine_winner(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            if (board[row][0] == opponent):
                return opponent
            return player

    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            if (board[0][col] == opponent):
                return opponent
            return player

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        if (board[0][0] == opponent):
            return opponent
        return player

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        if (board[0][2] == opponent):
            return opponent
        return player

    return None

def find_best_choice(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and not board[row][0] == '_'):
            if (board[row][2] == '_'):
                return [row, 2]
        if (board[row][0] == board[row][2] and not board[row][0] == '_'):
            if board[row][1] == '_':
                return [row, 1]
        if (board[row][2] == board[row][1] and not board[row][1] == '_'):
            if board[row][0] == '_':
                return [row, 0]
        
    for col in range(3):
        if (board[0][col] == board[1][col] and not board[0][col] == '_'):
            if board[2][col] == '_':
                return [2, col]
        if (board[0][col] == board[2][col] and not board[0][col] == '_'):
            if board[1][col] == '_':
                return [1, col]
        if (board[2][col] == board[1][col] and not board[1][col] == '_'):
            if board[0][col] == '_':
                return [0, col]

    if (board[0][2] == board[1][1] and not board[0][2] == '_'):
        if board[2][0] == '_':
            return [2,0]
    if (board[0][2] == board[2][0] and not board[0][2] == '_'):
        if board[1][1] == '_':
            return [1,1]
    if (board[2][0] == board[1][1] and not board[1][1] == '_'):
        if board[0][2] == '_':
            return [0,2]

    if (board[0][0] == board[1][1] and not board[0][0] == '_'):
        if board[2][2] == '_':
            return [2,2]
    if (board[0][0] == board[2][2] and not board[0][0] == '_'):
        if board[1][1] == '_':
            return [1,1]
    if (board[2][2] == board[1][1] and not board[1][1] == '_'):
        if board[0][0] == '_':
            return [0,0]

    empty_spots = [i*3+j for i in range(3)
                    for j in range(3) if board[i][j] == "_"]
    idx = choice(empty_spots)
    return[int(idx/3), idx % 3]

def findBestMove(board):
    root = state(copy.deepcopy(board))
    root.list_of_moves = list_of_blanks(root)
    create_root_children(board, root)
    root.list_of_moves = []
    for i in range(2000):
        root.children = sorted(root.children, key=lambda x: x.UCB, reverse=True)
        for child in root.children:
            if (child.win == 0 and child.blank == 0):
                create_each_state(child)
                break
        update_ucb_of_all_nodes(root)
    return list(root.children[0].move)

def get_score(node):
    return node.U/node.N + 2 * math.sqrt(math.log(node.parentN)/node.N)

def play_automatic(board, type):
    while isMovesLeft(board):
        x = find_best_choice(board)
        if (type == player and checkWin(board)):
            return True
        elif (type == opponent and checkWin(board)):
            return True
        if type == player:
            try:
                board[x[0]][x[1]] = opponent
            except:
                return None
            if checkWin(board):
                return False
            type = opponent
        else:
            x = find_best_choice(board)
            try:
                board[x[0]][x[1]] = player
            except:
                return None
            if checkWin(board):
                return True
            type = player
    return None

def isMovesLeft(board):
    return ('_' in board[0] or '_' in board[1] or '_' in board[2])

def checkWin(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            return True
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            return True

    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        return True

    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        return True

    return False

def printBoard(board):
    os.system('cls||clear')
    print("\n Player : X , Agent: O \n")
    for i in range(3):
        print(" ", end=" ")
        for j in range(3):
            if(board[i][j] == '_'):
                print(f"[{i*3+j+1}]", end=" ")
            else:
                print(f" {board[i][j]} ", end=" ")

        print()
    print()


if __name__ == "__main__":
    board = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']
    ]

    turn = 0

    while isMovesLeft(board) and not checkWin(board):
        if(turn == 0):
            printBoard(board)
            print(" Select Your Move :", end=" ")
            tmp = int(input())-1
            userMove = [int(tmp/3),  tmp % 3]
            while((userMove[0] < 0 or userMove[0] > 2) or (userMove[1] < 0 or userMove[1] > 2) or board[userMove[0]][userMove[1]] != "_"):
                print('\n \x1b[0;33;91m' + ' Invalid move ' + '\x1b[0m \n')
                print("Select Your Move :", end=" ")
                tmp = int(input())-1
                userMove = [int(tmp/3),  tmp % 3]
            board[userMove[0]][userMove[1]] = player
            print("Player Move:")
            printBoard(board)
            turn = 1
        else:
            bestMove = findBestMove(board)
            board[bestMove[0]][bestMove[1]] = opponent
            print("Agent Move:")
            printBoard(board)
            turn = 0

    if(checkWin(board)):
        if(turn == 1):
            print('\n \x1b[6;30;42m' + ' Player Wins! ' + '\x1b[0m')

        else:
            print('\n \x1b[6;30;42m' + ' Agent Wins! ' + '\x1b[0m')
    else:
        print('\n \x1b[0;33;96m' + ' Draw! ' + '\x1b[0m')

    input('\n Press Enter to Exit... \n')