# 基于SeqSeq的情感聊天机器人

## 数据处理

### 数据集搜集

  1. [数据集来源](https://github.com/codemayq/chinese_chatbot_corpus)
     - [x] 聊天机器人
     - [ ] 豆瓣多轮
     - [ ] [PTT八卦语料](https://github.com/zake7749/Gossiping-Chinese-Corpus)
     - [x] 青云语料 
     - [ ] 电视剧对白语料
     - [x] 贴吧论坛回帖语料
     - [ ] 微博语料
     - [x] 小黄鸡语料  
  2. [百度DuRecDial](https://baidu-nlp.bj.bcebos.com/DuRecDial.zip)
     DuRecDial包含多种类型的对话(推荐对话、闲聊、任务导向对话和QA)，来自7个领域(电影、明星、音乐、新闻、食物、poi和天气)的10.2k对话，以及156K个utterances。
  3. [NLPCC 2018 Multi-Turn Human-Computer Conversations](http://tcci.ccf.org.cn/conference/2018/taskdata.php)
  4. [情感分类数据集](https://www.biendata.xyz/ccf_tcci2018/datasets/emotion/)
     NLPCC Emotion Classification Challenge（训练数据中17113条，测试数据中2242条）和微博数据筛选后人工标注(训练数据中23000条，测试数据中2500条)
### 语料清洗（正则化、切分、判断）
1.语料清洗
     - `聊天机器人`: 按行处理,原数据中`- -`为`Question`,`-`为`Answer`。去除标识和多余的空格，忽略数据集开头的对话类别，以`\t`分隔问答。数据集中包含多轮对话，需对Github数据集中的代码进行修改。
     - `青云语料`: 按行处理，原数据中一行为一个问答对，以`|`分隔。去除`|`符号，以`\t`分隔问答。
     - `贴吧论坛回帖语料`:按行处理，原数据中一行为一个问答对，以`  `分隔。去除`  `符号并以`\t`分隔问答。
     - `小黄鸡语料`:按行处理，原数据中`M`为对话行，`E`为分割行。去除标识和多余的空格，以`\t`分隔问答。
     - `百度DuRecDial`:多轮对话，每行以`solution`开头，以`conversation`为对话起始，可在每行中找出对话起始位置再进行清理。
        ![DuRecdial语料](./images/DuRecdial语料.png)
        先定位对话位置，截取对话，删除对话中多余的空格和`[数字]`，以`","`分隔字符串，在写入文件时，山区两边的`”`，并以`\t`分隔问答。
     - `情感分类数据集`:多轮对话，每轮对话以空行分隔。在写入文件时，删去两边的`”`，并以`\t`分隔问答。
  2. 对数据集进行分词整理，句子和标签保存在两个文件中
  3. 训练情感分类器  



# 参考文献

- [自然语言处理（NLP）的发展历程，神经语言模型多任务学习介绍， ECM模型介绍等](https://blog.csdn.net/Tefuir_zjw/article/details/102526023?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165016778816781685310307%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165016778816781685310307&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-3-102526023.142^v9^pc_search_result_control_group,157^v4^control&utm_term=ECM%E6%83%85%E6%84%9F&spm=1018.2226.3001.4187)
- 

> 中文： 孙茂松, 陈新雄, 张开旭, 郭志芃, 刘知远. THULAC：一个高效的中文词法分析工具包. 2016.
> https://github.com/thunlp/THULAC-Python
> Hao Zhou, Minlie Huang, Xiaoyan Zhu, Bing Liu. Emotional Chatting Machine: Emotional Conversation Generation with Internal and External Memory. AAAI 2018, New Orleans, Louisiana, USA.
> If you use our corpus, please cite: Yan Song, Shuming Shi, Jing Li, and Haisong Zhang. Directional Skip-Gram: Explicitly Distinguishing Left and Right Context for Word Embeddings. NAACL 2018 (Short Paper). [pdf] [bib]

>https://developer.aliyun.com/article/647550?spm=a2c6h.24874632.expert-profile.227.5b4aadc9oATARD
