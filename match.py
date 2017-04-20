import unittest


def longest_common_substring(query, goal):
    m = [[0] * (1 + len(goal)) for i in range(1 + len(query))] # matrix with len(query) rows and len(goal) columns
    longest_length = 0
    x_longest_end_idx = 0
    print m
    for x in range(1, 1 + len(query)): # loop over all characters of the first string
        for y in range(1, 1 + len(goal)): # loop over all characters of the second string
            if query[x - 1] == goal[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest_length:
                    longest_length = m[x][y]
                    x_longest_end_idx = x
            else:
                m[x][y] = 0 # the elements are different: write a zero in the matrix
    print m
    lcs = query[x_longest_end_idx - longest_length: x_longest_end_idx]
    result = "{\"algorithm\": \"longest common substring\"," \
             " \"resultstring\": " + lcs + "," \
             " \"length\": " + str(longest_length) + " }"
    print result
    res = {'algorithm': "longest common substring", "resultString": lcs, 'length': longest_length}
    return res # return the longest common substring


def lcs(a, b):  # a = query, b = database instance
    print a
    print b
    lengths = [[0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x - 1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y - 1]:
            y -= 1
        else:
            assert a[x - 1] == b[y - 1]
            result = str(a[x - 1]) + result
            x -= 1
            y -= 1
    res = {'algorithm': "lcss", "resultString": result, 'matchLength': len(result), 'totalQueryLength': len(a)}
    return res

# longest_common_substring("aaabbbaaa", "aaababaaa")
# print lcs("aaabbbaaa", "aaababaaa")


def match():
    return "{\"results\": [ {\"title\": \"Titel 1\", \"listen\": \"Listen 1\"}, {\"title\": \"Titel 2\", \"listen\": \"Listen 2\"}, {\"title\": \"Titel 3\", \"listen\": \"Listen 3\"}, {\"title\": \"Titel 4\", \"listen\": \"Listen 4\"}, {\"title\": \"Titel 5\", \"listen\": \"Listen 5\"}  ] }"


# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- Testing ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
class MatchTestCase(unittest.TestCase):
    def test_longest_common_substring(self):
        result = longest_common_substring("aaabbbaaa", "aaababaaa")
        print result
        self.assertEqual(result["length"], 4)
        self.assertEqual(result["resultString"], "aaab")
        self.assertEqual(result["algorithm"], "longest common substring")
