import os 
import json
import time

def test_acc(test_filename, text, result_filename, phrase_filename):
    f_result = open(result_filename, 'w', encoding='utf-8-sig')
    f_result.write(f'汉字, 年份, 词频, 词种\n')
    f = open(test_filename, encoding='utf-8')
    map_han_phrase = {}
    for each in f:
        items = each.split(';')
        if len(items) == 3:
            han = items[0].strip()
            if han in text:
                year = items[1].strip()
                data = items[2].strip().replace("'", '"')
                json_data = json.loads(data)
                for phrase in json_data['ci_info']:
                    if han not in map_han_phrase:
                        map_han_phrase[han] = {}
                    map_han_phrase[han][phrase] = json_data['ci_info'][phrase] + map_han_phrase[han].get(phrase, 0)

                f_result.write(f'{han}, {year}, {json_data["zi_freq"]}, {json_data["zi_2_ci_type"]}\n')

    for han in map_han_phrase:
        #删除频率小于2的词
        map_han_phrase[han] = {k: v for k, v in map_han_phrase[han].items() if v >= 2}
        # 删除包含字符“△”的词
        map_han_phrase[han] = {k: v for k, v in map_han_phrase[han].items() if '△' not in k}
        # 分行按照频率由高到低打印map_phrase内容
        f_phrase = open(phrase_filename[:-3] + han + '.csv', 'w', encoding='utf-8-sig')
        f_phrase.write(f'词语, 词频\n')
        for phrase, freq in sorted(map_han_phrase[han].items(), key=lambda x: x[1], reverse=True):
            f_phrase.write(f"{phrase}, {freq}\n")

if __name__ == "__main__":
    test_acc('./output/single_word_coll_info.txt', ['昶', '鑫'], './output/single_word_freq.csv', './output/single_word_phrase.csv')
