"""
Find two maximums in sequence
"""
from operator import itemgetter


def two_max(data):
    """
    find 2 biggest maximums in data sequence
    return tuple (first_max, second_max)
    each maximum is a tuple (position_in_sequence, maximum_value) or None if maximum absent
    """
    if len(data) < 3:
        raise ValueError("Sequence too short")

    maximums = []
    is_grow = False
    prev = data[0]

    for i, j in enumerate(data[1:]):
        if is_grow:
            if j < prev:
                is_grow = False
                maximums.append((i, prev))
        else:
            if j > prev:
                is_grow = True

        prev = j

    maximums.sort(key=itemgetter(1), reverse=True)
    one, two = None, None
    if maximums:
        one = maximums[0]
    if len(maximums) > 1:
        two = maximums[1]

    return (one, two)


def check(data, expected_one, expected_two):
    """
    check result of find 2 maximums in data sequence
    """
    one, two = two_max(data)
    assert one == expected_one, "{} first expected {} got {}".format(data, expected_one, one)
    assert two == expected_two, "{} second expected {} got {}".format(data, expected_two, two)


if __name__ == '__main__':
    try:
        assert not two_max([1,2])
    except ValueError as exc:
        assert "too short" in str(exc)

    check([1, 1, 1], None, None)
    check([1, 2, 3], None, None)
    check([3, 2, 1], None, None)

    # one maximum at position 1 in sequence with value 2
    check([1, 2, 1], (1, 2), None)

    check(
      [1, 2, 1, 2, 1, 2, 1],
      (1, 2),
      (3, 2)
    )
    check(
      [1, 2, 5, 6, 3, 1, 7, 9, 8],
      (7, 9),
      (3, 6)
    )
    check(
      [1, 2, 5, 6, 3, 1, 7, 9, 8, 7, 6, 5, 4, 7, 3, 2],
      (7, 9),
      (13, 7)
    )
    check(
      [1, 2, 5, 6, 6, 6, 6, 3, 1, 7, 9, 9, 9, 9, 8, 8, 8],
      (13, 9),
      (6, 6)
    )
