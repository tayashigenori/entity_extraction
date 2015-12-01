#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def is_valid_mynumber(mynumber):
    mynumber_str = str(mynumber)
    if len(mynumber_str) != 12:
        return False
    return int(mynumber_str[-1]) == get_checksum(mynumber_str[:-1])

def get_checksum(mynumber_11keta, verbose = True):
    p_list = mynumber_11keta[::-1]
    q_list = [n+1 for n in range(1, 7)] + [n-5 for n in range(7, 12)]
    pnqn = sum(
        map(lambda str1,str2: int(str1)*int(str2), p_list, q_list)
        )
    rem = pnqn % 11
    ans = 0 if rem in (1,2) else 11 - rem
    if verbose:
        sys.stderr.write("--ans %s for mynumber(11 keta): %s\n" %(ans, mynumber_11keta))
    return ans

def main():
    print is_valid_mynumber(123456789010)
    print is_valid_mynumber(123456789011)
    print is_valid_mynumber(123456789012)
    print is_valid_mynumber(123456789013)
    print is_valid_mynumber(123456789014)
    print is_valid_mynumber(123456789015)
    print is_valid_mynumber(123456789016)
    print is_valid_mynumber(123456789017)
    print is_valid_mynumber(123456789018)
    print is_valid_mynumber(123456789019)
    print is_valid_mynumber("023456789010")

if __name__ == '__main__':
    main()
