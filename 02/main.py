from math import prod
from typing import Dict, List, Tuple


CONFIGURATION = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def turn_possible(turn: Dict[str, int]) -> bool:
    for colour, count in turn.items():
        if count > CONFIGURATION.get(colour, 0):
            return False

    return True

def game_possible(game: List[Dict[str, int]]) -> bool:
    for turn in game:
        if not turn_possible(turn):
            return False

    return True


def get_game_id(game: str) -> Tuple[int, str]:
    # each game begins with "Game ID:", parse the ID
    game_header, rest = game.split(":")
    game_id = int(game_header.split(" ")[-1])

    rest = rest.strip()

    return game_id, rest


def parse_colour(colour_str: str) -> Tuple[str, int]:
    count_str, colour = colour_str.split(" ")
    count = int(count_str)

    return colour, count

def parse_turn(turn_str: str) -> Dict[str, int]:
    colours_str = turn_str.split(",")
    turn = {}

    for colour_str in colours_str:
        colour_str = colour_str.strip()

        if colour_str:
            colour, count = parse_colour(colour_str)
            turn[colour] = count

    return turn

def parse_game_turns(game_turns: str) -> List[Dict[str, int]]:
    turns_str = game_turns.split(";")

    turns = []

    for turn_str in turns_str:
        turn_str = turn_str.strip()

        if turn_str:
            turn = parse_turn(turn_str)
            turns.append(turn)

    return turns



def parse_game(game: str) -> Tuple[int, List[Dict[str, int]]]:
    # game format:
    # Game ID: int colour_name, int colour_name, ...; int colour_name, int colour_name, ...; ...
    game_id, game_turns_str = get_game_id(game)

    game_turns = parse_game_turns(game_turns_str)

    return game_id, game_turns


def parse_games() -> Dict[int, List[Dict[str, int]]]:
    games: Dict[int, List[Dict[str, int]]] = {}

    with open("input_small.txt") as f:
        for line in f:
            line = line.strip()
            game_id, game = parse_game(line)
            games[game_id] = game

    return games


def min_counts(game: List[Dict[str, int]]) -> Dict[str, int]:
    min_counts = {"red": 0, "green": 0, "blue": 0}

    for turn in game:
        for colour, count in turn.items():
            min_counts[colour] = max(min_counts.get(colour, 0), count)

    return min_counts


def game_power(game: List[Dict[str, int]]) -> int:
    game_min_counts = min_counts(game)

    power = prod(game_min_counts.values())

    return power

def main():
    games = parse_games()

    possible_id_sum = sum(game_id for game_id, game in games.items() if game_possible(game))

    print(possible_id_sum)

def main_2():
    games = parse_games()

    power_sum = sum(game_power(game) for game in games.values())

    print(power_sum)



if __name__ == "__main__":
    main_2()
