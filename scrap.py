#request得到url
#得到html的所有代码
#beatifulsoup筛选代码中的文字

import requests
from bs4 import BeautifulSoup
import json
import chardet
import re
from pprint import pprint


import pandas as pd
import jieba 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread

import warnings
warnings.filterwarnings("ignore")

def get_cid():
    url='http://api.bilibili.com/x/player/pagelist?bvid=BV1PK4y1b7dt&jsonp=jsonp'
    res=requests.get(url).text
    json_dict=json.loads(res)
    return json_dict["data"][0]["cid"]
#得到cid
def get_data(cid):
    final_url="https://api.bilibili.com/x/v1/dm/list.so?oid="+str(cid)
    final_res=requests.get(final_url)
    final_res.encoding=chardet.detect(final_res.content)['encoding']
    final_res = final_res.text
    pattern = re.compile("<d.*?>(.*?)</d>")
    data = pattern.findall(final_res)
    return data

def save_to_file(data):
    with open("dan_mu.txt",'w',encoding="utf-8") as f:
        for i in data:
            f.write(i)
            f.write("\n")

with open("dan_mu.txt",encoding="utf-8") as f:
    txt=f.read()
txt=txt.split()  #列表
#txt  #得到每行一个列表
data_cut=[jieba.lcut(x) for x in txt]  #将每行监测词，每个词分开 lcut（x）分词
#data_cut
#加入停用词
with open("stopwords-master/cn_stopwords.txt",encoding='utf-8') as f:
    stop=f.read()
stop=stop.split()  #变为list
stop=["道","说道","说","啊","哦","啊啊啊","哈哈哈","啦","了","哦哦哦","你","给","这","跟","这个"]+stop


#将data_cut去掉stop之中的词
s_data_cut = pd.Series(data_cut)  #把data_cut变为array的series放入s_data_cut
all_words_after = s_data_cut.apply(lambda x:[i for i in x if i not in stop])  #对series中每个词进行lambda函数操作，返回i若i不在stop中



 #词频统计
all_words=[]
for i in all_words_after:
    all_words.extend(i)         #去掉了stop的词，变回list
word_count=pd.Series(all_words).value_counts()  #Series后得到每个词的数量 pd.Series().values_counts()


#绘制词云
#读取背景图片
back_picture= imread("seven2.jpg")
#设置词云参数
wc=WordCloud(
            font_path="simfang.ttf",
            background_color="white",
            max_words=2000,
            mask=back_picture,
            max_font_size=200,
            random_state=42,
            collocations=False
            )
#传入单词和数据的Series
wc2=wc.fit_words(word_count)


#绘制词云图片
plt.figure(figsize=(16,8))
plt.imshow(wc2)
plt.axis("off")
plt.show()
wc.to_file("Ciyun.png")