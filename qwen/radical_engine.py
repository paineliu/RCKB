import os 
import json
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  #（保证程序cuda序号与实际cuda序号对应）
os.environ['CUDA_VISIBLE_DEVICES'] = "2"  #（代表仅使用第0，1号GPU）

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

class RareKnowledge():
    def __init__(self, filename):
        f = open(filename, encoding='utf_8')
        self.j_data = json.load(f)
        self.map_rad_han = {}
        for item in self.j_data:
            r = self.j_data[item]['radical'][0]
            self.map_rad_han[r] = item
    
    def get_han(self, radicals):
        if radicals in self.map_rad_han:
            return self.map_rad_han[radicals]
        return ''
    
    def get_pinyin(self, han):
        return self.j_data[han]['pinyin']
    
class RadicalEngine():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("qwen-7b-finetune", trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained("qwen-7b-finetune", device_map="auto",trust_remote_code=True).eval()
        self.rk = RareKnowledge('../knowledge/result_chaizi_knowledge.json')

    def getRadical(self, request):

        message = request['text']
        response, history = self.model.chat(self.tokenizer, "请将下文解析成汉字部件列表：\n{}".format(message), history=None)
        han = self.rk.get_han(response)
        respond = {}
        respond['code'] = 200
        respond['message'] = 'ok'
        respond['data'] = {'radicals': response, 'han': han, 'pinyin':self.rk.get_pinyin(han)}

        return respond
    
def get_info(rk, text):
    han = rk.get_han(text)
    print(han)
    print(rk.get_pinyin(han))
    
if __name__ == "__main__":
    rk = RareKnowledge('../knowledge/result_chaizi_knowledge.json')
    get_info(rk, '火火火火')
    get_info(rk, '火火火')
    