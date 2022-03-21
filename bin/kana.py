#!/usr/bin/python3

import sys
import re
import pykakasi
import alkana
from pyokaka import okaka
import jaconv

kks = pykakasi.kakasi()
ascii_chars = re.compile('[\u0000-\u007F]+')
number_chars = re.compile('[0-9]+')

dictionary = {'SMAP': 'スマップ',
        'Official髭男dism': 'オフィシャルヒゲダンディズム',
        'L\'Arc～en～Ciel': 'ラルクアンシエル',
        'AKB48': 'エーケービーフォーティーエイト',
        'SKE48': 'エスケーイーフォーティエイト',
        'NMB48': 'エヌエムビーフォーティーエイト',
        'HKT48': 'エイチケーティーフォーティエイト',
        '関ジャニ∞': 'カンジャニエイト',
        'Kis-My-Ft2': 'キスマイフットツー',
        'Hi-STANDARD': 'ハイスタンダード',
        'KAT-TUN': 'カトゥーン',
        'EXO': 'エクソ',
        'μ\'s': 'ミューズ',
        'V6': 'ブイシックス',
        '性(サガ)': 'サガ',
        'Y.M.C.A.': 'ワイエムシーエー',
        'CHAGE＆ASKA': 'チャゲアンドアスカ',
        'CHAGE&ASKA': 'チャゲアンドアスカ',
        'B\'z': 'ビーズ',
        'WANDS': 'ワンズ',
        '中山美穂＆WANDS': 'ナカヤマミホアンドワンズ',
        'DEEN': 'ディーン',
        'T-BOLAN': 'ティーボラン',
        'ZYYG': 'ジーグ',
        'ZYYG,REV,ZARD&WANDS': 'ジーグレフザードワンズ',
        '光GENJI': 'ヒカルゲンジ',
        'BOΦWY': 'ボウイ',
        'TM NETWORK': 'ティーエムネットワーク',
        '50/50': 'フィフティフィフティ',
        'Kaoru Amane': 'カオルアマネ',
        'TOKIO': 'トキオ',
        'DJ OZMA': 'ディージェーオズマ',
        'THE ALFEE': 'ジアルフィー',
        'I to U': 'アイトユー',
        '+MILLION but-Love': 'プラス・ミリオン・バット・マイナス・ラブ',
        'YUI': 'ユイ',
        'GLAY': 'グレイ',
        'KYOSUKE HIMURO': 'キョウスケヒムロ',
        'ASKA': 'アスカ',
        'K': 'ケイ',
        'Aqua Timez': 'アクアタイムズ',
        'Kuwata Band': 'クワタバンド',
        'Song for U.S.A.': 'ソングフォーユーエスエー',
        '1986 OMEGA TRIBE': '1986オメガトライブ',
        'C-C-B': 'シーシービー',
        'CHANGE UR WORLD': 'チェンジユアワールド',
        'CHE.R.RY': 'チェリー',
        'CROSS TO YOU/ROCKIN\'MY SOUL': 'クロストゥーユー ロッキンマイソウル',
        'Cagayake! GIRLS': 'カガヤケガールズ',
        'Can\'t Stop Fallin\'in Love': 'キャントストップフォーリンラブ',
        }
english_dictionary = {'I': 'アイ',
        'Daylight': 'デイライト',
        'SUNSHINE': 'サンシャイン',
        'Sha': 'シャ',
        'la': 'ラ',
        'NOROSHI': 'ノロシ',
        'YAMATO': 'ヤマト',
        'UNLOCK': 'アンロック',
        'KinKi': 'キンキ',
        'J': 'ジェイ',
        'A': 'ア',
        'ENDLESS': 'エンドレス',
        '&': 'アンド',
        '＆': 'アンド',
        'YAH': 'ヤー',
        'Z': 'ゼット',
        'TANGO': 'タンゴ',
        'Strawberry': 'ストロベリー',
        'SAYONARA': 'サヨナラ',
        'WAKU': 'ワク',
        'Oneway': 'ワンウェイ',
        'supernova': 'スーパーノヴァ',
        '4': 'フォー',
        'CHA': 'チャ',
        'POPSTAR': 'ポップスター',
        '1000%': 'センパーセント',
        'BTS': 'ビーティーエス',
        'Dont': 'ドント',
        'DONT': 'ドント',
        }

