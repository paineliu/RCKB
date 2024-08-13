from collections import defaultdict
import math

import os

def make_phrase(corpus_pathname, word_filename, phrase_filename):

    f = open(word_filename, encoding='utf_8')
    g_words = {}
    g_phrase = defaultdict(float)

    for each in f:
        items = each.strip().split()
        g_words[items[0]] = int(items[1])
        
    paths = os.walk(corpus_pathname)
    file_total  = 0
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            full_name = os.path.join(path, file_name)
            print(full_name)
            f = open(full_name, encoding='utf_8')
            file_total += 1
            for each in f:
                each = each.rstrip()
                items = each.split('\t')
                if (int(items[1]) <= 5):
                    break
                for w in items[0]:
                    if w in g_words:
                        if len(items[0]) > 1 and len(items[0]) < 5:
                            freq = math.sqrt(int(items[1]))
                            g_phrase[items[0]] += freq
            
    g_list = sorted(g_phrase.items(), key = lambda x:x[1], reverse = True)
    total = 0
    f_out = open(phrase_filename, mode='w', encoding='utf-8')
    for each in g_list:
        total += 1
        freq = int(each[1] * each[1] / file_total)
        if (total == 1 or (total % 1000 == 0)):
            print(total, each[0], freq)
        f_out.write('{}\t{}\n'.format(each[0], freq))
    f_out.close()

    pass

if __name__ == '__main__':
    make_phrase('E:/data_utf8', './output/result_chaizi_word.txt', './output/result_chaizi_phrase.txt')