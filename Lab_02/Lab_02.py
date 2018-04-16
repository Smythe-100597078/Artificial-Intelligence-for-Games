from math import inf as infinity
from random import choice
import time
from os import system

HUMAN = -1
FIRST_AI = +1
SECOND_AI = -1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def evaluate(state):
    if wins(state, FIRST_AI):
        score = +1
    elif wins(state, SECOND_AI):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    return wins(state, HUMAN) or wins(state, FIRST_AI) or wins(state,SECOND_AI)


def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0: cells.append([x, y])
    return cells


def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    if player == FIRST_AI or player == SECOND_AI:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == FIRST_AI or player == SECOND_AI:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def render(state, first_ai_choice, second_ai_choice):
    print('----------------')
    for row in state:
        print('\n----------------')
        for cell in row:
            if cell == +1:
                print('|', first_ai_choice, '|', end='')
            elif cell == -1:
                print('|', second_ai_choice, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n----------------')
    
    # Game over message
    if wins(board, FIRST_AI):
        print('First AI wins!')
    elif wins(board, FIRST_AI):
        print('Second AI wins!')
    else:
        if game_over(board):
            print('AI Draw!')


def ai_turn(first_ai_choice, second_ai_choice,player_ID):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    
    if player_ID == FIRST_AI:
        print('First AIs turn [{}]'.format(first_ai_choice))
    else:print('Second AIs turn [{}]'.format(second_ai_choice))

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, player_ID)
        x, y = move[0], move[1]

    set_move(x, y, player_ID)
    time.sleep(1)


def update(first_ai_choice,second_ai_choice):
    ai_turn(first_ai_choice,second_ai_choice,FIRST_AI)
    ai_turn(first_ai_choice,second_ai_choice,SECOND_AI)
  

def main():
   
    first_ai_choice = 'X' # X or O
    second_ai_choice = 'O' # X or O
  
    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
       
        update(first_ai_choice,second_ai_choice)
        render(board,first_ai_choice,second_ai_choice)

    exit()


if __name__ == '__main__':
    main()