def remove_ignore_chars(str):
    str = str.replace('(', '').replace(')', '')
    ignore_chars = ',:=？/／!-. ♂☆'
    for c in ignore_chars:
        str = str.replace(c, ' ')

    return str

def normalize(morpheme):
    kana = morpheme['kana'].strip().replace('\'', '')
    if number_chars.fullmatch(kana):
        return kana
    kana = remove_ignore_chars(kana)
    if ascii_chars.match(kana):
        words = kana.split(' ')
        kana_words = []
        for w in words:
            if w == '':
                continue
            if w in english_dictionary:
                kana_words.append(english_dictionary[w])
            else:
                ret = alkana.get_kana(w)
                if ret == None:
                    if w.lower()[-1] == 's': # 複数形
                        ret = alkana.get_kana(w[:-1])
                    if ret == None:
                        #ローマ字をカタカナに変換してみる
                        ret = jaconv.hira2kata(okaka.convert(w))
                        print('unknown spell. may need to add definetion. %s -> [%s] : [%s]' % (morpheme['orig'], w, ret), file=sys.stderr)
                        #sys.exit(1)
                        #break
                    if w[-1] == 's': # 複数形
                        ret = ret + 'ズ'
                kana_words.append(ret.strip())
        kana = ''.join(kana_words)

    return kana

def convert(str):
    if str in dictionary:
        return dictionary[str]

    morphemes = kks.convert(str)
    return ''.join(map(normalize, morphemes))

if __name__ == '__main__':
    assert convert('漢字') == 'カンジ', '漢字を変換できること'
    assert convert('漢字の') == 'カンジノ', '漢字とひらがなを変換できること'
    assert convert('English') == 'イングリッシュ', '英語を変換できること'
    assert convert('SMAP') == 'スマップ', '定義語を変換できること'
    assert convert('Official髭男dism') == 'オフィシャルヒゲダンディズム', '定義語を変換できること'
    assert convert('L\'Arc～en～Ciel') == 'ラルクアンシエル', '定義語を変換できること'
    katakana = re.compile(r'[\u30A1-\u30F4・ー、。～…『』0-9 ]+') # カタカナ
    import glob
    for filename in glob.glob('data/*.csv'):
        with open(filename, 'r') as f:
            for line in f.readlines():
                cols = line.split('\t')
                title = cols[0]
                artist = cols[1]
                convert(title)
                convert(artist)
#                assert katakana.fullmatch(convert(title)) != None, 'カタカナ変換失敗: %s -> [%s]' % (title, convert(title))
#                assert katakana.fullmatch(convert(artist)) != None, 'カタカナ変換失敗: %s -> [%s]' % (artist, convert(artist))
    

