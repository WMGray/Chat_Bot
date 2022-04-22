# 数据集处理

import os
import json
import codecs
import yaml
import argparse
import pandas as pd
import re
import jieba
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary


def parse_args():
    """Data processing"""
    parser = argparse.ArgumentParser(description="Data processing")

    parser.add_argument('--config', nargs='?',
                        default='./configs/data.yaml',
                        help='Configuration file for model specifications')

    return parser.parse_args()


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

def process_train(data_name, Post_name, Response_name, Response_emo_name, encoding):
    """处理ecg_train_data.json"""
    # 读取数据
    data = codecs.open(data_name, encoding=encoding, errors='replace')
    Post = codecs.open(Post_name, 'a', encoding=encoding)
    Response = codecs.open(Response_name, 'a', encoding=encoding)
    Response_emo = codecs.open(Response_emo_name, 'a', encoding=encoding)

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

        # 分词
        post_sentence = ' '.join(jieba.cut(post_sentence))
        response_sentence = ' '.join(jieba.cut(response_sentence))

        # 写入文件
        Post.write(post_sentence + '\n')
        Response.write(response_sentence + '\n')

        Response_emo.write(str(response_emo) + '\n')

    data.close()
    Post.close()
    Response.close()


def process_test(data_name, Post_name, Response_name, Response_emo_name, encoding):
    """处理ecg_test_data.xlsx"""
    # 读取数据
    data = pd.read_excel(data_name)
    Post = codecs.open(Post_name, 'a', encoding=encoding)
    Response = codecs.open(Response_name, 'a', encoding=encoding)
    Response_emo = codecs.open(Response_emo_name, 'a', encoding=encoding)

    # 其他（Null)，喜好(Like)，悲伤(Sad)，厌恶(Disgust)，愤怒(Anger)，高兴（Happiness
    emo_dict = {'null': 0, 'like': 1, 'sad': 2, 'disgust': 3, 'angry': 4, 'happy': 5}
    post, response, response_emo, scores = data['post'], data['response'], data['emotion'], data['score']

    for index in range(0, len(scores)):
        if scores[index] == 2:
            # print(post[index], response[index], response_emo[index], emo_dict[response_emo[index]])
            # 句子规范化
            post_sentence = regular(post[index])
            response_sentence = regular(response[index])

            # 分词
            post_list = jieba.lcut(post_sentence)
            response_list = jieba.lcut(response_sentence)

            Post.write(' '.join(post_list) + '\n')
            Response.write(' '.join(response_list) + '\n')
            Response_emo.write(str(emo_dict[response_emo[index]]) + '\n')

    Post.close()
    Response.close()
    Response_emo.close()


def create_emo_dict(Hownet_path, Emo_dict_path):
    """创建情感词典"""
    if os.path.exists(Emo_dict_path):  # 如果存在，则直接读取
        emo_dict = json.load(open(Emo_dict_path, 'r'))
        return emo_dict
    else:
        emo_dict = {'positive': [], 'negative': []}
        for file in os.listdir(Hownet_path):
            if file.startswith('正面'):   # 正面情感词典
                f = codecs.open(Hownet_path + file, encoding='GBK')
                data = f.readlines()[2:]
                emo_dict['positive'] += [line.strip() for line in data]
                f.close()
                print('正面情感词典读取完毕')
            else:   # 负面情感词典
                f = codecs.open(Hownet_path + file, encoding='GBK')
                data = f.readlines()[2:]
                emo_dict['negative'] += [line.strip() for line in data]
                f.close()
                print('负面情感词典读取完毕')

        # 写入文件
        json.dump(emo_dict, open(Emo_dict_path, 'w'))




def process():
    """处理数据集"""
    print("开始处理数据集")

    # 读取配置文件
    args = parse_args()
    with open(args.config) as f:
        config = yaml.safe_load(f)["configuration"]

    train_data_path = config["train_data_path"]
    test_data_path = config["test_data_path"]

    # 训练集
    Post_train_path = config["Post_train_file"]
    Response_train_path = config["Response_train_file"]
    Emo_train_path = config["Emo_train_file"]

    # 开发集
    Post_test_path = config["Post_test_file"]
    Response_test_path = config["Response_test_file"]
    Emo_test_path = config["Emo_test_file"]

    # 编码方式
    encoding = config["encoding"]

    # 知网Hownet情感词典
    Hownet_path = config["Hownet_file_path"]
    Emotion_dict_file = config["Emotion_Dict_file"]

    print("创建情感词典：")
    create_emo_dict(Hownet_path, Emotion_dict_file)

    """print("开始处理ecg_train_data.json")
    process_train(train_data_path, Post_train_path, Response_train_path, Emo_train_path, encoding)

    print("开始处理ecg_test_data.xlsx")
    process_test(test_data_path, Post_test_path, Response_test_path, Emo_test_path, encoding)

    print("处理数据集完成")"""


if __name__ == "__main__":
    process()
