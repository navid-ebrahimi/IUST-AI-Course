import random

#################################################################################
# Functions
#################################################################################

def ai_action(game_state):
    ''' Generate and play move from tic tac toe AI'''
    #################################################################################

    condition = [
            # horizontal
            (0, 1, 2, 3),
            (1, 2, 3, 4),
            (5, 6, 7, 8),
            (6, 7, 8, 9),
            (10, 11, 12, 13),
            (11, 12, 13, 14),
            (15, 16, 17, 18),
            (16, 17, 18, 19),
            (20, 21, 22, 23),
            (21, 22, 23, 24),

            # vertical
            (0, 5, 10, 15),
            (5, 10, 15, 20),
            (1, 6, 11, 16),
            (6, 11, 16, 21),
            (2, 7, 12, 17),
            (7, 12, 17, 22),
            (3, 8, 13, 18),
            (8, 13, 18, 23),
            (4, 9, 14, 19),
            (9, 14, 19, 24),

            # diagonal
            (0, 6, 12, 18),
            (6, 12, 18, 24),
            (4, 8, 12, 16),
            (8, 12, 16, 20),
            (1, 7, 13, 19),
            (5, 11, 17, 23),
            (3, 7, 11, 15),
            (9, 13, 17, 21),
        ]

    diagonal = [
            (0, 6, 12, 18),
            (4, 8, 12, 16),
            (8, 12, 16, 20),
            (1, 7, 13, 19),
            (6, 12, 18, 24),
            (5, 11, 17, 23),
            (3, 7, 11, 15),
            (9, 13, 17, 21),
    ]

    index = -1
    for check in condition:
        if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, False, False, False):
            index = check[0]
            break
        if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (False, None, False, False):
            index = check[1]
            break
        if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (False, False, None, False):
            index = check[2]
            break
        if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (False, False, False, None):
            index = check[3]
            break


    if (index==-1):
        for check in condition:
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, True, True, True):
                index = check[0]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (True, None, True, True):
                index = check[1]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (True, True, None, True):
                index = check[2]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (True, True, True, None):
                index = check[3]
                break

    if (index == -1):
        for i in range(5):
            a = 0
            li = [1,2,3]
            for j in range(1,4):
                if (game_state[i*5 + j]):
                    a+=1
                    li.remove(j)

            if (a==2 and game_state[i*5 + li[0]] == None):
                index = i * 5 + li[0]
                break
            
            a = 0
            li = [1,2,3]
            for j in range(1,4):
                if (game_state[j*5 + i]):
                    a+=1
                    li.remove(j)

            if (a==2 and game_state[li[0]*5 + i] == None):
                index = i + (li[0]) * 5
                break

    if (index==-1):
        a = 0
        for check in diagonal:
            li = list(check)
            res = 0
            if (a<2):
                li.remove(check[0])
            else:
                li.remove(check[3])
            for i in range(1,4):
                if (a<2):
                    if (game_state[check[i]]):
                        res+=1
                        li.remove(check[i])

                else:
                    if (game_state[check[i-1]]):
                        res+=1
                        li.remove(check[i-1])

            if (res==2 and game_state[li[0]] == None):
                index = li[0]
                break

            a+=1





    if (index==-1):
        for check in condition:
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, None, False, False):
                index = check[0]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, False, None, False):
                index = check[0]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, False, False, None):
                index = check[0]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (False, None, None, False):
                index = check[1]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (False, None, False, None):
                index = check[1]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (False, False, None, None):
                index = check[2]
                break


    if (index==-1):
        for check in condition:
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (False, None, None, None):
                index = check[1]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, False, None, None):
                index = check[0]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, None, False, None):
                index = check[0]
                break
            if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, None, None, False):
                index = check[0]
                break
    
    
    if (index==-1):
        if (game_state[12] == None):
            index = 12

        else:
            for check in condition:
                if (game_state[check[0]],game_state[check[1]],game_state[check[2]],game_state[check[3]]) == (None, None, None, None):
                    index = check[0]
                    break

    try:
        if (index==-1):
            emptyStates = []
            for i in range(0,25):     
                if game_state[i] is None:
                    emptyStates.append(i)

            index = random.choice(emptyStates)
    except:
        pass

    return index
    #################################################################################