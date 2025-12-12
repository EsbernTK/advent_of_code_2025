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


def main_1():
    with open("day_2.txt") as f:
        data = f.read().strip().split(",")

    dupes, s = find_duplicates_sum(data)

    range_dupes = [[r, d] for r, d in zip(data, dupes)]

    print(dupes)
    print(s) #19386344315

def main_1_test():
    test_data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    test_data_list = test_data.strip().split(",")
    expected_dupes = set([11, 22,99, 1010, 1188511885, 222222, 446446, 38593859])
    dupes_test, s_tst = find_duplicates_sum(test_data_list)
    #dupes_set = set(dupes_test)
    assert s_tst == 1227775554

"""
--- Part Two ---
The clerk quickly discovers that there are still invalid IDs in the ranges in your list. Maybe the young Elf was doing other silly patterns as well?

Now, an ID is invalid if it is made only of some sequence of digits repeated at least twice. So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), and 1111111 (1 seven times) are all invalid IDs.

From the same example as before:

11-22 still has two invalid IDs, 11 and 22.
95-115 now has two invalid IDs, 99 and 111.
998-1012 now has two invalid IDs, 999 and 1010.
1188511880-1188511890 still has one invalid ID, 1188511885.
222220-222224 still has one invalid ID, 222222.
1698522-1698528 still contains no invalid IDs.
446443-446449 still has one invalid ID, 446446.
38593856-38593862 still has one invalid ID, 38593859.
565653-565659 now has one invalid ID, 565656.
824824821-824824827 now has one invalid ID, 824824824.
2121212118-2121212124 now has one invalid ID, 2121212121.
Adding up all the invalid IDs in this example produces 4174379265.

What do you get if you add up all of the invalid IDs using these new rules?
"""

def find_repeated_sequence_duplicates(low:str, high:str):
    low_int = int(low)
    high_int = int(high)

    low_len = len(low)
    high_len = len(high)

    out = []

    for k in range(1, high_len//2 + 1):
        low_n_mul = low_len // k
        high_n_mul = high_len // k

        for i in range(max(low_n_mul,1), high_n_mul +1):
            start_int = int(low[:k])
            new_n = int(str(start_int) * i)

            if(new_n < 10):
                #the digit has to be repeated twice, no n under 10 can be that
                continue

            if(i == 1):
                new_n_str = str(new_n)
                if new_n == int(new_n_str[0] * len(new_n_str)):
                    if low_int <= new_n <= high_int and new_n not in out:
                        out.append(new_n)

            else:
                while new_n <= high_int:
                    if(low_int <= new_n and new_n not in out):
                        out.append(new_n)
                    start_int += 1
                    new_n = int(str(start_int) * i)

                start_int = int(low[:k])
                new_n = int(str(start_int) * i)
                while low_int <= new_n:
                    if(new_n <= high_int and new_n not in out):
                        out.append(new_n)
                    start_int -= 1
                    new_n = int(str(start_int) * i)

    return out

def find_repeated_sequence_duplicates_sum(data_list):
    all_dupes = []
    s = 0
    for d in data_list:
        low, high = d.split("-")
        dupes = find_repeated_sequence_duplicates(low, high)
        all_dupes.append(dupes)
        s += sum(dupes)
    return all_dupes, s


def dupe_test(n_str):
    is_dupe_list = []
    for k in range(1,len(n_str) // 2 + 1):
        template = n_str[:k]
        is_dupe = True
        for i in range(k, len(n_str), k):
            if(n_str[i:i+k] != template):
                is_dupe = False
        is_dupe_list.append(is_dupe)
    assert any(is_dupe_list), f"{n_str} is not a dupe"


    #if(len(n_str) % 2 == 1):
    #    assert n_str == n_str[0] * len(n_str), f"{n_str} is not a dupe"
    #else:
    #    assert n_str[:len(n_str) // 2] == n_str[len(n_str) // 2:], f"{n_str} is not a dupe"

def main_2():
    with open("day_2.txt") as f:
        data = f.read().strip().split(",")

    dupes, s = find_repeated_sequence_duplicates_sum(data)

    flat_dupes = [x for xs in dupes for x in xs]
    flat_dupes_true = [dupe_test(str(x)) for x in flat_dupes]


    range_dupes = [[r, d] for r, d in zip(data, dupes)]

    print(dupes)
    print(s) #34421651195


def main_2_test():
    test_data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    test_data_list = test_data.strip().split(",")
    expected_dupes = set([11, 22,99,111,999, 1010, 1188511885, 222222, 446446, 38593859, 565656, 824824824, 2121212121])

    dupes, s = find_repeated_sequence_duplicates_sum(test_data_list)

    flat_dupes = [x for xs in dupes for x in xs]

    dupes_set = set(flat_dupes)
    if(0 in dupes_set):
        dupes_set.remove(0)

    assert len(dupes_set.difference(expected_dupes)) == 0

    assert s == 4174379265

def main_2_test_2():
    test_data_list = ['5140337-5233474']
    dupes, s = find_repeated_sequence_duplicates_sum(test_data_list)

    expected_dupes = set(
        [])



if __name__ == '__main__':
    #main_1_test()
    #main_1()

    main_2_test()
    main_2()





