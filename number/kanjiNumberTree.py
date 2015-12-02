#!/usr/bin/env python
# -*- coding: utf-8 -*-

## 途中

import sys
import re

PAT_ONLY_NUM = re.compile("^[0-9]+$")

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

def normalize_kanji_daiji(text):
    for before, after in load_file("./normalize.kanji_daiji.csv").items():
        text = text.replace(before, after)
    return text

class KanjiBase:
    def get_number(self,):
        return self._num
    def get_surface_form(self,):
        return self._sf
    def is_valid(self,):
        return self._is_valid

class KanjiNumber1Keta(KanjiBase):
    def __init__(self, original_form):
        self._is_valid = False
        self._sf   = normalize_kanji_daiji( original_form )
        self._num  = self.tonum( self._sf )
        self.validate()
        return
    def tonum(self, text):
        for before, after in load_file("./tonum.kanji_1keta.csv").items():
            text = text.replace(before, after)
        return text

class KanjiNumber10Keta(KanjiBase):
    def __init__(self, original_form):
        self._is_valid = False
        self._sf   = normalize_kanji_daiji( original_form )
        self._num  = self.tonum( self._sf )
        self.validate()
        return
    def tonum(self, text):
        for (pat_str, after) in kanji_10keta_patterns:
            pat = re.compile(pat_str)
            text = re.sub(pat, after, text)
        return text
    def validate(self,):
        # TODO
        self._is_valid = True

class KanjiNumber10000Keta(KanjiBase):
    def __init__(self, original_form):
        self._is_valid = False
        self._sf   = normalize_kanji_daiji( original_form )
        self._num  = self.tonum( self._sf )
        self.validate()
        return
    def tonum(self, text):
        for (pat_str, after) in kanji_10000keta_patterns:
            pat = re.compile(pat_str)
            text = re.sub(pat, after, text)
        return text
    def validate(self,):
        # TODO
        self._is_valid = True

class ParseException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class KanjiNumber(KanjiBase):
    def __init__(self, original_form):
        self._is_valid = False
        self._sf   = normalize_kanji_daiji( original_form )
        self._tree = self.build_tree( self._sf )
        self._num  = self.tonum( self._sf )
        self.validate()
        return
    def build_tree(self, text):
        try:
            keta_names = load_file("./tonum.kanji_10000keta.csv").keys()
            return self._build_tree(text, keta_names)
        except ParseException, e:
            self._is_valid = False
            raise ParseException("Parse failed")
    def _build_tree(self, text, keta_names):
        if len(keta_names) == 0:
            _text = KanjiNumber10Keta(text)
            if _text.is_valid() == False:
                raise ParseException("Parse failed")
            return _text
        if keta_names[0] in text:
            (leftside, rightside) = text.split(keta_names[0])
        else:
            return self._build_tree(text, keta_names[1:])
        _leftside  = KanjiNumber10Keta(leftside)
        _rightside = self._build_tree(rightside, keta_names[1:])
        if _leftside.is_valid() == False:
            raise ParseException("Parse Error")
        return {
            "keta": keta_names[0], 
            "leftside":  _leftside,
            "rightside": _rightside,
            }
    def validate(self,):
        m = re.search(PAT_ONLY_NUM, self._num)
        if m:
            self._is_valid = True
        else:
            self._is_valid = False
    def tonum(self, text):
        for (pat_str, after) in kanji_10000keta_patterns:
            pat = re.compile(pat_str)
            text = re.sub(pat, after, text)
        return text
    def get_number(self,):
        return self._num
    def get_number1(self,):
        # TODO
        return self._num
    def get_number2(self,):
        # TODO
        return self._num
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
                           k.is_valid(),
                           k.get_number1(),
                           k.get_number2(),
                           k.get_number(),
                           )
                         )

if __name__ == '__main__':
    main()
