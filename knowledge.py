from collections import defaultdict
import json
import os


def make_chaizi_knowledge(info_pathname, chaizi_filename, phrase_filename, knowledge_filename):
    map_han_pinyin = {}
    f_pinyin = open(os.path.join(info_pathname, 'pinyin.txt'), encoding='utf-8')
    for each in f_pinyin:
        items = each.strip().split()
        if len(items) == 4:
            map_han_pinyin[items[3]] = items[1]

    map_han_radical = {}
    
    f_chaizi = open(os.path.join(info_pathname, 'chaizi-utf8.txt'), encoding='utf-8')
    for each in f_chaizi:
        items = each.strip().split('\t')
        han = items[0]
        radical = items[1].replace(' ', '')
        map_han_radical[han] = [radical]

        # map_han_pinyin[items[3]] = map_han_pinyin[1]

    f_chaizi = open(os.path.join(info_pathname, 'chaizi-utf8.csv'), encoding='utf-8')
    for each in f_chaizi:
        items = each.strip().split(',')
        han = items[0]
        radicals = []
        radical1 = items[2].replace(' ', '')
        radical2 = items[3].replace(' ', '')
        radical3 = items[4].replace(' ', '')
        if len(radical1) > 0:
            radicals.append(radical1)
        if len(radical2) > 0:
            radicals.append(radical2)
        if len(radical3) > 0:
            radicals.append(radical3)
        if han not in map_han_radical:
            map_han_radical[han] = radicals

    map_han_level = {}
    for i in range(1, 4):
        f_level = open(os.path.join(info_pathname, 'level{}.txt'.format(i)), encoding='utf-8')
        data = f_level.read()
        for han in data:
            map_han_level[han] = i

    map_rare_han = {}
    map_radidal_han = {}

    f_chaizi = open(chaizi_filename, encoding='utf-8')
    for each in f_chaizi:
        items = each.strip().split()
        query = items[0]
        han = items[1]
        radical = items[2]
        freq = int(items[3])
        if han not in map_rare_han:
            map_rare_han[han] = {}
            map_rare_han[han]['freq'] = 0
            map_rare_han[han]['querys'] = []
            map_rare_han[han]['pinyin'] = map_han_pinyin[han]
            map_rare_han[han]['level'] = map_han_level.get(han, 4)
            map_rare_han[han]['radical'] = []
            map_rare_han[han]['phrases'] = {}
        
        map_rare_han[han]['freq'] += freq
        map_rare_han[han]['querys'].append(query)
        if radical not in map_rare_han[han]['radical']:
            map_rare_han[han]['radical'].append(radical)
        map_radidal_han[radical] = han

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 定义字母表
    
    f_phrase = open(phrase_filename, encoding='utf-8')
    for each in f_phrase:
        items = each.strip().split('\t')
        phrase = items[0]
        freq = int(items[1])
        valid = True
        for item in phrase:
            if item in alphabet:
                valid = False
                # print(phrase)
                break
        
        if valid:
            for item in ['多大', '身高', '资料','新闻','天气','地图', '邮编', '吧', '写真', '的', '诗词','演员','几岁', '试婚', '近况','背景', '违纪','记者', '近况', '小说','贴吧', '帖吧', '男排', '淘汰', "怎么", "拼音","读音","什么", "组词", "邮件","简介", "照片",'意思','博客','图片','微博','简历','官网', '直播','身价']:
                if item in phrase:
                    valid = False
                    break

        if valid:
            for han in phrase:
                if han in map_rare_han:
                    map_rare_han[han]['phrases'][phrase] = freq
    f = open(knowledge_filename, 'w', encoding='utf-8')
    json.dump(map_rare_han, f, ensure_ascii=False, indent=4)

def make_normal_knowledge(info_pathname, normal_filename, phrase_filename, knowledge_filename):
    map_han_pinyin = {}
    f_pinyin = open(os.path.join(info_pathname, 'pinyin.txt'), encoding='utf-8')
    for each in f_pinyin:
        items = each.strip().split()
        if len(items) == 4:
            map_han_pinyin[items[3]] = items[1]

    # map_han_radical = {}
    
    # f_normal = open(os.path.join(info_pathname, 'chaizi-utf8.txt'), encoding='utf-8')
    # for each in f_normal:
    #     items = each.strip().split('\t')
    #     han = items[0]
    #     radical = items[1].replace(' ', '')
    #     map_han_radical[han] = [radical]

    #     print(items)
    #     # map_han_pinyin[items[3]] = map_han_pinyin[1]

    # f_normal = open(os.path.join(info_pathname, 'chaizi-utf8.csv'), encoding='utf-8')
    # for each in f_normal:
    #     items = each.strip().split(',')
    #     han = items[0]
    #     radicals = []
    #     radical1 = items[2].replace(' ', '')
    #     radical2 = items[3].replace(' ', '')
    #     radical3 = items[4].replace(' ', '')
    #     if len(radical1) > 0:
    #         radicals.append(radical1)
    #     if len(radical2) > 0:
    #         radicals.append(radical2)
    #     if len(radical3) > 0:
    #         radicals.append(radical3)
    #     if han not in map_han_radical:
    #         map_han_radical[han] = radicals

    map_han_level = {}
    for i in range(1, 4):
        f_level = open(os.path.join(info_pathname, 'level{}.txt'.format(i)), encoding='utf-8')
        data = f_level.read()
        for han in data:
            map_han_level[han] = i

    map_rare_han = {}
    map_radidal_han = {}

    f_normal = open(normal_filename, encoding='utf-8')
    for each in f_normal:
        items = each.strip().split()
        han = items[0]
        freq = int(items[1])
        if han not in map_han_pinyin:
            continue
        if han not in map_rare_han:
            map_rare_han[han] = {}
            map_rare_han[han]['freq'] = 0
            map_rare_han[han]['pinyin'] = map_han_pinyin[han]
            map_rare_han[han]['level'] = map_han_level.get(han, 4)
            map_rare_han[han]['phrases'] = {}
        
        map_rare_han[han]['freq'] += freq

    f_phrase = open(phrase_filename, encoding='utf-8')
    for each in f_phrase:
        items = each.strip().split('\t')
        phrase = items[0]
        freq = int(items[1])
        for han in phrase:
            if han in map_rare_han:
                map_rare_han[han]['phrases'][phrase] = freq
    f = open(knowledge_filename, 'w', encoding='utf-8')
    json.dump(map_rare_han, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':    
    make_chaizi_knowledge('./info', './output/result_chaizi_freq.txt', './output/result_chaizi_phrase.txt', './output/result_chaizi_knowledge.json')
    make_normal_knowledge('./info', './output/result_single_word.txt', './output/result_chaizi_phrase.txt', './output/result_single_knowledge.json')
