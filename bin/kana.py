#!/usr/bin/python3

import sys
import re
import json
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
        'ALFEE': 'アルフィー',
        'I to U': 'アイトユー',
        '+MILLION but-Love': 'プラス・ミリオン・バット・マイナス・ラブ',
        'YUI': 'ユイ',
        'GLAY': 'グレイ',
        'GLAY×EXILE': 'グレイ エグザイル',
        'GLAY feat.KYOSUKE HIMURO': 'グレイ キョウスケヒムロ',
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
        'Can\'t stop Fallin\'in Love': 'キャントストップフォーリンラブ',
        'B.B.クィーンズ': 'ビービークィーンズ',
        'LINDBERG': 'リンドバーグ',
        'TMN': 'ティーエムエヌ',
        'X': 'エックス',
        'X JAPAN': 'エックスジャパン',
        'シャ乱Q': 'シャランキュー',
        'H Jungle With t': 'エイチジャングルウィズティー',
        '2PM': 'トゥーピーエム',
        'T.C.R.横浜銀蝿R.S.': 'ザ・クレイジー・ライダー ヨコハマギンバエ ローリング・スペシャル',
        'T.M.Revolution': 'ティーエムレボルーション',
        'T.M.Revolution×水樹奈々': 'ティーエムレボルーション ミズキナナ',
        'キ・ス・ウ・マ・イ 〜KISS YOUR MIND〜/S.O.S (Smile On Smile)': 'キ・ス・ウ・マ・イ エスオーエス',
        'EXILE TRIBE  (三代目 J Soul Brothers VSGENERATIONS)': 'エグザイルトライブサンダイメジェイソウルブラザーズブイエスジェネレーションズ',
        'SNOW DOMEの約束／Luv Sick': 'スノードームノヤクソク',
        'Calling×Breathless': 'コーリング ブレスレス',
        '175R': 'イナゴライダー',
        'GReeeeN': 'グリーン',
        'FREAKY': 'フリーキー',
        'Free&Easy': 'フリーアンドイージー',
        'freebird': 'フリーバード',
        'RIP SLYME': 'リップスライム',
        'trf': 'ティーアールエフ',
        'STU48': 'エスティーユーフォーティーエイト',
        'Whiteberry': 'ホワイトベリー',
        'BTS(防弾少年団)': 'ビーティーエス',
        'FAKE LOVE／Airplane pt.2': 'フェイクラブ エアプレインパートツー',
        'J.S.B. HAPPINESS': 'ジェイエスビー・ハピネス',
        'LPS': 'エルピーエス',
        'LOVE(L.O.V.E.)': 'ラブ',
        'エル・オー・ヴィ・愛・N・G': 'エル・オー・ヴイ・アイ・エヌ・ジー',
        'L⇔R': 'エルアール',
        '浜崎あゆみ&KEIKO': 'ハマサキアユミ ケイコ',
        'H': 'エイチ',

        'Deep in your heart/+MILLION but-Love': 'ディープインユアハート',
        'M': 'エム',
        'ZERO LANDMINE': 'ゼロ・ランドマイン',
        'N.M.L.': 'エヌエムエル',
        '『Lily\'s e.p.』 Amploud/静かな日々の階段を': 'アンプラウド',
        'm-flo': 'エムフロー',
        '忌野清志郎+坂本龍一': 'イマワノキヨシロウ サカモトリュウイチ',
        '$百萬BABY': 'ヒャクマンドルベイビー',
        '100%…SOかもね!': '100パーセントソウカモネ',
        'NAI・NAI 16': 'ナイナイシックスティーン',
        '1/2の神話': 'ニブンノイチノシンワ',
        'H2O': 'エイチツーオー',
        '篠原涼子 with t.komuro': 'シノハラリョウコ',
        '『The Birthday ～Ti Amo～』        Ti Amo/SUPER SHINE/24karats': 'ティアーモ',
        '『60s 70s 80s』        NEW LOOK/ROCK STEADY/WHAT A FEELING': 'ニュールック',
        '爪爪爪/「F」': 'ツメツメツメ',
        '『MOON』 Moon Crying        /That Ant\'s Cool/Once Again/Lady Go!': 'ムーンクライング',
        'TK PRESENTS こねっと': 'ティーケープレゼンツコネット',
        '1/2': 'ニブンノイチ',
        '坂本龍一 featuring Sister M': 'サカモトリュウイチ シスターエム',
        '愛なんだ/LOOKIN\'FOR MY DREAM': 'アイナンダ',
        'V6/Coming Century': 'ブイシックス',
        'S．O．S': 'エスオーエス',
        '#好きなんだ': 'スキナンダ',
        'MIC Drop／DNA／Crystal Snow ': 'マイクドロップ',
        'Hey！Say！JUMP／A.Y.T.': 'ヘイセイジャンプ',
        '亀と山P': 'カメトヤマピー',
        'ROCK THA TOWN': 'ロックザタウン',
        'God\'s S.T.A.R.': 'ゴッド',
        'BLOWIN\'': 'ブロウウィン',
        '部屋とYシャツと私': 'ヘヤトワイシャツトワタシ',
        'KIX・S': 'キックス',
        'X ': 'エックス',
        '涙2(LOVEヴァージョン)': 'ナミダナミダ',
        '中山美穂&WANDS': 'ナカヤマミホ ワンズ',
        'V2': 'ブイツー',
        'HEAVEN’S DRIVE': 'ヘブンズドライブ',
        'Breakin\'out to the morning': 'ブレイキンアウトゥーザモーニング',
        'Let’s try again': 'レッツトライアゲイン',
        'T.W.L／イエローパンジーストリート': 'ティーダブルエル',
        'Don’t Wanna Lie': 'ドントワナライ',
        'P.S.I LOVE YOU': 'ピーエスアイラブユー',
        'C-Girl': 'シーガール',
        '&G': 'アンジー',
        'HKT48 feat.氣志團': 'エイチケーティーフォーティーエイト キシダン',
        'O.R.I.O.N.': 'オリオン',
        'B’z': 'ビーズ',
        'JYJ': 'ジェイワイジェイ',
        'R.Y.U.S.E.I.': 'リュウセイ',
        'C.O.S.M.O.S.～秋桜～': 'コスモス',
        'STRANGER(REAL)': 'ストレンジャー',
        'Luv Bias': 'ラブバイアス',
        'We Just Go Hard feat.AK-69/EUPHORIA': 'ウィージャストゴーハード',
        'LET’S MUSIC': 'レッツミュージック',
        '1/3の純情な感情': 'サンブンノイチノジュンジョウナカンジョウ',
        'wanna Be A Dreammaker': 'ワナビーアドリームメイカー',
        'Troublemaker': 'トラブルメイカー',
        'Lφve Rainbow': 'ラヴ・レインボー',
        'XIAH': 'シア',
        'XIAH junsu': 'シア ジュンス',
        'Lia／多田葵': 'リア タダアオイ',
        'Lights／Boy With Luv': 'ライツ',
        'Breakthrough': 'ブレイクスルー',
        'MONSTA X': 'モンスタエックス',
        '純情U-19': 'ジュンジョウアンダーナインティーン',
        '24karats TRIBE OF GOLD': 'トゥエンティーフォーカラッツ トライブ オブ ゴールド',
        'D-51': 'ディー・ゴー・イチ',
        'Dreamland': 'ドリームランド',
        'BENNIE K': 'ベニーケー',
        'STEP you/is this LOVE?': 'ステップユー',
        'SMILY/ビー玉': 'スマイリー',
        '『トンガリキッズ I 』 B-DASH(Ver.HANAGOE)        /MEGANE(Ver.HANAGOE)': 'ビーダッシュ',
        'BOHBO No.5/神の島遙か国': 'ボーボ・ナンバー・ファイヴ',
        'Imitation Rain/D.D.': 'イミテーションレイン',
        'SixTONES vs Snow Man': 'ストーンズ スノーマン',
        'Nobody’s fault': 'ノーバディーズ・フォルト',
        'PROTOSTAR(無限大)': 'プロトスター',
        'ソーユートコあるよね?': 'ソーユートコアルヨネ',
        'STARGAZER(OH-EH-OH)': 'スターゲイザー',
        '3-2': 'サンヒクニ',
        'It’s my life/PINEAPPLE': 'イッツマイライフ',
        'TOMORROW X TOGETHER': 'トゥモロー・バイ・トゥギャザー',
        'real Emotion/1000の言葉': 'リアルエモーション',
        '中山優馬 w/B.I.Shadow/NYC boys': 'ナカヤマユウマ',
        'R.I.P./Merry Christmas': 'アール アイ ピー',
        'JEJUNG&YUCHUN(from 東方神起)': 'ジェジュンユチョン ',
        '∞SAKAおばちゃんROCK/大阪ロマネスク': 'オオサカオバチャンロック',
        'OH！！ POPSTAR': 'オオポップスター',
        'Broken Sunset': 'ブロークンサンセット',
        'MISIA+DCT': 'ミーシャ・プラス・ドリームズ・カム・トゥルー',
        'ラッツ＆スター': 'ラッツアンドスター',
        'さらば‥夏': 'サラバナツ',
        'Jumpin\'Jack Boy': 'ジャンピンジャックボーイ',
        '昭和枯れすゝき': 'ショウワカレススキ',
        '青山テルマ feat.Soulja': 'アオヤマテルマ ソルジャ',
        'UVERworld': 'ウーバーワールド',
        'Wanderin\'Destiny': 'ワンダリン・デスティニー',
        'SHAZNA': 'シャズナ',
        'NGT48': 'エヌジーティーフォーティーエイト',
        'ツッパリHigh School Rock\'n Roll(登校編)': 'ツッパリハイスクールロックンロール',
        'だんご３兄弟': 'ダンゴサンキョウダイ',
        'モーニング娘。\'15': 'モーニングムスメ',
        'モーニング娘。\'17': 'モーニングムスメ',
        'モーニング娘。\'19': 'モーニングムスメ',
        'LOVE～Destiny～/LOVE～since1999～': 'ラブデスティニー',
        'Everyday、カチューシャ': 'エブリデイカチューシャ',
        'NYC': 'エヌワイシー',
        'ROSECOLOR': 'ローズカラー',
        'GO-BANG\'S': 'ゴーバンズ',
        'NO TITLIST': 'ノン タイトリスト',
        'AL-MAUJ': 'アルマージ',
        'nobodyknows+': 'ノーバディノウズ',
        'Otherside／愛が止まるまでは': 'アザーサイド',
        'ER': 'イーアール',
        'ER2': 'イーアール ツー',
        'A(Rocketeer/Brighter)': 'ロケッティアー',
        'CHALLENGER(Born To Be Wild)': 'チャレンジャー ボーントゥービーワイルド',
        'ENHYPEN': 'エンハイフン',
        '明日が聴こえる/Children\'s Holiday': 'アシタガキコエル',
        'SIAM SHADE': 'シャムシェイド',
        'チームドラゴン from AKB48': 'チームドラゴン フロム エーケービーフォーティーエイト',
        'IZ*ONE': 'アイズワン',
        'Lucky-Unlucky／Oh！ my darling': 'ラッキーアンラッキー',
        'fairyland/altarna': 'フェアリーランド',
        '泣いたりしないで/RED×BLUE': 'ナイタリシナイデ',
        'Gorie with Jasmine&Joann': 'ゴリエ・ウィズ・ジャスミン・アンド・ジョアン',
        '舞い落ちる花びら(Fallin’ Flower)': 'マイオチルハナビラ',
        'I am/Muah Muah': 'アイアム',
        '青春“サブリミナル”': 'セイシュンサブリミナル',
        'IT\'S SHOWTIME!!': 'イッツショウタイム',
        '『UNTITLED 4 ballads』        UNSPEAKABLE/愛の謳/ルーム/nostalgia': 'アンスピーカブル',
        '『THE HURRICANE ～FIREWORKS～』        FIREWORKS/優しい光/…': 'ファイヤーワークス',
        '『THE MONSTER ～Someday～』        Someday/THE NEXT DOOR/愛すべき未来へ/…': 'サムデイ',
        'Don\'t say ”lazy”': 'ドントセイレイジー',
        'Beautiful World/Kiss&Cry': 'ビューティフルワールド',
        'ALWAYS(A SONG FOR LOVE)': 'オルウェイズ',
        'FUNKASTIC': 'ファンカスティック',
        '【es】～Theme of es～': 'エス',
        'MAICCA～まいっか': 'マイッカ',
        'あなただけを～Summer Heartbreak～': 'アナタダケヲ サマーハートブレイク',
        'Wait&See ～リスク～': 'ウェイト・アンド・シー リスク',
        'ﾊﾞｨﾊﾞｨDuﾊﾞｨ～See you again～／A MY GIRL FRIEND': 'バイバイ・ドゥバイ シー・ユー・アゲイン ア・マイ・ガール・フレンド',
        }
