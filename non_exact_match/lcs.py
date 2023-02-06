import numpy as np


def lcsubstring(string1, string2):
    len_s1 = 1 + len(string1)
    len_s2 = 1 + len(string2)

    m = np.zeros((len_s1, len_s2), dtype=int).tolist()

    longest, x_longest = 0, 0
    for x in range(1, len_s1):
        for y in range(1, len_s2):
            if string1[x - 1] == string2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = y
            #                     print(string2[x_longest - longest: x_longest])
            else:
                m[x][y] = 0
    return string2[x_longest - longest: x_longest], x_longest - longest, x_longest, longest
