import os 
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  #（保证程序cuda序号与实际cuda序号对应）
os.environ['CUDA_VISIBLE_DEVICES'] = "2"  #（代表仅使用第0，1号GPU）

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

tokenizer = AutoTokenizer.from_pretrained("qwen-7b-finetune", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained("qwen-7b-finetune", device_map="auto",

trust_remote_code=True).eval()

response, history = model.chat(tokenizer, "请将下文解析成汉字部件列表：\n两个木", history=None)
print(response)
