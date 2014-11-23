__author__ = 'giorgos'

import os

def get_disk_usage(p):
    return rec_get_disk_usage(p, 0)

def rec_get_disk_usage(p, acc):
    if os.path.isdir(p):
        for child in os.listdir(p):
            fp = os.path.join(p, child)
            acc += get_disk_usage(fp)

    else:
        acc += os.path.getsize(p)

    return acc

path = "//Users/giorgos/Workspace/Projects/WorldBeat/backend/"
total = get_disk_usage(path)

# print ( '{0:<7}'.format(total), path)


def rec_is_palindrome(s, i, j):
    if i <= j:
        return True

    return s[i] == s[j] and rec_is_palindrome(s, i+1, j-1)


def is_palindrome(s):
    return rec_is_palindrome(s, 0, len(s) - 1)


print is_palindrome('gohangasalamiimalasagnahog')