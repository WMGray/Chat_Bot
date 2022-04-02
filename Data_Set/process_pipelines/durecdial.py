import codecs
import os
import re

from config import Config
from util import *

def process(raw_corpus_file_name, result_file_name):
    """处理数据，将原始数据转换为tsv格式"""
    raw_corpus_file = codecs.open(raw_corpus_file_name, encoding=Config.encoding, errors='replace')
    result_file_name = codecs.open(result_file_name, 'a', encoding=Config.encoding)  # 追加模式(多个文件合为一个文件)

    # 开始统一格式
    start_symbol = '"conversation": ['
    for index, line in enumerate(raw_corpus_file):
        if index % 10000 == 0:
            print(raw_corpus_file_name, index)
        if start_symbol in line:  # 如果改行中含有对话，则开始处理
            # 先提取所有对话
            start_pos = line.index(start_symbol)+len(start_symbol)  # 对话开始的位置

            conversations = re.sub(r'\[[1234567890]\]', '', line[start_pos:-3]).replace(' ', '')  # 去掉空格、[数字]
            # conversations = line[start_pos:-3].replace('"', '').replace(' ', '').split("' ")

            conversations = conversations.split('","')  # 将每个对话分割开
            for QA in range(0, len(conversations)-1):
                print(conversations[QA])
                result_file_name.write(conversations[QA].strip('"') + '\t' + conversations[QA+1].strip('"') + '\n')




def durecdial_process_pipeline():
    print("duecdial_process_pipeline")
    raw_root = Config.raw_DuRecDial_corpus_root
    result_file_name = os.path.join(Config.clean_chat_corpus_root, "durecdial.tsv")

    if os.path.exists(result_file_name):  # 如果已经处理过，就不用再处理了
        os.remove(result_file_name)
    
    for file_name in os.listdir(raw_root):
      raw_corpus_file_name = os.path.join(raw_root, file_name)  # 获取每一个文件的位置
      process(raw_corpus_file_name, result_file_name)  # 处理每一个文件

    format_refine(result_file_name) # 格式化数据



