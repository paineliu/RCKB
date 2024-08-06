import os
import math

def find_postfix_fixlen_word(filename, postfix_list):
    map_word = {}

    f = open(filename, 'r', encoding='utf-8')
    for each in f:
        items = each.split()
        query = items[0]
        han = query[0]
        freq = int(items[1])
        for postfix in postfix_list:
            if (postfix == query[1:]):
                map_word[han] = map_word.get(han, 0) + freq
    f.close()
    return map_word

def stat_single_match(data_path, postfix_list, out_file, all_file):
    f_total = 0
    map_all_word = {}
    map_word_day = {}
    for root,dirs,files in os.walk(data_path):
        for file in files:
            f_total += 1
            fullname = os.path.join(root, file)
            print('load', fullname, end='\r')
            map_word = find_postfix_fixlen_word(fullname, postfix_list)
            day = fullname[-12:-4]

            for each in map_word:
                map_all_word[each] = map_all_word.get(each, 0) + math.sqrt(map_word[each])
                if each not in map_word_day:
                    map_word_day[each] = []
                map_word_day[each].append([day, map_word[each]])
    print()

    lst_word = sorted(map_all_word.items(), key = lambda x: x[1], reverse = True)

    print('write', out_file)
    f = open(out_file, 'w', encoding='utf-8')
    for each in lst_word:
        s = '{}\t{}'.format(each[0], int((each[1] * each[1]) / f_total))
        f.write('{}\n'.format(s))
    f.close()

    print('write', all_file)
    f = open(all_file, 'w', encoding='utf-8')
    for each in map_word_day:
        for item in map_word_day[each]:
            s = '{}\t{}\t{}'.format(each, item[0], item[1])
            f.write('{}\n'.format(s))
    f.close()

def find_chaizi_word(filename, postfix_list):
    map_word = {}

    f = open(filename, 'r', encoding='utf-8')
    for each in f:
        items = each.split()
        query = items[0]
        freq = int(items[1])
        for postfix in postfix_list:
            if (postfix in query):
                han = query[0:-len(postfix)]
                if len(han) > 1:
                    map_word[han] = map_word.get(han, 0) + freq
                break
    f.close()
    return map_word


def stat_chaizi_match(data_path, postfix_list, out_file, all_file):
    f_total = 0
    map_all_word = {}
    map_word_day = {}
    for root,dirs,files in os.walk(data_path):
        for file in files:
            f_total += 1
            fullname = os.path.join(root, file)
            print('load', fullname, end='\r')
            map_word = find_chaizi_word(fullname, postfix_list)
            day = fullname[-12:-4]
            for each in map_word:
                map_all_word[each] = map_all_word.get(each, 0) + math.sqrt(map_word[each])
                if each not in map_word_day:
                    map_word_day[each] = []
                map_word_day[each].append([day, map_word[each]])
    print()

    lst_word = sorted(map_all_word.items(), key = lambda x: x[1], reverse = True)

    print('write', out_file)
    f = open(out_file, 'w', encoding='utf-8')
    for each in lst_word:
        s = '{}\t{}'.format(each[0], int((each[1] * each[1]) / f_total))
        f.write('{}\n'.format(s))
    f.close()

    print('write', all_file)
    f = open(all_file, 'w', encoding='utf-8')
    for each in map_word_day:
        for item in map_word_day[each]:
            s = '{}\t{}\t{}'.format(each, item[0], item[1])
            f.write('{}\n'.format(s))
    f.close()

