import codecs
import os

from config import Config
from util import *


def prepocess(raw_corpus_file_name, result_file_name):
    start_end_symbol = "E"
    utterance_symbol = "M"

    raw_corpus_file = codecs.open(raw_corpus_file_name, encoding=Config.encoding, errors="replace")  # 打开文件
    result_file = codecs.open(result_file_name, "w", encoding=Config.encoding)  # 打开文件

    single_session = []   # 用于存放单个对话
    session_lengths = []

    for index, line in enumerate(raw_corpus_file):  # 遍历每一行
        if index % 100000 == 0:
            print(raw_corpus_file_name, index)

        if line.startswith(start_end_symbol): # 空行标记
            if len(single_session) == 2:  # 凑齐一对对话
                pairs = generate_single_pairs_from_multi_turn(single_session)
                for pair in pairs:
                    result_file.write("\t".join(pair) + "\n")
                session_lengths.append(len(single_session))
            single_session = []  # 清空
        elif line.startswith(utterance_symbol): # 对话标记
            line = line[1:].strip() # 去掉第一个字符和开头、结尾空格
            utterance = line.strip()
            single_session.append(utterance) 

    print("avg session length", sum(session_lengths) / len(session_lengths))  # 输出平均对话长度
    raw_corpus_file.close()
    result_file.close()


def xiaohuangji_process_pipeline():
    print("xiaohuangji_process_pipeline")
    raw_corpus_file_name = Config.raw_xiaohuangji_corpus_path
    result_file_name = os.path.join(Config.clean_chat_corpus_root, "xiaohuangji.tsv")

    prepocess(raw_corpus_file_name, result_file_name)
    format_refine(result_file_name)