english_dictionary = {'I': 'アイ',
        'Daylight': 'デイライト',
        'SUNSHINE': 'サンシャイン',
        'Sha': 'シャ',
        'la': 'ラ',
        'LA': 'ラ',
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
        'Swallowtail': 'スワローテイル',
        '100': 'ワンハンドレッド',
        'KNOCKINON': 'ノッキングオン',
        'Breezin': 'ブリージン',
        'SixTONES': 'ストーンズ',
        'Grateful': 'グレイトフル',
        'Everything': 'エブリシング',
        'Endless': 'エンドレス',
        'youthful': 'ユースフル',
        'Moonlight': 'ムーンライト',
        'Mirrorcle': 'ミラクル',
        'FIREBALL': 'ファイヤーボール',
        'Melty': 'メルティ',
        'darlin\'': 'ダーリン',
        'monochrome': 'モノクローム',
        'X\'MAS': 'クリスマス',
        'X\'mas': 'クリスマス',
        'Movin\'on': 'ムービンオン',
        'Something': 'サムシング',
        'Suger': 'シュガー',
        'Everybody': 'エブリバディ',
        'Mother\'s': 'マザーズ',
        'LOVER\'S': 'ラバーズ',
        'DAYBREAK': 'デイブレイク',
        'SHININ\'STAR': 'シャイニンスター',
        'name?': 'ネーム',
        'Wonderland': 'ワンダーランド',
        'Madness': 'マッドネス',
        'Unfair': 'アンフェア',
        'Bittersweet': 'ビタースウィート',
        'ROCK\'N': 'ロックン',
        'ROLL': 'ロール',
        'Pecori': 'ペコリ',
        'EP': 'イーピー',
        'Breezin\'': 'ブリージン',
        'forgiveness': 'フォーギブネス',
        'Ohno': 'オーノ',
        'NYC': 'エヌワイシー',
        'JAY\'ED': 'ジェイド',
        'Sunset': 'サンセット',
        'weeeek': 'ウィーク',
        'DAYBREAK\'S': 'デイブレイカーズ',
        'Part2': 'パートツー',
        'FANTASISTA': 'ファンタジスタ',
        'KNOCKIN\'ON': 'ノッキンオン',
        'everybody': 'エブリバディ',
        'OVERNIGHT': 'オーバーナイト',
        'MONKEY\'S': 'モンキーズ',
        'PEANUTS': 'ピーナッツ',
        'Rock\'n': 'ロックン',
        }