def read_chaizi_info(filenames):
    map_rad = {}
    map_rad_han = {}
    for filename in filenames:
        print('load', filename)
        if (not '.csv' in filename):
            f_chaizi = open(filename, 'r', encoding='utf-8')
            for each in f_chaizi:
                each = each.strip()
                items = each.split('\t')
                han = items[0]
                rads = items[1].split()
                if (han not in map_rad):
                    map_rad[han]  = []
                map_rad[han].append(rads)
            f_chaizi.close()
        else:
            f_chaizi = open(filename, 'r', encoding='utf-8')
            for each in f_chaizi:
                each = each.strip()
                items = each.split(',')
                han = items[0]
                if(len(items[2]) > 0):
                    rads = items[2].split()
                    if (han not in map_rad):
                        map_rad[han]  = []
                    map_rad[han].append(rads)
            f_chaizi.close()
    for han in map_rad:
        new_rads = []
        has_sub = False
        for rads in map_rad[han]:
            for rad in rads:
                if rad in map_rad:
                    subs = map_rad[rad]
                    
                    for sub in subs:
                        for i in sub:
                            new_rads.append(i)
                    has_sub = True
                else:
                    new_rads.append(rad)
        if has_sub:
            map_rad[han].append(new_rads)

    for han in map_rad:
        for rads in map_rad[han]:
            rad_str = ''
            for sub in rads:
                rad_str += sub
            if (rad_str in map_rad_han):
                if (han not in map_rad_han[rad_str]):
                    map_rad_han[rad_str].append(han)
            else:
                map_rad_han[rad_str] = [han]

    return map_rad_han, map_rad

