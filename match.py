import json

def longestCommonSubstring(query, goal):
    return query + ", len = " + str(len(query))

print longestCommonSubstring("test", "lol")

#print json.dump(longestCommonSubstring("test", "lol"))


def match():
    return "{\"result\":{\"lol\": \"xxx\"}}"

#print(longestCommonSubstring("Hello World", "nyi"))