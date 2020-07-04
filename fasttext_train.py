import pandas as pd
import jieba
import codecs
import pynlpir 
import fasttext
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
import numpy as np

stop_data_dir = 'data/stop_words.txt'         #停用词路径
user_dict_dir = "data/userdict_all.txt"       #自定义词典路径
train_data_dir  = 'data/data.xlsx'   ##必须包含 content 和 score 两列 ， utf-8格式
test_data_dir = 'data/cqk.xlsx'   ##必须包含 content这一列， utf-8格式
output_dir = 'e:/output.xlsx'
jieba.load_userdict(user_dict_dir)

data = pd.read_excel(train_data_dir,encoding='utf-8')
data.content = data.content.astype(str)

data['segment'] = data['content'].apply(lambda x:jieba.lcut(x))
real = pd.read_excel(test_data_dir,encoding='utf-8')

print('----------开始去停用词--------')
#去停用词
stop_list= [] #用来存停用词的list
with codecs.open(stop_data_dir,encoding='utf-8') as f:
    for x in f.readlines():
        x1 = x.replace("\n", "").replace("\r","").replace("\r\n","")
        stop_list.append(x1)
for i in range(len(data)):
    word = data['segment'][i].copy()
    for x in word:
        if x in stop_list:
            data['segment'][i].remove(x)

real['segment'] = real['content'].apply(lambda x:jieba.lcut(x))
for i in range(len(real)):
    word = real['segment'][i].copy()
    for x in word:
        if x in stop_list:
            real['segment'][i].remove(x)


train_data, test_data, train_label, test_label = train_test_split(data['segment'], data['score'], test_size=0.25, random_state=42)
train_data.index = range(len(train_data))
train_label.index = range(len(train_label))
test_data.index = range(len(test_data))
test_label.index = range(len(test_label))

with open('d:/train_semantic.txt','w',encoding='utf-8') as f:
    for i in range(len(train_data)):
        str1 = " ".join(train_data[i])+"\t"+"__label__"+str(train_label[i])+'\n'
        f.write(str1)

with open('d:/test_semantic.txt','w',encoding='utf-8') as f:
    for i in range(len(test_data)):
        str1 = " ".join(test_data[i])+"\t"+"__label__"+str(test_label[i])+'\n'
        f.write(str1)

def get_label(pred):
    index = np.argmax(pred[1])
    label = int(pred[0][index][-1])
    return label

def get_proba(pred):
    pred_dic = {}
    pred_dic[pred[0][0]] = pred[1][0]
    pred_dic[pred[0][1]] = pred[1][1]
    return pred_dic['__label__1']

print('------------------开始训练模型--------------------')
model = fasttext.train_supervised(input="d:/train_semantic.txt",lr=0.1, epoch=100, wordNgrams=3, dim=300)
print('------------------模型训练结束--------------------')


test_pred = []
for i in range(len(test_data)):
    r = model.predict(" ".join(test_data[i]),k=2)
    test_pred.append(get_label(r))

acc = accuracy_score(test_pred,test_label)
precision = precision_score(test_pred,test_label)
recall = recall_score(test_pred,test_label)
f1 = f1_score(test_pred,test_label)

print("准确率："+ str(acc)+"\n")
print("精准率："+ str(precision)+"\n")
print("召回率："+ str(recall)+"\n")
print("F1值："+ str(f1)+"\n")


print('------------------正在测试--------------------')
cqk=[]
for u in real['segment'].values:
    res = model.predict(" ".join(u),k=2)
    cqk.append(get_proba(res))
real['pred_score'] = cqk
# real['true_score'] = real['star'].apply(lambda x:0 if x<60  else 1)
print('------------------正在写入测试文件--------------------')
real[['content','pred_score']].to_excel(output_dir,encoding='gbk')