def make_chaizi_data(chaizi_filenames, query_filename, out_filename, log_filename):

    map_chaizi, map_han = read_chaizi_info(chaizi_filenames)
    print('write', out_filename)
    f = open(query_filename, 'r', encoding='utf-8')
    f_o = open(out_filename, 'w', encoding='utf-8')
    f_l = open(log_filename, 'w', encoding='utf-8')

    for each in f:
        each = each.strip()
        items = each.split()
        query = items[0]
        freq = int(items[1])
        jiegou = ''
        if freq == 0:
            break
        han = ''

        if '下' in query or '上' in query:
            jiegou = 'up-down'
        elif '左边' in query or '右边' in query:
            jiegou = 'left-right'

        query = query.replace('下面', '')
        query = query.replace('上面', '')
        query = query.replace('字里面', '')
        query = query.replace('里面', '')
        query = query.replace('一个', '')
        query = query.replace('加个', '')
        query = query.replace('加', '')
        query = query.replace('三点水', '氵')
        query = query.replace('单人旁', '亻')
        query = query.replace('艹字头', '艹')
        query = query.replace('草字头', '艹')
        query = query.replace('立字旁', '立')
        query = query.replace('提手旁', '扌')
        query = query.replace('提手', '扌')
        query = query.replace('耳朵旁', '阝')
        query = query.replace('耳刀', '阝')
        query = query.replace('双人旁', '彳')
        query = query.replace('绞丝旁', '纟')
        query = query.replace('言字旁', '讠')
        query = query.replace('竖心旁', '忄')
        query = query.replace('树心', '忄')
        query = query.replace('金字旁', '钅')
        query = query.replace('女字旁', '女')
        query = query.replace('竹字头', '竹')
        query = query.replace('木字旁', '木')
        query = query.replace('土字旁', '土')
        query = query.replace('提土旁', '土')
        query = query.replace('火字旁', '火')
        query = query.replace('口字旁', '口')
        query = query.replace('日字旁', '日')
        query = query.replace('四点水', '灬')
        query = query.replace('四点底', '灬')
                
        query = query.replace('一点', '丶')
        query = query.replace('一横', '一')
        query = query.replace('两横', '二')
        query = query.replace('一竖', '丨')
        query = query.replace('一撇', '丿')
        query = query.replace('一丿', '丿')
        query = query.replace('两点', '冫')
        query = query.replace('三点', '氵')
        query = query.replace('点', '丶')
        query = query.replace('竖', '丨')
        query = query.replace('的繁体', '')
        query = query.replace('合起来', '')
        query = query.replace('组成的', '')
        query = query.replace('中间', '')
        query = query.replace('撇', '丿')
        query = query.replace('字', '')
        query = query.replace('上边', '')
        query = query.replace('下边', '')
        query = query.replace('左边', '')
        query = query.replace('右边', '')

        if len(query) > 3 and ('去' not in query):
            query = query.replace('上', '')
            query = query.replace('下', '')
            query = query.replace('一', '')

        # 处理 "字到部件查询"
        begin = query.find('去掉')
        if (begin != -1 and len(query) > begin + 2):
            if(begin == 4):
                if (query[2] == '的'):
                    query = query[3] + '|' + query[begin+2:]
            else:
                query = query[:begin] + '|' + query[begin+2:]
        begin = query.find('少个')
        if (begin != -1 and len(query) > begin + 2):
            if(begin == 4):
                if (query[2] == '的'):
                    query = query[3] + '|' + query[begin+2:]
            else:
                query = query[:begin] + '|' + query[begin+2:]
        begin = query.find('少')
        if (begin != -1 and len(query) > begin + 1):
            if(begin == 4):
                if (query[2] == '的'):
                    query = query[3] + '|' + query[begin+1:]
            else:
                query = query[:begin] + '|' + query[begin+1:]

        if (query not in map_chaizi):      
            # 处理 "数量"
            begin = query.find('两个')
            if (begin != -1 and len(query) > begin + 2):
                query = query[:begin] + query[begin+2] + query[begin+2:]
            begin = query.find('俩个')
            if (begin != -1) and len(query) > begin + 2:
                query = query[:begin] + query[begin+2] + query[begin+2:]
            begin = query.find('2个')
            if (begin != -1) and len(query) > begin + 2:
                query = query[:begin] + query[begin+2] + query[begin+2:]
            begin = query.find('二个')
            if (begin != -1) and len(query) > begin + 2:
                query = query[:begin] + query[begin+2] + query[begin+2:]
            begin = query.find('多两')
            if (begin != -1 and len(query) > begin + 2):
                query = query[:begin] + query[begin+2] + query[begin+2:]
            begin = query.find('两')
            if (begin != -1 and len(query) > begin + 1):
                query = query[:begin] + query[begin+1] + query[begin+1:]
            begin = query.find('三个')
            if (begin != -1) and len(query) > begin + 2:
                query = query[:begin] + query[begin+2] * 2 + query[begin+2:]
            begin = query.find('3个')
            if (begin != -1) and len(query) > begin + 2:
                query = query[:begin] + query[begin+2] * 2 + query[begin+2:]
            begin = query.find('三')
            if (begin != -1 and len(query) > begin + 1):
                query = query[:begin] + query[begin+1] * 2 + query[begin+1:]
            begin = query.find('四个')
            if (begin != -1) and len(query) > begin + 2:
                query = query[:begin] + query[begin+2] * 3 + query[begin+2:]
            begin = query.find('4个')
            if (begin != -1) and len(query) > begin + 2:
                query = query[:begin] + query[begin+2] * 3 + query[begin+2:]
            begin = query.find('四')
            if (begin != -1 and len(query) > begin + 1):
                query = query[:begin] + query[begin+1] * 3 + query[begin+1:]
        
        if ('|' in query):
            q_han = query.split('|')[0]
            q_rad = query.split('|')[1]
            if (q_han in map_han):
                for rads in map_han[q_han]:
                    if len(rads) == 2:
                        if (rads[0] == q_rad):
                            han = rads[1]
                        if (rads[1] == q_rad):
                            han = rads[0]
        else:
            if (query not in map_chaizi):
                if items[0] in map_chaizi:
                    query = items[0]

            if (query in map_chaizi):
                han = map_chaizi[query][0]

        if len(han) > 0:
            f_o.write('{}\t{}\t{}\t{}\n'.format(items[0], han, query, freq)) 
        else:
            f_l.write('{}\t{}\n'.format(each, query)) 

    f.close()
    f_o.close()
    f_l.close()

