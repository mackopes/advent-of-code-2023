import dataclasses
from re import S
from typing import List, Optional, Tuple


# @dataclasses.dataclass
# class SeedRange:
#     start: int
#     length: int


@dataclasses.dataclass
class Range:
    dest_start: int
    source_start: int
    length: int

    @property
    def source_end(self) -> int:
        return self.source_start + self.length

    def in_range(self, value: int) -> bool:
        return self.source_start <= value < self.source_start + self.length

    def map(self, value: int) -> int:
        if not self.in_range(value):
            raise ValueError(f"{value} not in range {self}")

        return self.dest_start + (value - self.source_start)

    def seed_range_overlap(self, seed_range: "Range") -> bool:
        return (
            seed_range.source_start < self.source_start + self.length
            and seed_range.source_start + seed_range.length > self.source_start
        )

    def seed_range_map(self, seed_range: "Range") -> Tuple[List["Range"], Optional["Range"]]:
        if not self.seed_range_overlap(seed_range):
            if seed_range.source_end <= self.source_start:
                return [seed_range], None
            else:
                return [], seed_range

        res = []

        # seed range starts before this range
        if seed_range.source_start < self.source_start:
            before_source_start = seed_range.source_start
            before_length = self.source_start - seed_range.source_start
            before_dest_start = seed_range.dest_start

            assert before_dest_start == before_source_start

            res.append(Range(before_dest_start, before_source_start, before_length))

        # overlap is mapped
        overlap_source_start = max(seed_range.source_start, self.source_start)
        overlap_source_end = min(
            seed_range.source_start + seed_range.length, self.source_start + self.length
        )
        overlap_length = overlap_source_end - overlap_source_start
        overlap_dest_start = self.dest_start + (overlap_source_start - self.source_start)

        # assert overlap_dest_start == overlap_source_start
        res.append(Range(overlap_dest_start, overlap_dest_start, overlap_length))

        after_range = None

        # seed range ends after this range
        if seed_range.source_end > self.source_end:
            after_source_start = self.source_end
            after_source_end = seed_range.source_end
            after_length = after_source_end - after_source_start
            after_dest_start = after_source_start

            assert after_dest_start == after_source_start

            after_range = Range(after_dest_start, after_dest_start, after_length)

        return res, after_range


@dataclasses.dataclass
class Map:
    fr: str
    to: str

    ranges: List[Range]

    def map(self, value: int) -> int:
        for r in self.ranges:
            if r.in_range(value):
                return r.map(value)

        return value

    def seed_range_map(self, seed_range: Range) -> List[Range]:
        res = []

        self.ranges = sorted(self.ranges, key=lambda x: x.source_start)

        unmapped_range = seed_range

        for r in self.ranges:
            if not unmapped_range:
                break
            mapped, unmapped_range = r.seed_range_map(unmapped_range)
            res.extend(mapped)

        if unmapped_range:
            res.append(unmapped_range)

        return res


def parse_seeds(seeds_line: str) -> List[int]:
    seed_numbers = seeds_line.split(": ")[1]
    seeds = [int(x) for x in seed_numbers.split(" ") if x]
    return seeds


def parse_seeds_2(seeds_line: str) -> List[Range]:
    seed_numbers_str = seeds_line.split(": ")[1]
    seed_numbers = [int(x) for x in seed_numbers_str.split(" ") if x]

    seeds = []

    for start, length in zip(seed_numbers[::2], seed_numbers[1::2]):
        # seeds.extend(range(start, start + length))
        seeds.append(Range(start, start, length))

    return seeds


def parse_map_header(map_header: str) -> Tuple[str, str]:
    map_name = map_header.split(" ")[0]
    fr, to = map_name.split("-to-")

    return fr, to


def parse_range(range_line: str) -> Range:
    dest_start, source_start, length = range_line.split(" ")
    return Range(int(dest_start), int(source_start), int(length))


def parse_maps(maps_lines: List[str]) -> List[Map]:
    maps = []

    fr, to = None, None
    ranges = []

    for line in maps_lines:
        if ":" in line:
            if fr and to:
                maps.append(Map(fr, to, ranges))
                ranges = []
            fr, to = parse_map_header(line)
            continue

        if line.strip():
            ranges.append(parse_range(line))
            continue

    if fr and to:
        maps.append(Map(fr, to, ranges))

    return maps


def parse_input():
    with open("input.txt") as f:
        lines = f.readlines()

    seeds = parse_seeds_2(lines[0])
    maps = parse_maps(lines[1:])

    # print("seeds", seeds)
    # print("maps", maps)

    return seeds, maps


def map_seed(maps: List[Map], seed: int) -> int:
    for m in maps:
        seed = m.map(seed)
    return seed


def main():
    # import os
    # print(os.getcwd())
    seeds, maps = parse_input()

    ranges = seeds

    for m in maps:
        print(m.fr, m.to)
        new_ranges = []
        for seed_range in ranges:
            new_ranges.extend(m.seed_range_map(seed_range))
        ranges = new_ranges

    minvalue = min(r.dest_start for r in ranges)
    print(minvalue)

    # print([r.dest_start for r in ranges])


    # for i in tqdm(range(len(values))):
    #     values[i] = map_seed(values[i], maps)

    # curr_min = map_seed(maps, values[0])

    # with multiprocessing.Pool() as pool:
    #     # v = min(tqdm(pool.imap_unordered(functools.partial(map_seed, maps), values, chunksize=100000), total=len(values)))
    #     for v in pool.imap_unordered(
    #         functools.partial(map_seed, maps), values, chunksize=100000
    #     ):
    #         if v < curr_min:
    #             curr_min = v

        # values = [m.map(x) for x in values]
        # do the same in parallel

    # print(values)
    # print(curr_min)


if __name__ == "__main__":
    main()
