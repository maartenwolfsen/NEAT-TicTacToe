import random

class TicTacToe:
    USER_INPUT_STRING = "Your turn (use 0-9 to place at that position)"

    # Todo: Variable grid size
    def __init__(self, grid_size):
        self.turn = True
        self.field = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.p1_moves = []
        self.p2_moves = []
        self.grid_size = grid_size

    # Check if combination is reached
    def in_field(self, player_field, search):
        for item in search:
            if item not in player_field:
                return False

        return True

    # User input
    def user_input(self, input):
        if self.field[input] != 0:
            # fitness -1
            input = self.user_input(int(input(self.USER_INPUT_STRING)))

        return input

    # Check if win conditions are met
    def check_win(self):
        i = 0

        for value in self.field:
            if value == 1: self.p1_moves.append(i)
            if value == 2: self.p2_moves.append(i)

            i += 1

        if self.check_player(self.p1_moves): return 1
        if self.check_player(self.p2_moves): return 2

        return 0

    # Check if player has met win conditions
    # Todo: Dynamic checking
    def check_player(self, player):
        if (self.in_field(player, [0, 1, 2]) or
            self.in_field(player, [3, 4, 5]) or
            self.in_field(player, [6, 7, 8]) or
            self.in_field(player, [0, 3, 6]) or
            self.in_field(player, [1, 4, 7]) or
            self.in_field(player, [2, 5, 8]) or
            self.in_field(player, [0, 4, 8]) or
            self.in_field(player, [2, 4, 6])):
            return True

        return False

    # Opponent move (random move)
    def opponent_move(self):
        open = []
        i = 0

        for spot in self.field:
            if spot == 0:
                open.append(i)

            i += 1

        return open[random.randint(0, len(open) - 1)]

    # Print TicTacToe field
    def print_field(self):
        print("[" + str(self.field[0]) + str(self.field[1]) + str(self.field[2]) + "]")
        print("[" + str(self.field[3]) + str(self.field[4]) + str(self.field[5]) + "]")
        print("[" + str(self.field[6]) + str(self.field[7]) + str(self.field[8]) + "]")

    # End turn
    def end_turn(self):
        self.turn = not self.turn
        win = self.check_win()

        if win != 0:
            print("Player " + str(win) + " won!")

            return False

        return True

def main():
    game = TicTacToe(3)
    game.print_field()
    run = True

    while run:
        # Opponent turn
        if not game.turn:
            game.field[game.opponent_move()] = 2
            run = game.end_turn()

            continue

        # Player turn
        u_input = game.user_input(
            int(input(
                "[" + str(1 if game.turn else 2) + "] " + game.USER_INPUT_STRING)
            )
        )
        game.field[u_input] = 1
        run = game.end_turn()
        game.print_field()

main()
