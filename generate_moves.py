import numpy as np
from utils import *


class MovesConfigure:
    def __init__(self):
        self.ordinal_limit = 8
        self.generated_moves = []
        self.generated_labels = []
        self.limit = []
        self.directions = [
            [(0,2), (0,1), (0,0)],
            [(2,0), (1,0), (0,0)],
            [(2,2), (1,1), (0,0)],
            [(-2,2), (-1,1), (0,0)],
        ]


def add_moves(history, config):
    config.generated_moves.append(history.copy())
    game_map = np.zeros((3,3))
    for i in range(0, 9):
        x = history[i] % 3
        y = history[i] // 3
        game_map[y][x] = i % 2 + 1 # 1 is player, 2 is bot
        if i >= 4:
            check = check_win_both(game_map, config.directions)  
            if check != 0: 
                config.generated_labels.append(check)
                config.limit.append(i + 1) # number of moves requires to win
                return 
    config.generated_labels.append(0)
    config.limit.append(9)

        
def check_win_both(game_map, directions):
    for notation in range(1, 3):
        for i in range(0, 3): # height 
            for j in range(0, 3): # width
                if game_map[i][j] == notation:
                    for direction in directions:
                        check = True
                        for adds_x, adds_y in direction:
                            if i + adds_y < 0 or j + adds_x < 0 or i + adds_y > 2 or j + adds_x > 2 or game_map[i + adds_y][j + adds_x] != notation:
                                check = False
                                break
                        if check:
                            return notation
    return 0 # draw


def brute_force(num, history, is_visisted, move_config):
    for i in range(0, 9):
        x = i % 3
        y = i // 3
        if not is_visisted[y,x]:
            is_visisted[y,x] = True
            history.append(i)
            if num == move_config.ordinal_limit:
                add_moves(history, move_config) 
            else:
                brute_force(num + 1, history, is_visisted, move_config)
            history.pop(len(history) - 1)
            is_visisted[y][x] = False



def generate_moves_with_labels():
    move_config = MovesConfigure()
    is_visisted = np.full((3,3), False)
    history = []
    brute_force(0, history, is_visisted, move_config)
    move_config.generated_moves = np.array(move_config.generated_moves)
    move_config.generated_labels = np.array(move_config.generated_labels)
    move_config.limit = np.array(move_config.limit)

    set_moves = set([])
    tf = np.ones((len(move_config.limit)))

    for i in range(0, len(move_config.generated_moves)):
        concatenated_string = concatenate_nparr_string(move_config.generated_moves[0: (move_config.limit[i] - 1)])
        if concatenated_string in set_moves:
            tf[i] = 0
        else:
            set_moves.add(concatenated_string)    
    
    move_config.generated_moves = move_config.generated_moves[tf == 1]
    move_config.generated_labels = move_config.generated_labels[tf == 1]
    move_config.limit = move_config.limit[tf == 1]


    return move_config.generated_moves, move_config.generated_labels, move_config.limit


if __name__ == '__main__':
    move_config = MovesConfigure()
    is_visisted = np.full((3,3), False)
    history = []
    brute_force(0, history, is_visisted, move_config)
    move_config.generated_moves = np.array(move_config.generated_moves).astype('int')
    move_config.generated_labels = np.array(move_config.generated_labels).astype('int')
    move_config.limit = np.array(move_config.limit).astype('int')

    set_moves = set([])
    tf = np.ones((len(move_config.limit)))

    for i in range(0, len(move_config.generated_moves)):
        concatenated_string = concatenate_nparr_string(move_config.generated_moves[i, 0 : move_config.limit[i] - 1])
        if concatenated_string in set_moves:
            tf[i] = 0
        else:
            set_moves.add(concatenated_string)    
    

    move_config.generated_moves = move_config.generated_moves[tf == 1]
    move_config.generated_labels = move_config.generated_labels[tf == 1]
    move_config.limit = move_config.limit[tf == 1]

    np.savetxt('moves.txt', move_config.generated_moves)
    np.savetxt('labels.txt', move_config.generated_labels)
    np.savetxt('limit.txt', move_config.limit)

    