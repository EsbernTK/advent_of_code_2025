"""
--- Day 2: Gift Shop ---
You get inside and take the elevator to its only other stop: the gift shop. "Thank you for visiting the North Pole!" gleefully exclaims a nearby sign. You aren't sure who is even allowed to visit the North Pole, but you know you can access the lobby through here, and from there you can access the rest of the North Pole base.

As you make your way through the surprisingly extensive selection, one of the clerks recognizes you and asks for your help.

As it turns out, one of the younger Elves was playing on a gift shop computer and managed to add a whole bunch of invalid product IDs to their gift shop database! Surely, it would be no trouble for you to identify the invalid product IDs for them, right?

They've even checked most of the product ID ranges already; they only have a few product ID ranges (your puzzle input) that you'll need to check. For example:

11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
(The ID ranges are wrapped here for legibility; in your input, they appear on a single long line.)

The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-).

Since the young Elf was just doing silly patterns, you can find the invalid IDs by looking for any ID which is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.

None of the numbers have leading zeroes; 0101 isn't an ID at all. (101 is a valid ID that you would ignore.)

Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:

11-22 has two invalid IDs, 11 and 22.
95-115 has one invalid ID, 99.
998-1012 has one invalid ID, 1010.
1188511880-1188511890 has one invalid ID, 1188511885.
222220-222224 has one invalid ID, 222222.
1698522-1698528 contains no invalid IDs.
446443-446449 has one invalid ID, 446446.
38593856-38593862 has one invalid ID, 38593859.
The rest of the ranges contain no invalid IDs.
Adding up all the invalid IDs in this example produces 1227775554.

What do you get if you add up all of the invalid IDs?
"""



def find_duplicates_for_n(n_str:str, min, max):
    n_len = len(n_str)
    out = [0]
    #if(n_len % 2 == 1):
    #    return out

    half_len = n_len//2 if n_len > 1 else 1
    half_n = int(n_str[:half_len])

    n1 = int(str(half_n) * 2)
    while min <= n1:
        if n1 <= max:
            out.append(n1)
        half_n -= 1
        n1 = int(str(half_n) * 2)

    half_n = int(n_str[:half_len])
    n2 = int(str(half_n) * 2)
    while n2 <= max:
        if min <= n2 and n2 not in out:
            out.append(n2)
        half_n += 1
        n2 = int(str(half_n) * 2)

    return out

def find_duplicates_in_range(low:str, high:str):
    if(len(high) - len(low) > 1):
        raise NotImplementedError
    low_int = int(low)
    high_int = int(high)

    low_ns = find_duplicates_for_n(low, low_int, high_int)
    #high_ns = find_duplicates_for_n(high, low_int, high_int)
    #high_ns = [n if n not in low_ns else 0 for n in high_ns]


    #out = low_ns + high_ns
    return low_ns

def find_duplicates_sum(data_list):
    all_dupes = []
    s = 0
    for d in data_list:
        low, high = d.split("-")
        dupes = find_duplicates_in_range(low, high)
        all_dupes.append(dupes)
        s += sum(dupes)
    return all_dupes, s





if __name__ == '__main__':
    test_data =["11-22","95-115","998-1012","1188511880-1188511890","222220-222224","1698522-1698528","446443-446449","38593856-38593862"]
    expected_dupes = set([11, 22,99, 1010, 1188511885, 222222, 446446, 38593859])
    dupes_test, s_tst = find_duplicates_sum(test_data)
    #dupes_set = set(dupes_test)
    assert s_tst == 1227775554

    with open("day_2.txt") as f:
        data = f.read().strip().split(",")

    dupes, s = find_duplicates_sum(data)

    range_dupes = [[r, d] for r, d in zip(data, dupes)]

    print(dupes)
    print(s) #19386344315




