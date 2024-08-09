import os
import json

def make_train_dataset(desc_filename, train_pathname):
    
    print(desc_filename)
    
    os.makedirs(train_pathname, exist_ok=True)

    f = open(desc_filename, encoding="utf-8")

    train_data = []
    test_data = []
    val_data = []
    line_total = 0
    
    for each in f:
        item = each.strip().split()
        query = item[0]
        hanzi = item[1]
        radicals = item[2]

        data ={
            "id": "identity_radical_{}".format(line_total),
            "conversations": [
                {
                    "from": "user",
                    "value": "{}{}".format("请将下文解析成汉字部件列表：\n", query)
                },
                {
                    "from": "assistant",
                    "value": "{}".format(radicals)
                }
            ]
        }
                
        if (line_total % 10) < 8:
            train_data.append(data)
         
        elif (line_total % 10) < 9:
            test_data.append(data)
        else:
            val_data.append(data)
            
        line_total += 1    

    f = open(os.path.join(train_pathname, "radical_train.json"), 'w', encoding='utf-8')
    json.dump(train_data, f, ensure_ascii=False, indent=4)
    f.close()

    f = open(os.path.join(train_pathname, "radical_test.json"), 'w', encoding='utf-8')
    json.dump(test_data, f, ensure_ascii=False, indent=4)
    f.close()

    f = open(os.path.join(train_pathname, "radical_dev.json"), 'w', encoding='utf-8')
    json.dump(val_data, f, ensure_ascii=False, indent=4)
    f.close()

if __name__ == '__main__':
    make_train_dataset('./output/result_chaizi_freq.txt', './radical_qwen')
