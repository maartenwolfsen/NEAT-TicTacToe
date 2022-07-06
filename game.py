import random

USER_INPUT_STRING = "Your turn (use 0-9 to place at that position)"

def in_array(array, search):
    for item in search:
        if item not in array:
            return False

    return True

def user_input(field, input):
    if field[input] != 0:
        # fitness -1
        input = user_input(int(input(USER_INPUT_STRING)))

    return input

def check_win(field):
    p1_moves = []
    p2_moves = []
    i = 0

    for value in field:
        if value == 1: p1_moves.append(i)
        if value == 2: p2_moves.append(i)

        i += 1

    if check_player(p1_moves): return 1
    if check_player(p2_moves): return 2

    return 0

def check_player(player):
    if (in_array(player, [0, 1, 2]) or
        in_array(player, [3, 4, 5]) or
        in_array(player, [6, 7, 8]) or
        in_array(player, [0, 3, 6]) or
        in_array(player, [1, 4, 7]) or
        in_array(player, [2, 5, 8]) or
        in_array(player, [0, 4, 8]) or
        in_array(player, [2, 4, 6])):
        return True

    return False

def opponent_move(field):
    open = []
    i = 0

    for spot in field:
        if spot == 0:
            open.append(i)

        i += 1

    return open[random.randint(0, len(open) - 1)]

def print_field(field):
    print(str(field[0]) + str(field[1]) + str(field[2]))
    print(str(field[3]) + str(field[4]) + str(field[5]))
    print(str(field[6]) + str(field[7]) + str(field[8]))

def end_turn(field):
    print_field(field)
    win = check_win(field)

    if win != 0:
        print("Player " + str(win) + " won!")

        return False

    return True

def main():
    field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn = True
    run = True
    print_field(field)

    while run:
        if not turn:
            field[opponent_move(field)] = 2
            turn = not turn
            run = end_turn(field)

            continue

        u_input = user_input(
            field,
            int(input(
                "[" + str(1 if turn else 2) + "] " + USER_INPUT_STRING)
            )
        )
        field[u_input] = 1
        turn = not turn
        run = end_turn(field)

main()
