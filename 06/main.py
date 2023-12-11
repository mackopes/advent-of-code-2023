from math import prod
from typing import Generator, List
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance: int


def parse_numbers(time_str: str) -> Generator[int, None, None]:
    times = time_str.split(":")[1]
    for x in times.split():
        if not x:
            continue
        yield int(x)
    # return [int(x) for x in times.split() if x]


def parse_as_one_number(time_str: str) -> int:
    numbers_str = time_str.split(":")[1]

    number = int(numbers_str.replace(" ", ""))

    return number


def parse_input() -> List[Race]:
    with open("input.txt") as f:
        lines = f.readlines()

    times = parse_numbers(lines[0])
    distances = parse_numbers(lines[1])

    return [Race(time, distance) for time, distance in zip(times, distances)]


def parse_input_2() -> Race:
    with open("input.txt") as f:
        lines = f.readlines()

    time = parse_as_one_number(lines[0])
    distance = parse_as_one_number(lines[1])

    return Race(time, distance)


def distance(holding_time, total_time) -> int:
    return holding_time * total_time - holding_time * holding_time


def wins_race(race: Race, holding_time: int) -> bool:
    return race.distance < distance(holding_time, race.time)


def n_ways_to_win(race: Race) -> int:
    return sum(1 for holding_time in range(race.time) if wins_race(race, holding_time))

def main():
    races = parse_input()

    # distance = holding_time * leftover_time
    # distance = holding_time * total_time - holding_time^2 -> upside down parabola

    print(prod(n_ways_to_win(race) for race in races))

def main_2():
    race = parse_input_2()

    ways_to_win = n_ways_to_win(race)

    print(ways_to_win)


if __name__ == "__main__":
    main_2()
