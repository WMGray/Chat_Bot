# 一些配置
import os


class Config(object):
    """配置"""
    # 基本配置
    encoding = 'utf-8'

    # 数据集路径
    Data_path = "Data"

    train_path = os.path.join(Data_path, "ecg_train_data.json")
    test_path = os.path.join(Data_path, "ecg_test_data.xlsx")

    # 数据保存路径
    Post_path = os.path.join(Data_path, "Post.tsv")
    Response_path = os.path.join(Data_path, "Response.tsv")

    Response_emo_path = os.path.join(Data_path, "Response_emo.tsv")
