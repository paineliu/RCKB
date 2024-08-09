from collections import defaultdict
import math
import os
g_map = defaultdict(float)

g_words = [
    '垚',
    '燚',
    '堃',
    '焱',
    '昶',
    '昱',
    '犇',
    '赟',
    '翊',
    '燊',
    '靳',
    '晟',
    '骉',
    '仝',
    '淼',
    '旻',
    '囡',
    '婧',
    '煜',
    '幢',
    '砼',
    '臻',
    '喆',
    '歆',
    '夯',
    '翀',
    '頔',
    '騳',
    '昝',
    '圩',
    '艮',
    '泵',
    '彧',
    '尛',
    '斛',
    '岑',
    '黔',
    '槑',
    '昕',
    '趸',
    '曌',
    '柘',
    '灏',
    '龘',
    '阚',
    '怼',
    '颢',
    '聿',
    '珩',
    '梓',
    '珏',
    '疃',
    '晔',
    '尕',
    '淦',
    '寅',
    '咲',
    '颉',
    '邑',
    '廿',
    '訾',
    '辊',
    '羴',
    '鋆',
    '覃',
    '矗',
    '阜',
    '叒',
    '沂',
    '晁',
    '嬲',
    '泺',
    '甦',
    '劼',
    '骅',
    '鱻',
    '罡',
    '轶',
    '灬',
    '厝',
    '熠',
    '暨',
    '舸',
    '乜',
    '酉',
    '昇',
    '喀',
    '姝',
    '弋',
    '槎',
    '滇',
    '尹',
    '烨',
    '罘',
    '尧',
    '崟',
    '汝',
    '兢',
    '岫',
    '毳',]

for file in [
    'E:/data_utf8/20150000.txt', 
    'E:/data_utf8/20150001.txt', 
    'E:/data_utf8/20150002.txt', 
    'E:/data_utf8/20150003.txt', 
    'E:/data_utf8/20150004.txt', 
    'E:/data_utf8/20150005.txt', 
    'E:/data_utf8/20150006.txt', 
    'E:/data_utf8/20150007.txt', 
    'E:/data_utf8/20150008.txt', 
    'E:/data_utf8/20150009.txt', 
    'E:/data_utf8/20150010.txt', 
    'E:/data_utf8/20150011.txt', 
    'E:/data_utf8/20150012.txt', 
    'E:/data_utf8/20150013.txt', 
    'E:/data_utf8/20150014.txt', 
    'E:/data_utf8/20150015.txt', 
    'E:/data_utf8/20150016.txt', 
    'E:/data_utf8/20150017.txt', 
    'E:/data_utf8/20150018.txt', 
    'E:/data_utf8/20150019.txt', 
    'E:/data_utf8/20150020.txt', 
    'E:/data_utf8/20150021.txt', 
    'E:/data_utf8/20150022.txt', 
    'E:/data_utf8/20150023.txt', 
    'E:/data_utf8/20150024.txt', 
    'E:/data_utf8/20150025.txt', 
    'E:/data_utf8/20150026.txt', 
    'E:/data_utf8/20150027.txt', 
    'E:/data_utf8/20150028.txt', 
    'E:/data_utf8/20150029.txt', 
    'E:/data_utf8/20150030.txt', 
    ]:
    f = open(file, encoding='utf_8')
    print(file)
    for each in f:
        each = each.rstrip()
        items = each.split('\t')
        if (int(items[1]) <= 5):
            break
        for w in g_words:
            if (w in items[0]):
                if len(items[0]) <= 5:
                    freq = math.sqrt(int(items[1]))
                    g_map[items[0]] += freq

g_list = sorted(g_map.items(), key = lambda x:x[1], reverse = True)
total = 0
os.makedirs('output', exist_ok=True)
f_out = open('output/result_phrase.txt', mode='w', encoding='utf-8')
for each in g_list:
    total += 1
    freq = int(each[1] * each[1] / 31)
    if (total == 1 or (total % 1000 == 0)):
        print(total, each[0], freq)
    f_out.write('{}\t{}\n'.format(each[0], freq))
f_out.close()
