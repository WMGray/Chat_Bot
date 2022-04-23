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
    if os.path.exists(Post_name) and os.path.exists(Response_name) and os.path.exists(Response_emo_name):
        print('文件已存在，跳过处理')
        return
    # 读取数据
    data = codecs.open(data_name, encoding=encoding, errors='replace')
    Post = codecs.open(Post_name, 'a', encoding=encoding)
    Response = codecs.open(Response_name, 'a', encoding=encoding)
    Response_emo = codecs.open(Response_emo_name, 'a', encoding=encoding)

    data_list = json.load(data)
    for conversation in data_list:
        post, response = conversation[0], conversation[1]  # 取出每一个对话

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
    if os.path.exists(Post_name) and os.path.exists(Response_name) and os.path.exists(Response_emo_name):
        print('文件已存在，跳过处理')
        return
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
        print('情感词典已存在，加载词典')
        emo_dict = json.load(open(Emo_dict_path, 'r'))
        return emo_dict
    else:
        print('创建情感词典')
        emo_dict = {'positive': [], 'negative': []}
        for file in os.listdir(Hownet_path):
            if file.startswith('正面'):  # 正面情感词典
                try:
                    with codecs.open(Hownet_path + file, 'r', encoding='utf-8') as f:
                        data = f.readlines()[2:]
                except:
                    with codecs.open(Hownet_path + file, 'r', encoding='gbk') as f:
                        data = f.readlines()[2:]
                emo_dict['positive'] += [line.strip() for line in data]
                f.close()
                print('正面情感词典读取完毕')
            else:  # 负面情感词典
                try:
                    with codecs.open(Hownet_path + file, 'r', encoding='utf-8') as f:
                        data = f.readlines()[2:]
                except:
                    with codecs.open(Hownet_path + file, 'r', encoding='gbk') as f:
                        data = f.readlines()[2:]
                emo_dict['negative'] += [line.strip() for line in data]
                f.close()
                print('负面情感词典读取完毕')

        emo_dict['positive'] = list(set(emo_dict['positive']))
        emo_dict['negative'] = list(set(emo_dict['negative']))
        # 写入文件
        json.dump(emo_dict, open(Emo_dict_path, 'w', encoding='utf-8'))
        print('情感词典写入完毕')

        return emo_dict


def mark_emo(Response_path, Choice_path, emo_dict, encoding):
    """标记情感词"""
    if os.path.exists(Choice_path):  # 如果存在，则不进行标记
        print('已标记，跳过')
        return
    # 打开文件
    Response = codecs.open(Response_path, 'r', encoding=encoding)
    Choice = codecs.open(Choice_path, 'w', encoding=encoding)

    for index, line in enumerate(Response):
        words = line.strip().split()
        emo = []
        for word in words:
            if word in emo_dict['positive']:
                emo.append(1)
            elif word in emo_dict['negative']:
                emo.append(-1)
            else:
                emo.append(0)
        Choice.write(' '.join([str(emo[i]) for i in range(len(emo))]) + '\n')


    # 关闭文件
    Response.close()
    Choice.close()


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
    train_Post_path = config["train_Post_file"]
    train_Response_path = config["train_Response_file"]
    train_Choice_path = config["train_Choice_file"]
    train_Emo_path = config["train_Emo_file"]

    # 开发集
    dev_Post_path = config["dev_Post_file"]
    dev_Response_path = config["dev_Response_file"]
    dev_Choice_path = config["dev_Choice_file"]
    dev_Emo_path = config["dev_Emo_file"]

    # 编码方式
    encoding = config["encoding"]

    # 知网Hownet情感词典
    Emotion_words_path = config["emo_words_file_path"]
    Emotion_dict_file = config["Emotion_Dict_file"]

    print("开始处理ecg_train_data.json")
    process_train(train_data_path, train_Post_path, train_Response_path, train_Emo_path, encoding)
    print("开始处理ecg_test_data.xlsx")
    process_test(test_data_path, dev_Post_path, dev_Response_path, dev_Emo_path, encoding)
    print("处理数据集完成")

    print("构造情感词典")
    emo_dict = create_emo_dict(Emotion_words_path, Emotion_dict_file)
    print("构造情感词典完毕,共加载正向词{}个，负向词{}个".format(len(emo_dict['positive']), len(emo_dict['negative'])))

    print("开始标记情感词（Choice文件）")
    print("开始处理train_Response.tsv")
    mark_emo(train_Response_path, train_Choice_path, emo_dict, encoding)
    print("开始处理dev_Response.tsv")
    mark_emo(dev_Response_path, dev_Choice_path, emo_dict, encoding)
    print("标记情感词完毕")


if __name__ == "__main__":
    process()
