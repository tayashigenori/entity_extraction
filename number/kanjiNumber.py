#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

def load_file(filename):
    r = {}
    f = open(filename)
    try:
        for l in f.readlines():
            l = unicode(l.strip(), 'utf-8')
            (before, after) = l.split(u",")
            r[before] = after
    finally:
        f.close()
    return r

"""
large_kanji_patterns = {
    re.compile(u"万(?=[0-9]{4})") : "0" * 0,
    re.compile(u"万(?=[0-9]{3})") : "0" * 1,
    re.compile(u"万(?=[0-9]{2})") : "0" * 2,
    re.compile(u"万(?=[0-9]{1})") : "0" * 3,
    re.compile(u"万(?=[0-9]{0})") : "0" * 4,
    re.compile(u"億(?=[0-9]{8})") : "0" * 0,
    re.compile(u"億(?=[0-9]{7})") : "0" * 1,
    re.compile(u"億(?=[0-9]{6})") : "0" * 2,
    re.compile(u"億(?=[0-9]{5})") : "0" * 3,
    re.compile(u"億(?=[0-9]{4})") : "0" * 4,
    re.compile(u"億(?=[0-9]{3})") : "0" * 5,
    re.compile(u"億(?=[0-9]{2})") : "0" * 6,
    re.compile(u"億(?=[0-9]{1})") : "0" * 7,
    re.compile(u"億(?=[0-9]{0})") : "0" * 8,
    ....
    }
small_kanji_patterns = {
    re.compile(u"十(?=[0-9]{1})") : "0" * 0
    re.compile(u"十(?=[0-9]{0})") : "0" * 1
    re.compile(u"百(?=[0-9]{2})") : "0" * 0
    re.compile(u"百(?=[0-9]{1})") : "0" * 1
    re.compile(u"百(?=[0-9]{0})") : "0" * 2
    re.compile(u"千(?=[0-9]{3})") : "0" * 0
    re.compile(u"千(?=[0-9]{2})") : "0" * 1
    re.compile(u"千(?=[0-9]{1})") : "0" * 2
    re.compile(u"千(?=[0-9]{0})") : "0" * 3
    )
"""

PAT_ONLY_NUM = re.compile("^[0-9]+$")

kanji_10000keta_patterns = []
for large_kanji, power in load_file("./tonum.kanji_10000keta.csv").items():
    kanji_10000keta_patterns += [
        (u"%s(?=[0-9]{%d})" %(large_kanji, int(power)-i), "0" * i)
        for i in range(5)
        ]

kanji_10keta_patterns = []
for small_kanji, power in load_file("./tonum.kanji_10keta.csv").items():
    kanji_10keta_patterns += [
        (u"%s(?=[0-9]{%d})" %(small_kanji, int(power)-i), "0" * i)
        for i in range(5)
        ]

class KanjiNumber:
    def __init__(self, original_form):
        self._is_valid = False
        self._sf   = self.normalize_kanji_daiji( original_form )
        self._num1 = self.tonum_kanji_1keta(     self._sf      )
        self._num2 = self.tonum_kanji_10keta(    self._num1    )
        self._num  = self.tonum_kanji_10000keta( self._num2    )
        self.validate()
        return
    """
    validation
    """
    def validate(self,):
        m = re.search(PAT_ONLY_NUM, self._num)
        if m:
            self._is_valid = True
        else:
            self._is_valid = False
    def is_valid_number(self,):
        return self._is_valid
    """
    normalize
    """
    def normalize_kanji_daiji(self, text):
        for before, after in load_file("./normalize.kanji_daiji.csv").items():
            text = text.replace(before, after)
        return text
    """
    to num
    """
    def tonum_kanji_1keta(self, text):
        for before, after in load_file("./tonum.kanji_1keta.csv").items():
            text = text.replace(before, after)
        return text
    def tonum_kanji_10keta(self, text):
        for (pat_str, after) in kanji_10keta_patterns:
            pat = re.compile(pat_str)
            text = re.sub(pat, after, text)
        return text
    def tonum_kanji_10000keta(self, text):
        for (pat_str, after) in kanji_10000keta_patterns:
            pat = re.compile(pat_str)
            text = re.sub(pat, after, text)
        return text
    """
    getter
    """
    def get_number(self,):
        return self._num
    def get_number1(self,):
        return self._num1
    def get_number2(self,):
        return self._num2
    def get_surface_form(self,):
        return self._sf

def main():
    nums = [u"五万",
            u"五万五千",
            u"５５万３３３３３３"
            ]
    for n in nums:
        k = KanjiNumber(n)
        sys.stdout.write("""number %s is valid? %d
normailzed to:
\t%s
\t%s
\t%s\n"""
                         %(k.get_surface_form(),
                           k.is_valid_number(),
                           k.get_number1(),
                           k.get_number2(),
                           k.get_number(),
                           )
                         )

if __name__ == '__main__':
    main()
