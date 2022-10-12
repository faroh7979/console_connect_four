from collections import deque
from colorama import Fore, Back


class Colors:
    red_system = Fore.RED + Back.BLACK  # for wrong input
    blue_system = Fore.BLUE + Back.BLUE  # for entering input
    red = Fore.RED  # for player mark coloring
    blue = Fore.BLUE  # for player mark coloring
    green = Fore.GREEN  # for player mark coloring
    yellow = Fore.YELLOW  # for player mark coloring
    black = Fore.BLACK  # for player mark coloring
    magenta = Fore.MAGENTA  # for player mark coloring
    cyan = Fore.CYAN  # for player mark coloring
    white = Fore.WHITE  # for player mark coloring


colors_list = ['red', 'blue', 'green', 'yellow', 'black', 'magenta', 'cyan', 'white']


def player_details(user_input):
    player_deque = deque()

    try:  # check vor valid input
        number_of_players = int(user_input)
    except ValueError:
        user_input = input(Fore.YELLOW + 'Please select number of players between 1 and 9 >>> ')
        return player_details(user_input)

    player_details_dict = {}  # use dictionary for player screen name and player symbol
    for current_num in range(1, number_of_players + 1):
        player_name = input(f'Player {current_num}, please choose your screen name >>> ')

        if player_name in player_details_dict:
            used_screen_name = True

            while used_screen_name:
                player_name = input(f'{player_name} is already taken! Please choose another one >>> ')

                if player_name not in player_details_dict:
                    break

        player_symbol = input(f'{player_name} please enter your playing mark! Only one symbol >>> ')
        if len(player_symbol) != 1:
            player_symbol_too_short = True

            while player_symbol_too_short:
                player_symbol = input(f'{player_name} your mark is too long, please enter it again >>> ')
                if len(player_symbol) == 1:
                    break

        if player_symbol in player_details_dict.values():
            player_symbol_is_taken = True

            while player_symbol_is_taken:
                player_symbol = \
                    input(f'{player_name} "{player_symbol}" is already taken, please choose another one >>> ')
                if player_symbol not in player_details_dict.values():
                    break

        player_details_dict[player_name] = player_symbol
        player_deque.append((player_name, player_symbol))

    return player_deque, player_details_dict


def check_for_win(current_matrix, matrix_row, matrix_col, possible_movements, current_player_symbol):
    for current_row_index in range(matrix_row):  # this check starting from top row, need optimisations
        for current_column_index in range(matrix_col):
            if current_matrix[current_row_index][current_column_index] != current_player_symbol:  # no chance for winning
                continue

            for movement in possible_movements:
                row_move, col_move = movement
                new_row_index = current_row_index + row_move
                new_col_index = current_column_index + col_move

                for winning_streak in range(3):  # need three in a row from current position to take the win

                    # check for invalid index
                    if 0 > new_row_index or new_row_index >= matrix_row or 0 > new_col_index or new_col_index >= matrix_col:
                        break
                    if current_matrix[new_row_index][new_col_index] != current_player_symbol:
                        break

                    new_row_index += row_move
                    new_col_index += col_move

                else:
                    return True  # three wining in a row
    else:
        return False  # there is no winning combination


def column_choosing(queue, matrix, num_matrix_rows, num_matrix_cols, winning_movements):
    free_column = [int(i) for i in range(1, num_matrix_cols + 1)]
    win = False
    player_name = ''

    while not win:
        player_on_turn = queue.popleft()
        queue.append(player_on_turn)
        player_name = player_on_turn[0]
        player_symbol = player_on_turn[1]

        chosen_column = 0
        while True:
            try:
                chosen_column = int(input(f'{player_name}, please select one of the following {", ".join(map(str, free_column))} where to drop your coin >>> '))

                if 1 > chosen_column > 7 or chosen_column not in free_column:
                    continue

                break

            except ValueError:
                continue

        chosen_column_index = chosen_column - 1  # because index starting from zero
        for row_index in range(len(matrix) - 1, - 1, - 1):  # check from the bottom
            if matrix[row_index][chosen_column_index] == '0':
                matrix[row_index][chosen_column_index] = player_symbol

                if row_index == 0:  # the coin is placed on the top of the column
                    free_column.remove(chosen_column)

                break  # founded slot for player coin

        for row in matrix:
            print(row)


        win = check_for_win(matrix, num_matrix_rows, num_matrix_cols, winning_movements, player_symbol)

    if win:
        return f'{player_name} win the game'

    if not free_column:
        return f'No winner. The game ends with a draw!'


number_of_players_input = input(Colors.red + 'Please select number of players between 1 and 9 >>> ')

matrix_field_rows, matrix_field_cols = 6, 7  # that is tha classical board for this game
matrix_field = [['0' for _ in range(matrix_field_cols)] for _ in range(matrix_field_rows)]

possible_winning_directions = (
    (1, 0),
    (1, - 1),
    (1, 1),
    (- 1, 0),
    (- 1, - 1),
    (- 1, 1),
    (0, - 1),
    (0, 1),
)

queue_one, initial_matrix = player_details(number_of_players_input)
new_matrix = column_choosing(queue_one, matrix_field, matrix_field_rows, matrix_field_cols, possible_winning_directions)

print(new_matrix)
