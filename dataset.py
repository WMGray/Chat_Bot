# 数据集处理

import os
import json
import codecs
from config import Config
import pandas as pd
import re


def regular(line):
    """句子规范化"""
    line = re.sub(r'…{1,100}', '…', line)
    line = re.sub(r'\.{3,100}', '…', line)
    line = re.sub(r'···{2,100}', '…', line)
    line = re.sub(r'\.{1,100}', '。', line)
    line = re.sub(r'。{1,100}', '。', line)
    line = re.sub(r'？{1,100}', '？', line)
    line = re.sub(r'!{1,100}', '！', line)
    line = re.sub(r'！{1,100}', '！', line)
    line = re.sub(r'~{1,100}', '～', line)
    line = re.sub(r'～{1,100}', '～', line)

    return line

def process_train(data_name, Post_name, Response_name, Response_emo_name):
    """处理ecg_train_data.json"""
    # 读取数据
    data = codecs.open(data_name, encoding=Config.encoding, errors='replace')
    Post = codecs.open(Post_name, 'a', encoding=Config.encoding)
    Response = codecs.open(Response_name, 'a', encoding=Config.encoding)
    Response_emo = codecs.open(Response_emo_name, 'a', encoding=Config.encoding)

    data_list = json.load(data)
    for conversation in data_list:
        post, response = conversation[0], conversation[1]   # 取出每一个对话

        post_sentence = post[0].replace('\n', '').replace(' ', '').strip()
        post_emo = post[1]
        response_sentence = response[0].replace('\n', '').replace(' ', '').strip()
        response_emo = response[1]

        # 句子规范化
        post_sentence = regular(post_sentence)
        response_sentence = regular(response_sentence)

        # 写入文件
        Post.write(post_sentence + '\n')
        Response.write(response_sentence + '\n')

        Response_emo.write(str(response_emo) + '\n')

    data.close()
    Post.close()
    Response.close()


def process_test(data_name, Post_name, Response_name, Response_emo_name):
    """处理ecg_test_data.xlsx"""
    # 读取数据
    data = pd.read_excel(data_name)
    Post = codecs.open(Post_name, 'a', encoding=Config.encoding)
    Response = codecs.open(Response_name, 'a', encoding=Config.encoding)
    Response_emo = codecs.open(Response_emo_name, 'a', encoding=Config.encoding)

    # 其他（Null)，喜好(Like)，悲伤(Sad)，厌恶(Disgust)，愤怒(Anger)，高兴（Happiness
    emo_dict = {'null': 0, 'like': 1, 'sad': 2, 'disgust': 3, 'angry': 4, 'happy': 5}
    post, response, response_emo, scores = data['post'], data['response'], data['emotion'], data['score']

    for index in range(0, len(scores)):
        if scores[index] == 2:
            # print(post[index], response[index], response_emo[index], emo_dict[response_emo[index]])
            # 句子规范化
            post_sentence = regular(post[index])
            response_sentence = regular(response[index])

            Post.write(post[index] + '\n')
            Response.write(response[index] + '\n')
            Response_emo.write(str(emo_dict[response_emo[index]]) + '\n')

    Post.close()
    Response.close()
    Response_emo.close()


def process():
    """处理数据集"""
    print("开始处理数据集")

    train_data_path = Config.train_path
    test_data_path = Config.test_path
    Post_name = Config.Post_path
    Response_name = Config.Response_path
    Response_emo_name = Config.Response_emo_path

    print("开始处理ecg_train_data.json")
    process_train(train_data_path, Post_name, Response_name, Response_emo_name)

    print("开始处理ecg_test_data.xlsx")
    process_test(test_data_path, Post_name, Response_name, Response_emo_name)

    print("处理数据集完成")


if __name__ == "__main__":
    process()