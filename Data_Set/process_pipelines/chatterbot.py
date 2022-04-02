import codecs
import os

from config import Config
from util import *


def prepocess(raw_corpus_file_name, result_file_name):
    post_symbol = "- -"
    response_symbol = "  -"

    raw_corpus_file = codecs.open(raw_corpus_file_name, encoding=Config.encoding, errors="replace")
    result_file = codecs.open(result_file_name, "a", encoding=Config.encoding)

    post = None

    for index, line in enumerate(raw_corpus_file):
        if index % 100000 == 0:  # 每100000行输出一次
            print(raw_corpus_file_name, index) 
        # 忽略对话类别
        if line.startswith(post_symbol):         # 如果是Question
            post = line.lstrip(post_symbol).strip()              # 去掉前面的" - -"和左右空格
        elif line.startswith(response_symbol):   # 如果是Answer
            if post:
                response = line.lstrip(response_symbol).strip()  # 去掉前面的"  -"和左右空格
                result_file.write(post + "\t" + response + "\n")

    raw_corpus_file.close()
    result_file.close()


def chatterbot_process_pipeline():
    print("chatterbot_process_pipeline")

    raw_root = Config.raw_chatterbot_corpus_root
    result_file_name = os.path.join(Config.clean_chat_corpus_root, "chatterbot.tsv")
    if os.path.exists(result_file_name):  # 如果已经处理过，就不用再处理了
        os.remove(result_file_name)
    for file_name in os.listdir(raw_root):
        raw_corpus_file_name = os.path.join(raw_root, file_name)
        prepocess(raw_corpus_file_name, result_file_name)

    format_refine(result_file_name)
