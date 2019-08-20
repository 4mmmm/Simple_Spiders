import requests
import re

from PIL import Image

import numpy as  np
import jieba
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt

#可通过输入的b站视频爬取该视频的弹幕并稍作词云分析
def get_barrage(origin_url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    
    response=requests.get(origin_url,headers=headers)
    cid = re.findall(r'cid=(\d+)&aid', response.text)[0]
    result_url='https://comment.bilibili.com/'+cid+'.xml'
    response=requests.get(result_url,headers=headers)
    
    response.encoding=response.apparent_encoding
    #一开始保存下来的txt总是乱码，改成utf-8，后来调试的时候看到response有个apparent_encoding，google一下了才知道要这么加一句
    
    datas = re.findall(r'<d.*?>(.*?)</d>', response.text)
    with open('bilibili_barrage'+cid+'.txt','w',encoding='utf-8') as f:
        for data in datas:
            f.write(data+'\n')

    global file_path
    file_path='bilibili_barrage'+cid+'.txt'

def data_analyze(file_path):
    background=np.array(Image.open('background.jpg'))
    text = open(file_path,'r',encoding='UTF-8').read()
    result_text=jieba_text(text)

    wc=WordCloud(
    background_color="white",
    max_words=150,
    mask=background,#设置图片的背景
    max_font_size=60,
    random_state=42,
    font_path='C:/Windows/Fonts/simkai.ttf'   #中文处理，用系统自带的字体
    ).generate(result_text)

    image_colors=ImageColorGenerator(background)
    plt.imshow(wc,interpolation='bilinear')
    plt.axis('off')
    plt.show()
    plt.axis("off")
    plt.imshow(background,cmap=plt.cm.gray)
    wc.to_file('barrage.png')

def jieba_text(text):
    jieba.add_word("啤站")
    mywordlist=[]
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用/连接
    listStr='/'.join(seg_list)
    #打开停用词表
    f_stop=open('stopwords.txt',encoding="utf8")
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    #对默认模式分词的进行遍历，去除停用词
    for myword in listStr.split('/'):
        #去除停用词
        if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)


if __name__ == "__main__":
    file_path=''
    url=input('input the url of the bilibili video:')
    get_barrage(url)
    data_analyze(file_path)