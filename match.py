import unittest
import time


def longest_common_substring(query, goal):
    m = [[0] * (1 + len(goal)) for i in range(1 + len(query))]  # matrix with len(query) rows and len(goal) columns
    longest_length = 0
    x_longest_end_idx = 0
    print m
    for x in range(1, 1 + len(query)):     # loop over all characters of the first string
        for y in range(1, 1 + len(goal)):  # loop over all characters of the second string
            if query[x - 1] == goal[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest_length:
                    longest_length = m[x][y]
                    x_longest_end_idx = x
            else:
                m[x][y] = 0  # the elements are different: write a zero in the matrix
    print m
    lcs = query[x_longest_end_idx - longest_length: x_longest_end_idx]
    result = "{\"algorithm\": \"longest common substring\"," \
             " \"resultstring\": " + lcs + "," \
             " \"length\": " + str(longest_length) + " }"
    print result
    res = {'algorithm': "longest common substring", "resultString": lcs, 'length': longest_length}
    return res  # return the longest common substring


def lcs(query, db_instance):
    lengths = [[0 for j in range(len(db_instance) + 1)] for i in range(len(query) + 1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(query):
        for j, y in enumerate(db_instance):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])
    # read the substring out from the matrix
    result = ""
    x, y = len(query), len(db_instance)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x - 1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y - 1]:
            y -= 1
        else:
            assert query[x - 1] == db_instance[y - 1]
            result = str(query[x - 1]) + result
            x -= 1
            y -= 1

    edit_distance = len(query) - len(result)
    res = {'algorithm': "lcss",
           'resultString': result,
           'matchLength': len(result),
           'totalQueryLength': len(query),
           'editDistance': edit_distance}
    print query
    print db_instance
    print "result = " + result
    print "matchl = " + str(len(result))
    print "totall = " + str(len(query))
    return res

a = [1, 2, 3, 4, 5, 0, 0, 0, 0]
b = [1, 3, 4]
r = [1, 3]
#print lcs(a, b)
#print lcs(a, r)


def compute_match_score(ioi, rel_notes):
    print "compute match score"
    print "ioi.matchlength = " + str(float(ioi["matchLength"]))
    print "ioi.totallength = " + str(float(ioi["totalQueryLength"]))
    print "ioi.editdistanc = " + str(ioi["editDistance"])
    print "rel.matchlength = " + str(float(rel_notes["matchLength"]))
    print "rel.totallength = " + str(float(rel_notes["totalQueryLength"]))
    print "rel.editdistanc = " + str(rel_notes["editDistance"])

    score = 0
    print score
    ioi_edit_distance = ioi["editDistance"]
    ioi_match_length = float(ioi["matchLength"])
    ioi_total_length = float(ioi["totalQueryLength"])
    print "ioi_edit_distance / ioi_match_length = " + str(ioi_edit_distance / ioi_match_length)

    score += (ioi_match_length / ioi_total_length)
    print score

    rel_notes_edit_distance = rel_notes["editDistance"]
    rel_notes_match_length = float(rel_notes["matchLength"])
    rel_notes_total_length = float(rel_notes["totalQueryLength"])
    print "rel_notes_edit_distance / rel_notes_match_length = " + str(rel_notes_edit_distance / rel_notes_match_length)

    score += (rel_notes_match_length / rel_notes_total_length)
    print score
    # score += (float(ioi["matchLength"] / float(ioi["totalQueryLength"])))
    # score += (float(rel_notes["matchLength"] / float(rel_notes["totalQueryLength"])))
    score /= 2    # divide by the amount of calculations you did
    score *= 100  # for percents
    return score

print compute_match_score(lcs(a, b), lcs(a, b))


# -------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------- Testing ------------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
class MatchTestCase(unittest.TestCase):
    def test_longest_common_substring(self):
        result = longest_common_substring("aaabbbaaa", "aaababaaa")
        self.assertEqual(result["length"], 4)
        self.assertEqual(result["resultString"], "aaab")
        self.assertEqual(result["algorithm"], "longest common substring")
