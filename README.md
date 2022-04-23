# 基于SeqSeq的情感聊天机器人

## 文件介绍
- **configs**: 配置文件保存路径
  1. **data.yaml**: `dataset.py`配置文件
- **dataset.py**: 处理数据集
## 数据处理

### 数据集
[情感对话生成数据集](https://www.biendata.xyz/ccf_tcci2018/datasets/ecg/)

### 语料清洗（正则化、切分、判断）
1. 将对话分离成`Post`和`Response`，并进行`jieba`分词
2. `Response_emo.tsv`中保存了对话的情感标签,每个对话单独一行
3. 规范每一个句子,删去句子中多余的符号，如`!!!`改为`!`
4. 创建情感词典，词典来源为`知网Hownet情感词典`中的`正面情感词语(中文)`、`负面情感词语(中文)`和`BosonNLP情感词典`中的`正面情绪词`和`负面情绪词`
5. 对`train_Response.tsv`和`dev_Response.tsv`中的每一个词语进行情感标记，正向标记为`1`，负向标记为`-1`,不在情感词典中的标记为`0`,然后分别保存在 
   `train_Choice.tsv`和`dev_Choice.tsv`中


# 参考文献

- [自然语言处理（NLP）的发展历程，神经语言模型多任务学习介绍， ECM模型介绍等](https://blog.csdn.net/Tefuir_zjw/article/details/102526023?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165016778816781685310307%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165016778816781685310307&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-3-102526023.142^v9^pc_search_result_control_group,157^v4^control&utm_term=ECM%E6%83%85%E6%84%9F&spm=1018.2226.3001.4187)
- 

> 中文： 孙茂松, 陈新雄, 张开旭, 郭志芃, 刘知远. THULAC：一个高效的中文词法分析工具包. 2016.
> https://github.com/thunlp/THULAC-Python
> Hao Zhou, Minlie Huang, Xiaoyan Zhu, Bing Liu. Emotional Chatting Machine: Emotional Conversation Generation with Internal and External Memory. AAAI 2018, New Orleans, Louisiana, USA.
> If you use our corpus, please cite: Yan Song, Shuming Shi, Jing Li, and Haisong Zhang. Directional Skip-Gram: Explicitly Distinguishing Left and Right Context for Word Embeddings. NAACL 2018 (Short Paper). [pdf] [bib]

>https://developer.aliyun.com/article/647550?spm=a2c6h.24874632.expert-profile.227.5b4aadc9oATARD

# 问题及解决办法
1. from tensorflow.contrib.seq2seq import ...
   问题：ModuleNotFoundError: No module named ‘tensorflow.contrib’
   解决方法：from tensorflow_addons.seq2seq import ...
2. from tensorflow_addons.seq2seq import ...
   问题： cannot import name 'GreedyEmbeddingHelper' from 'tensorflow_addons.seq2seq'
   解决方法：修改为GreedyEmbeddingSampler
3. from tensorflow.contrib.rnn import LSTMStateTuple
   问题：No module named 'tensorflow.contrib'
   解决方法：from tensorflow.compat.v1.nn.rnn_cell import LSTMStateTuple
4. with tf.variable_scope('seq2seq_placeholder'):
   问题： module 'tensorflow' has no attribute 'variable_scope'
   解决方法：with tf.compat.v1.variable_scope('seq2seq_placeholder'):
5. tf.placeholder
   问题：module 'tensorflow' has no attribute 'placeholder'
   解决方法：tf.compat.v1.placeholder
6. self.encoder_inputs = tf.compat.v1.placeholder(tf.int32, [None, None], name="encoder_inputs")
   问题：tf.placeholder() is not compatible with eager execution.
   解决方法：在该行代码前添加 tf.compat.v1.disable_eager_execution()
7. initializer = tf.contrib.layers.xavier_initializer()
   问题：module 'tensorflow' has no attribute 'contrib'
   解决方法：