#        /MEGANE(Ver. -> [MEGANEVer]
#        FIREWORKS/ -> [FIREWORKS]
#        Someday/THE NEXT DOOR/ -> [Someday]
#        Ti Amo/SUPER SHINE/24karats -> [Ti]
#        UNSPEAKABLE/ -> [UNSPEAKABLE]
# AKATSUKI/ -> [AKATSUKI]
# Amploud/ -> [Amploud]
# B-DASH(Ver. -> [B]
# II -> [II]
# J Soul Brothers VSGENERATIONS) -> [VSGENERATIONS]
# Moon Crying        /That Ant's Cool/Once Again/Lady Go! -> [Crying]
# Shakin -> [Shakin]
# featuring Sister M -> [M]
# from AKB48 -> [AKB48]
# starring Satoshi Ohno -> [Satoshi]
# w/B. -> [w]
# with t. -> [t]
## -> [#]
#$ -> [$]
#&G -> [&G]
#&KEIKO -> [&KEIKO]
#&WANDS -> [&WANDS]
#(Fallin -> [Fallin]
#+ -> [+]
#/I'm on fire -> [Im]
#/LOOKIN'FOR MY DREAM -> [LOOKINFOR]
#/NYC -> [NYC]
#/REDBLUE -> [REDBLUE]
#/S. -> [S]
#1/2 -> [1]
#1/3 -> [1]
#100% -> [100%]
#175R -> [175R]
#2(LOVE -> [2LOVE]
#24karats TRIBE OF GOLD -> [24karats]
#2PM -> [2PM]
#3-2 -> [3]
#5/ -> [5]
#60s 70s 80s -> [60s]
#: -> [:]
#=Do! -> [=Do]
#=LOVE -> [=LOVE]
#? -> [?]
#A(Rocketeer/Brighter) -> [ARocketeer]
#AAO -> [AAO]
#ABO -> [ABO]
#AI -> [AI]
#AK-69/EUPHORIA -> [AK]
#AL-MAUJ -> [AL]
#ALWAYS(A SONG FOR LOVE) -> [ALWAYSA]
#ARIGATO -> [ARIGATO]
#AinoArika -> [AinoArika]
#Airplane pt. -> [Airplane]
#Aja -> [Aja]
#Are You There？ -> [There？]
#B -> [B]
#B. -> [B]
#BANZAI -> [BANZAI]
#BE:FIRST -> [BE:FIRST]
#BENNIE K -> [BENNIE]
#BLOWIN' -> [BLOWIN]
#BOHBO No. -> [BOHBO]
#BORDER: -> [BORDER:]
#BTS -> [BTS]
#BTS( -> [BTS]
#Baby Don't Cry -> [Dont]
#Beautiful World/Kiss&Cry -> [Kiss&Cry]
#Bittersweet -> [Bittersweet]
#Boy With Luv -> [Luv]
#Breakin'out to the morning -> [Breakinout]
#Breakthrough -> [Breakthrough]
#Breezin' -> [Breezin]
#Broken Sunset -> [Sunset]
#C-C-B -> [C]
#C-Girl -> [C]
#C. -> [C]
#CAN YOU CELEBRATE？ -> [CELEBRATE？]
#CHALLENGER(Born To Be Wild) -> [CHALLENGERBorn]
#CHANGE UR WORLD -> [UR]
#CHE. -> [CHE]
#CHIKAN! -> [CHIKAN]
#CROSS TO YOU/ROCKIN'MY SOUL -> [ROCKINMY]
#Cagayake! -> [Cagayake]
#CallingBreathless -> [CallingBreathless]
#Can You Keep A Secret？ -> [Secret？]
#Can't Stop Fallin'in Love -> [Fallinin]
#Can't stop Fallin'in Love -> [Fallinin]
#Chau -> [Chau]
#D-51 -> [D]
#D. -> [D]
#DA -> [DA]
#DA. -> [DA]
#DAYBREAK -> [DAYBREAK]
#DAYBREAK'S BELL -> [DAYBREAKS]
#DNA -> [DNA]
#DON'T U EVER STOP -> [DONT]
#Don't Leave Me -> [Dont]
#Don't look back -> [Dont]
#Don't say  -> [Dont]
#Don't wanna cry -> [Dont]
#Don't you see! -> [Dont]
#Dreamland -> [Dreamland]
#Du -> [Du]
#E. -> [E]
#EAST ENDYURI -> [ENDYURI]
#ENHYPEN -> [ENHYPEN]
#ENKA) -> [ENKA]
#ER -> [ER]
#ER2 -> [ER2]
#EXILE ATSUSHI -> [ATSUSHI]
#Endless Game -> [Endless]
#Endless sorrow -> [Endless]
#Everybody Go -> [Everybody]
#Everyday、 -> [Everyday、]
#Everything -> [Everything]
#F -> [F]
#FANTASISTA -> [FANTASISTA]
#FIREBALL -> [FIREBALL]
#FIREWORKS -> [FIREWORKS]
#FREAKY -> [FREAKY]
#FU-JI-TSU -> [FU]
#FUNK FUJIYAMA -> [FUJIYAMA]
#FUNK THE PEANUTS -> [PEANUTS]
#FUNKASTIC -> [FUNKASTIC]
#Fanfare -> [Fanfare]
#Free&Easy -> [Free&Easy]
#G -> [G]
#GAO -> [GAO]
#GLAY -> [GLAY]
#GLAYEXILE -> [GLAYEXILE]
#GReeeeN -> [GReeeeN]
#God's S. -> [S]
#Gorie with Jasmine -> [Gorie]
#Gorie with Jasmine&Joann -> [Gorie]
#Grateful Days -> [Grateful]
#H -> [H]
#H Jungle With t -> [H]
#H2O -> [H2O]
#HANABI -> [HANABI]
#HANAGOE) -> [HANAGOE]
#HELLO EP -> [EP]
#HITOMEBORE -> [HITOMEBORE]
#HKT48 feat. -> [HKT48]
#Hate tell a lie -> [a]
#High School Rock'n Roll( -> [Rockn]
#How to be a Girl -> [a]
#I am a HERO -> [a]
#I am/Muah Muah -> [Muah]
#I'm proud -> [Im]
#II  -> [II]
#II -> [II]
#INI -> [INI]
#IT'S SHOWTIME! -> [SHOWTIME]
#IZ*ONE -> [IZ*ONE]
#Imitation Rain/D. -> [D]
#JEJUNG&YUCHUN(from  -> [JEJUNG&YUCHUNfrom]
#JITTERIN'JINN -> [JITTERINJINN]
#JO1 -> [JO1]
#JUJU with JAY'ED -> [JAYED]
#JYJ -> [JYJ]
#Janne Da Arc -> [Janne]
#Joann -> [Joann]
#Jumpin'Jack Boy -> [JumpinJack]
#KA -> [KA]
#KAGUYA -> [KAGUYA]
#KAN -> [KAN]
#KANZAI BOYA -> [KANZAI]
#KARA -> [KARA]
#KATSUMI -> [KATSUMI]
#KI -> [KI]
#KISSIN -> [KISSIN]
#KIX -> [KIX]
#KNOCKIN'ON YOUR DOOR -> [KNOCKINON]
#KOKORO&KARADA/LOVE -> [KOKORO&KARADA]
#Kenji -> [Kenji]
#Kiroro -> [Kiroro]
#Koi -> [Koi]
#Komachi Angel -> [Komachi]
#L -> [L]
#L. -> [L]
#LA -> [LA]
#LA LOVE SONG -> [LA]
#LINDBERG -> [LINDBERG]
#LOVE(L. -> [LOVEL]
#LPS -> [LPS]
#Lia -> [Lia]
#Lily's e. -> [e]
#Lucky-Unlucky -> [Unlucky]
#Luv Bias -> [Luv]
#Luv Sick -> [Luv]
#M -> [M]
#M. -> [M]
#MAICCA -> [MAICCA]
#MIC Drop -> [MIC]
#MINMI -> [MINMI]
#MISIA -> [MISIA]
#MISIA+DCT -> [MISIA+DCT]
#MONSTA X -> [MONSTA]
#MUGO -> [MUGO]
#Maji -> [Maji]
#Man&Woman -> [Man&Woman]
#Melty Love -> [Melty]
#Memento-Mori -> [Mori]
#Mi-Ke -> [Mi]
#Mirrorcle World -> [Mirrorcle]
#Moonlight -> [Moonlight]
#Movin'on without you -> [Movinon]
#N -> [N]
#N. -> [N]
#NAI -> [NAI]
#NAI 16 -> [NAI]
#NANA -> [NANA]
#NANA starring MIKA NAKASHIMA -> [NANA]
#NE -> [NE]
#NGT48 -> [NGT48]
#NINJIN -> [NINJIN]
#NO TITLIST -> [TITLIST]
#NOA -> [NOA]
#NYC -> [NYC]
#Next 100 Years -> [100]
#NiziU -> [NiziU]
#O -> [O]
#O. -> [O]
#OVERNIGHT SENSATION         -> [OVERNIGHT]
#Onara -> [Onara]
#One in a million -> [a]
#Ooo Baby -> [Ooo]
#Otherside -> [Otherside]
#P -> [P]
#P. -> [P]
#PROTOSTAR( -> [PROTOSTAR]
#Part2 -> [Part2]
#Pecori Night -> [Pecori]
#Pure/You're my sunshine -> [Youre]
#Q -> [Q]
#R -> [R]
#R. -> [R]
#RA -> [RA]
#REIRA starring YUNA ITO -> [REIRA]
#RIP SLYME -> [SLYME]
#ROCK THA TOWN -> [THA]
#ROCK'N ROLL -> [ROCKN]
#ROSECOLOR -> [ROSECOLOR]
#RUI -> [RUI]
#RY -> [RY]
#Re:LIVE -> [Re:LIVE]
#Rock'n Rouge -> [Rockn]
#S (Smile On Smile) -> [S]
#S -> [S]
#S DRIVE -> [S]
#S MUSIC -> [S]
#S. -> [S]
#SAKURA -> [SAKURA]
#SEKAI NO OWARI -> [SEKAI]
#SHAZNA -> [SHAZNA]
#SIAM SHADE -> [SIAM]
#SMILY/ -> [SMILY]
#STARGAZER(OH-EH-OH) -> [STARGAZEROH]
#STEP you/is this LOVE? -> [LOVE?]
#STRANGER(REAL) -> [STRANGERREAL]
#STU48 -> [STU48]
#Sachiko -> [Sachiko]
#Sakura -> [Sakura]
#Shadow/NYC boys -> [NYC]
#SixTONES -> [SixTONES]
#SixTONES vs Snow Man -> [SixTONES]
#Someday -> [Someday]
#Something ELse -> [Something]
#Soulja -> [Soulja]
#Stand by U -> [U]
#Step and a step -> [a]
#Suger Soul feat. -> [Suger]
#Summer Heartbreak -> [Heartbreak]
#Summer Madness -> [Madness]
#Sunrise/Sunset -> [Sunrise]
#Swallowtail Butterfly -> [Swallowtail]
#T. -> [T]
#TEPPEN -> [TEPPEN]
#THE ALFEE -> [ALFEE]
#TIKI BUN -> [TIKI]
#TK PRESENTS  -> [TK]
#TMN -> [TMN]
#TOKIO/ -> [TOKIO]
#TOMORROW X TOGETHER -> [X]
#TSUNAMI -> [TSUNAMI]
#Take a picture/Poppin -> [a]
#The SHIGOTONIN -> [SHIGOTONIN]
#Theme of es -> [es]
#Ti Amo -> [Ti]
#Troublemaker -> [Troublemaker]
#U-19 -> [U]
#U. -> [U]
#UNTITLED 4 ballads -> [UNTITLED]
#USA for AFRICA -> [USA]
#UVERworld -> [UVERworld]
#UZA -> [UZA]
#Unfair World -> [Unfair]
#V. -> [V]
#V2 -> [V2]
#V6/Coming Century -> [V6]
#W. -> [W]
#WANNA BEEEE! -> [BEEEE]
#Wait&See  -> [Wait&See]
#Wanderin'Destiny -> [WanderinDestiny]
#What is LOVE？ -> [LOVE？]
#What's your name? -> [name?]
#Whiteberry -> [Whiteberry]
#Why？ -> [Why？]
#Wonderland -> [Wonderland]
#X  -> [X]
#X JAPAN -> [X]
#XIAH -> [XIAH]
#XIAH junsu -> [XIAH]
#Y -> [Y]
#Y. -> [Y]
#YUI -> [YUI]
#Ya -> [Ya]
#You're My Only SHININ'STAR -> [Youre]
#You're my sunshine -> [Youre]
#You're the Only -> [Youre]
#ZERO -> [ZERO]
#ZERO LANDMINE -> [ZERO]
#ZOKKON  -> [ZOKKON]
#ZUTTO -> [ZUTTO]
#a Day in Our Life -> [a]
#a road home -> [a]
#a song is born -> [a]
#a walk in the park -> [a]
#aiko -> [aiko]
#epo -> [epo]
#es -> [es]
#everybody goes        - -> [everybody]
#fairyland/altarna -> [fairyland]
#forgiveness -> [forgiveness]
#fragile/JIRENMA -> [JIRENMA]
#freebird -> [freebird]
#hiro -> [hiro]
#koi-wazurai -> [koi]
#komuro -> [komuro]
#m-flo -> [m]
#monochrome -> [monochrome]
#no no darlin' -> [darlin]
#nobodyknows+ -> [nobodyknows+]
#p. -> [p]
#real Emotion/1000 -> [1000]
#s fault -> [s]
#s my life/PINEAPPLE -> [s]
#s try again -> [s]
#since1999 -> [since1999]
#t Wanna Lie -> [t]
#take a chance -> [a]
#trf -> [trf]
#ve Rainbow -> [ve]
#wanna Be A Dreammaker -> [Dreammaker]
#weeeek -> [weeeek]
#with NAOMI CAMPBELL -> [NAOMI]
#youthful days -> [youthful]
#z -> [z]
#／いつかきっと… -> [イツカキット…]
#／くるみ -> [クルミ]
#／ここにしかない -> [ココニシカナイ]
#／すこしだけやさしく -> [スコシダケヤサシク]
#／すっぴん -> [スッピン]
#／ひまわり／それがすべてさ -> [ヒマワリ]
