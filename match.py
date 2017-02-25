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
   return result # return the longest common substring

# other method: longest common subsequence (tolerance)
def lcss(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C

def backTrack(C, X, Y, i, j):
    if i == 0 or j == 0:
        return ""
    elif X[i-1] == Y[j-1]:
        return backTrack(C, X, Y, i-1, j-1) + X[i-1]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backTrack(C, X, Y, i, j-1)
        else:
            return backTrack(C, X, Y, i-1, j)

def backTrackAll(C, X, Y, i, j):
    if i == 0 or j == 0:
        return set([""])
    elif X[i-1] == Y[j-1]:
        return set([Z + X[i-1] for Z in backTrackAll(C, X, Y, i-1, j-1)])
    else:
        R = set()
        if C[i][j-1] >= C[i-1][j]:
            R.update(backTrackAll(C, X, Y, i, j-1))
        if C[i-1][j] >= C[i][j-1]:
            R.update(backTrackAll(C, X, Y, i-1, j))
        return R

longest_common_substring("aaabbbaaa", "aaababaaa")
print backTrack(lcss("aaabbbaaa", "aaababaaa"), "aaabbbaaa", "aaababaaa",len("aaabbbaaa"), len("aaababaaa"))

#print json.dump(longestCommonSubstring("test", "lol"))


def match():
    return "{\"result\":{\"lol\": \"xxx\"}}"

#print(longestCommonSubstring("Hello World", "nyi"))