def remove_ignore_chars(str):
    str = str.replace('(', '').replace(')', '')
    ignore_chars = ',:=？/／!-. ♂☆'
    for c in ignore_chars:
        str = str.replace(c, ' ')

    return str

def normalize(morpheme):
    kana = morpheme['kana'].strip() #.replace('\'', '')
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
                        if ascii_chars.match(ret):
                            raise Exception('unknown spell. may need to add definetion. %s -> [%s] : [%s]' % (morpheme['orig'], w, ret))
                    if w[-1] == 's': # 複数形
                        ret = ret + 'ズ'
                kana_words.append(ret.strip())
        kana = ''.join(kana_words)

    return kana

def convert(str):
    if str in dictionary:
        return dictionary[str]

    try:
        morphemes = kks.convert(str)
        return ''.join(map(normalize, morphemes))
    except Exception as e:
        print('[%s] %s' % (str, e), file=sys.stderr)

songs = []
class Song:
    title = ''
    artist = ''
    chars = []
    sales = 0
    def __init__(self, title, artist, title_kana, artist_kana, sales):
        self.title = title
        self.artist = artist
        self.chars = list(set(list(title_kana + artist_kana)))
        self.sales = int(sales)


if __name__ == '__main__':
    assert convert('漢字') == 'カンジ', '漢字を変換できること'
    assert convert('漢字の') == 'カンジノ', '漢字とひらがなを変換できること'
    assert convert('English') == 'イングリッシュ', '英語を変換できること'
    assert convert('SMAP') == 'スマップ', '定義語を変換できること'
    assert convert('Official髭男dism') == 'オフィシャルヒゲダンディズム', '定義語を変換できること'
    assert convert('L\'Arc～en～Ciel') == 'ラルクアンシエル', '定義語を変換できること'
    katakana = re.compile('[\u30A1-\u30F4・★＃＊∞’！－ー、。，&～…「」『』（）“＆0-9 ]+') # カタカナ
    import glob
    for filename in glob.glob('data/*.csv'):
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.rstrip()
                cols = line.split('\t')
                title = cols[0]
                artist = cols[1]
                sales = cols[2]
                convert_title = convert(title)
                assert katakana.fullmatch(convert_title) != None, 'カタカナ変換失敗: %s -> [%s]' % (title, convert_title)
                convert_artist = convert(artist)
                assert katakana.fullmatch(convert_artist) != None, 'カタカナ変換失敗: %s -> [%s]' % (artist, convert_artist)
                songs.append(Song(title, artist, convert_title, convert_artist, sales).__dict__)

    with open('data/songs.json', 'w') as f:
        json.dump(songs, f, indent=2)

    


