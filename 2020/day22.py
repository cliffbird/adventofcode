from main import BaseProcessor
import re

class D22Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        #self.base_run(path_suffix="example2")
        self.base_run()

    def run1(self):
        if self.path_suffix == "example2":
            return

        cards_by_player = {}
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if "Player" in line:
                    m = re.match("Player (\d+):", line)
                    player_number = int(m.group(1))
                    cards_by_player[player_number] = []
                    continue

                cards_by_player[player_number].append(int(line))

            game = Game1(cards_by_player[1], cards_by_player[2])

            game_ended = False
            while not game_ended:
                game_ended = game.play_round()

    def run2(self):
        cards_by_player = {}
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if "Player" in line:
                    m = re.match("Player (\d+):", line)
                    player_number = int(m.group(1))
                    cards_by_player[player_number] = []
                    continue

                cards_by_player[player_number].append(int(line))

            game = Game2(cards_by_player[1], cards_by_player[2])

            game_ended = False
            winner = None
            while not game_ended:
                game_ended, winner = game.play_round()

class Game1:
    def __init__(self, p1_cards, p2_cards):
        self.player1 = Deck(p1_cards)
        self.player2 = Deck(p2_cards)
        self.num_rounds = 0

    def play_round(self):
        self.num_rounds += 1
        print(f"-- Round {self.num_rounds} --")
        print(f"Player 1's deck: {', '.join(str(x) for x in self.player1.cards)}")
        print(f"Player 2's deck: {', '.join(str(x) for x in self.player2.cards)}")
        c1 = self.player1.play()
        c2 = self.player2.play()
        print(f"Player 1 plays: {c1}")
        print(f"Player 2 plays: {c2}")

        if c1 > c2:
            self.player1.win_round(c1, c2)
            print("Player 1 wins the round!")
        elif c2 > c1:
            self.player2.win_round(c2, c1)
            print("Player 2 wins the round!")

        print()

        if self.player1.num_cards() == 0 or self.player2.num_cards() == 0:
            print("\n== Post-game results ==")
            print(f"Player 1's deck: {', '.join(str(x) for x in self.player1.cards)}")
            print(f"Player 2's deck: {', '.join(str(x) for x in self.player2.cards)}")

            print(f"part1: p1 {self.player1.get_score()} | p2 {self.player2.get_score()}")
            return True
        return False


class Game2:
    def __init__(self, p1_cards, p2_cards, game_count=1):
        self.round_history = {} # key is the number of cards for p1, value is a set of "p1deck|p2deck"
        self.p2_round_history = set()
        self.player1 = Deck(p1_cards)
        self.player2 = Deck(p2_cards)
        self.num_rounds = 0
        self.game_count = game_count
        self.enable_print = False
        if self.enable_print:
            print(f"=== Game {game_count} ===")

    def play_round(self):
        self.num_rounds += 1
        if self.enable_print:
            print(f"-- Round {self.num_rounds} (Game {self.game_count}) --")
        p1_deck_str = ','.join(str(x) for x in self.player1.cards)
        p2_deck_str = ','.join(str(x) for x in self.player2.cards)
        p1_num_cards_at_round_start = len(self.player1.cards)
        if p1_num_cards_at_round_start not in self.round_history:
            self.round_history[p1_num_cards_at_round_start] = set()
        else:
            compound_deck_str = f"{p1_deck_str}|{p2_deck_str}"
            if p1_num_cards_at_round_start in self.round_history and compound_deck_str in self.round_history[p1_num_cards_at_round_start]:
                return True, 1
            self.round_history[p1_num_cards_at_round_start].add(compound_deck_str)

        if self.enable_print:
            print(f"Player 1's deck: {p1_deck_str}")
            print(f"Player 2's deck: {p2_deck_str}")

        round_winner = None

        c1 = self.player1.play()
        c2 = self.player2.play()

        p1_num_cards = len(self.player1.cards)
        p2_num_cards = len(self.player2.cards)

        if p1_num_cards >= c1 and p2_num_cards >= c2:
            # play recursive combat
            sub_p1_cards = list(self.player1.cards[:c1])
            sub_p2_cards = list(self.player2.cards[:c2])
            sub_game = Game2(sub_p1_cards, sub_p2_cards, game_count=self.game_count+1)

            sub_game_ended = False
            while not sub_game_ended:
                sub_game_ended, round_winner = sub_game.play_round()
        else:
            if c1 > c2:
                round_winner = 1
            elif c2 > c1:
                round_winner = 2

        if self.enable_print:
            print(f"Player 1 plays: {c1}")
            print(f"Player 2 plays: {c2}")

        if round_winner == 1:
            self.player1.win_round(c1, c2)
            if self.enable_print:
                print(f"Player 1 wins round {self.num_rounds} of game {self.game_count}!\n")
        else:
            self.player2.win_round(c2, c1)
            if self.enable_print:
                print(f"Player 2 wins round {self.num_rounds} of game {self.game_count}!\n")

        if self.player1.num_cards() == 0 or self.player2.num_cards() == 0:
            if self.player1.num_cards() == 0:
                winner = 2
            else:
                winner = 1
            if self.game_count == 1:
                print("\n== Post-game results ==")
                print(f"Player 1's deck: {', '.join(str(x) for x in self.player1.cards)}")
                print(f"Player 2's deck: {', '.join(str(x) for x in self.player2.cards)}")

                print(f"part1: p1 {self.player1.get_score()} | p2 {self.player2.get_score()}")
            else:
                if self.enable_print:
                    print(f"The winner of game {self.game_count} is player {winner}")
            return True, winner
        return False, None


class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.num_wins = 0
        self.num_rounds = 0

    def play(self):
        self.num_rounds += 1
        return self.cards.pop(0)

    def win_round(self, card1, card2):
        self.cards.append(card1)
        self.cards.append(card2)
        self.num_wins += 1

    def num_cards(self):
        return len(self.cards)

    def get_score(self):
        multiplier = 1
        score = 0
        while self.cards:
            cur = self.cards.pop()
            score += cur * multiplier
            multiplier += 1
        return score

