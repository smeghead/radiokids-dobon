#!/usr/bin/python3

import sys
import re
import pykakasi
import alkana

kks = pykakasi.kakasi()
ascii_chars = re.compile('[\u0000-\u007F]+')

dictionary = {'SMAP': 'スマップ',
        'Official髭男dism': 'オフィシャルヒゲダンディズム',
        'L\'Arc～en～Ciel': 'ラルクアンシエル',
        }

def normalize(morpheme):
    kana = morpheme['kana']
    if ascii_chars.match(kana):
        ret = alkana.get_kana(kana)
        if ret == None:
            print('unknown spell. may need to add definetion. [%s]' % kana, file=sys.stderr)
            sys.exit(1)
        kana = ret

    return kana

def convert(str):
    if str in dictionary:
        return dictionary[str]

    morphemes = kks.convert(str)
    #print(morphemes)
    return ''.join(map(normalize, morphemes))

if __name__ == '__main__':
    assert convert('漢字') == 'カンジ', '漢字を変換できること'
    assert convert('漢字の') == 'カンジノ', '漢字とひらがなを変換できること'
    assert convert('English') == 'イングリッシュ', '英語を変換できること'
    assert convert('SMAP') == 'スマップ', '定義語を変換できること'
    assert convert('Official髭男dism') == 'オフィシャルヒゲダンディズム', '定義語を変換できること'
    assert convert('L\'Arc～en～Ciel') == 'ラルクアンシエル', '定義語を変換できること'
    
