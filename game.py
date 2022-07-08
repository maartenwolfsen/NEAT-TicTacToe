from os import path
import random
import neat
import pickle

ROOT_DIR = path.dirname(__file__)
ETC_DIR = path.join(ROOT_DIR, 'etc')

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
            return -1

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

    def output_to_move(self, output):
        move = 0

        if output > -1.75 and output <= -1.25:
            move = 1
        elif output > -1.25 and output <= -0.75:
            move = 2
        elif output > -0.75 and output <= -0.25:
            move = 3
        elif output > -0.25 and output <= 0.25:
            move = 4
        elif output > 0.25 and output <= 0.75:
            move = 5
        elif output > 0.75 and output <= 1.25:
            move = 6
        elif output > 1.25 and output <= 1.75:
            move = 7
        else:
            move = 8

        return move

    def check_if_moves_left(self):
        for move in self.field:
            if move == 0:
                return True

        return False

def main(genomes, config):
    networks = []
    ge = []
    games = []

    # Setup Neural Networks
    for _, g in genomes:
        network = neat.nn.FeedForwardNetwork.create(g, config)
        networks.append(network)
        games.append(TicTacToe(3))
        g.fitness = 0
        ge.append(g)

    for index, game in enumerate(games):
        run = True

        while run:
            if not game.check_if_moves_left():
                ge[index].fitness -= 0.5
                print("No moves left")
                games.pop(index)
                networks.pop(index)
                ge.pop(index)
                run = False

                continue

            # Opponent turn
            if not game.turn:
                game.field[game.opponent_move()] = 2
                result = game.end_turn()

                if result == False:
                    game.print_field()
                    ge[index].fitness -= 1
                    games.pop(index)
                    networks.pop(index)
                    ge.pop(index)

                run = result

                continue

            # Player turn
            input_data = game.field
            output = networks[index].activate(input_data)
            move = game.output_to_move(output[0])
            print("Player move: " + str(move))
            u_input = game.user_input(move)

            # Invalid move
            if u_input == -1:
                ge[index].fitness -= 1
                games.pop(index)
                networks.pop(index)
                ge.pop(index)
                run = False
                print("Player 1 lost because of invalid move")

                continue

            game.field[u_input] = 1
            result = game.end_turn()

            # Game won
            if result == False:
                game.print_field()
                game = TicTacToe(3)
                ge[index].fitness += 1
                games[index] = game
                result = True

# Run AI
def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(main)


    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

# Set Config
if __name__ == "__main__":
    run(path.join(ETC_DIR, "config"))