def sort_chaizi(chaizi_filename, word_filename, log_filename):
    map_word_freq = {}
    map_word_total = {}
    f = open(chaizi_filename, 'r', encoding='utf-8')
    for each in f:
        items = each.strip().split()
        if len (items) == 4:
            w = items[1]
            f = int(items[3])
            if (w not in map_word_total):
                map_word_total[w] = set()
            map_word_total[w].add(items[0])
            map_word_freq[w] = map_word_freq.get(w, 0) + f
    
    lst_word = sorted(map_word_freq.items(), key = lambda x: x[1], reverse = True)

    print('write', word_filename)
    f = open(word_filename, 'w', encoding='utf-8')
    t_w = 0
    t_q = 0
    for each in lst_word:
        s = '{}\t{}'.format(each[0], each[1])
        f.write('{}\n'.format(s))
        t_q += len(map_word_total[each[0]])
        t_w += 1
    f.close()

    print('write', log_filename)
    f = open(log_filename, 'w', encoding='utf-8')
    f.write('# 查询数量/汉字数量 = {} {}/{}\n'.format(t_q / t_w, t_q, t_w))
    for each in lst_word:
        idx = 0
        for q in map_word_total[each[0]]:
            idx += 1
            s = '{}\t{}\t{}'.format(idx, each[0], q)
            f.write('{}\n'.format(s))
    f.close()



def load_han_level(filename):
    f = open(filename, 'r', encoding='utf-8')
    s = ''
    for each in f:
        s += each
    f.close()
    return set(s)

def check_level(info_path, word_file, word_level_file):
    level1 = load_han_level(os.path.join(info_path, 'level1.txt'))
    level2 = load_han_level(os.path.join(info_path, 'level2.txt'))
    level3 = load_han_level(os.path.join(info_path, 'level3.txt'))
    l1_total = 0
    l2_total = 0
    l3_total = 0
    l4_total = 0
    f = open(word_file, 'r', encoding='utf-8')
    for each in f:
        items = each.strip().split()
        if len (items) == 2:
            w = items[0]
            freq = int(items[1])
            if (freq == 0):
                break
            if w in level1:
                l1_total += 1
            elif w in level2:
                l2_total += 1
            elif w in level3:
                l3_total += 1
            else:
                l4_total += 1
    l_total = l1_total + l2_total + l3_total + l4_total
    f.close()
    print('write', word_level_file)
    f = open(word_level_file, 'w', encoding='utf-8')
    f.write('level1={:.2%} {}/{}\n'.format(l1_total/l_total, l1_total, l_total))
    f.write('level2={:.2%} {}/{}\n'.format(l2_total/l_total, l2_total, l_total))
    f.write('level3={:.2%} {}/{}\n'.format(l3_total/l_total, l3_total, l_total))
    f.write('others={:.2%} {}/{}\n'.format(l4_total/l_total, l4_total, l_total))
    f.close()

def top_100(stat_file, out_file, max_num = 100):
    f = open(stat_file, 'r', encoding='utf-8')
    lst = ['这', '字']
    set_top = set()
    out_total = 0
    print('write', out_file)
    f_o = open(out_file, 'w', encoding='utf-8')
    for each in f:
        each = each.strip()
        items = each.split()
        han = items[0]
        freq = int(items[1])
        if han in lst:
            continue
        if (freq == 0):
            break
        out_total += 1
        if (out_total % 5 == 1):
            f_o.write('{}\t{}'.format(han, freq))
        else:
            f_o.write('\t{}\t{}'.format(han, freq))
        set_top.add(han)
        if (out_total % 5 == 0):
            f_o.write('\n')
        if (out_total >= max_num):
            break
    if (out_total % 5 != 0):
        f_o.write('\n')
    f.close()
    f_o.close()

    return set_top
    
