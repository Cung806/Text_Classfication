### 爬取携程景区评论，使用fasttext模型和LSTM模型对评论进行情感分类
**1. 爬取携程网上景区的评论信息，包括评论、得分、日期等信息。将得分80、100分的评论作为正类，20、40、60分的评论作为负类，构建情感分类训练集。**
**2. 使用fasttext模型对景区评论数据进行情感分类。**
**3. 使用torchtext对中文评论数据进行处理，构建了一个LSTM模型用来做情感分类。**
**4. 一共爬取了重庆、成都两个城市的前十热点景区的评论，一共6w+评论，但是只发布了1w条评论**

#### 代码目录：


+ data
    + stop_words.txt 停用词表
    + user_dict_all.txt 用户自定义词典
    + train.xlsx 爬取下来整理的数据，1w条
	+ cqk.xlsx 磁器口景区的评论数据
+ craw.py  爬虫代码
+ fasttext_train.py    fasttext训练代码
+ torchtext_rnn_classification.ipynb  torchtext处理程序和pytorch训练程序


#### 模型效果:

| 模型  | Acc | F值 |
| --------- | -------- |------ |
| fasttext  | 0.90  | 0.93  |
| LSTM  | 0.91  | -  |