def stat_chaizi_day_freq(query_file, day_file, out_file):
    map_query_han = {}
    map_han_day = {}
    f = open(query_file, 'r', encoding='utf-8')
    for each in f:
        if each[0] == '#':
            continue
        items = each.strip().split()
        if len (items) == 3:
            h = items[1]
            q = items[2]
            map_query_han[q] = h
    f.close()

    f = open(day_file, 'r', encoding='utf-8')
    for each in f:
        each = each.strip()
        if each[0] == '#':
            continue
        items = each.strip().split()
        if len (items) == 3:
            q = items[0]
            d = items[1]
            freq = int(items[2])
            if q in map_query_han:
                h = map_query_han[q]
                if h not in map_han_day:
                    map_han_day[h] = {}
                map_han_day[h][d] = map_han_day[h].get(d, 0) + freq
    f.close()
    
    print('write', out_file)
    f = open(out_file, 'w', encoding='utf-8')
    for h in map_han_day:
        l_day =  sorted(map_han_day[h])
        for d in l_day:
            s = '{}\t{}\t{}'.format(h, d, map_han_day[h][d])
            f.write('{}\n'.format(s))
    f.close()

def single_chaizi_compare(info_path, single_top, chaizi_top, comp_file):
    level1 = load_han_level(os.path.join(info_path, 'level1.txt'))
    level2 = load_han_level(os.path.join(info_path, 'level2.txt'))
    level3 = load_han_level(os.path.join(info_path, 'level3.txt'))
    level_all = level1 | level2 | level3

    print('write', comp_file)
    f = open(comp_file, 'w', encoding='utf-8')
    f.write('single&chaizi={}\n'.format(single_top.intersection(chaizi_top)))

    f.write('single&level1={}\n'.format(single_top.intersection(level1)))
    f.write('single&level2={}\n'.format(single_top.intersection(level2)))
    f.write('single&level3={}\n'.format(single_top.intersection(level3)))
    f.write('single&out={}\n'.format(single_top - level_all))

    f.write('chaizi&level1={}\n'.format(chaizi_top.intersection(level1)))
    f.write('chaizi&level2={}\n'.format(chaizi_top.intersection(level2)))
    f.write('chaizi&level3={}\n'.format(chaizi_top.intersection(level3)))
    f.write('chaizi&out={}\n'.format(chaizi_top - level_all))
    
    f.close()

def rare_stat(data_path, info_path, prefix_list, out_path):
    if not os.path.isdir(out_path):
        os.path.mkdirs(out_path)
    stat_single_match(data_path, prefix_list, os.path.join(out_path, 'result_single_word.txt'), os.path.join(out_path, 'query_single_all.txt'))
    stat_chaizi_match(data_path, prefix_list, os.path.join(out_path, 'query_chaizi_freq.txt'), os.path.join(out_path, 'query_chaizi_all.txt'))
    make_chaizi_data([os.path.join(info_path, 'chaizi-gbk.txt'), os.path.join(info_path, 'chaizi-gbk.csv')], os.path.join(out_path, 'query_chaizi_freq.txt'), os.path.join(out_path, 'result_chaizi_freq.txt'), os.path.join(out_path, 'result_chaizi_freq.log'))
    sort_chaizi(os.path.join(out_path, 'result_chaizi_freq.txt'), os.path.join(out_path, 'result_chaizi_word.txt'), os.path.join(out_path, 'result_chaizi_query.txt'))
    check_level(info_path, os.path.join(out_path, 'result_chaizi_word.txt'), os.path.join(out_path, 'result_chaizi_word_level.txt'))
    check_level(info_path, os.path.join(out_path, 'result_single_word.txt'), os.path.join(out_path, 'result_single_word_level.txt'))
    stat_chaizi_day_freq(os.path.join(out_path, 'result_chaizi_query.txt'), os.path.join(out_path, 'query_chaizi_all.txt'), os.path.join(out_path, 'query_chaizi_day_freq.txt'))

    single_top = top_100(os.path.join(out_path, 'result_single_word.txt'), os.path.join(out_path, 'result_single_word_top100.txt'))
    chaizi_top = top_100(os.path.join(out_path, 'result_chaizi_word.txt'), os.path.join(out_path, 'result_chaizi_word_top100.txt'))
    single_chaizi_compare(info_path, single_top, chaizi_top, os.path.join(out_path, 'result_single_chaizi_compare.txt'))

    
rare_stat('./data', './info', ['字读什么', '字念什么', '是什么字', '念什么字', '念什么', '读什么'], './output')
