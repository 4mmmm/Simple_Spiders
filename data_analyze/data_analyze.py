import jieba
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from wordcloud import ImageColorGenerator, WordCloud

def data_analyze(file_path):
    background=np.array(Image.open('background.jpg'))
    text = open(file_path,'r',encoding='UTF-8').read()
    result_text=jieba_text(text)

    wc=WordCloud(
    background_color="white",
    max_words=1800,
    mask=background,#设置图片的背景
    max_font_size=100,
    font_path='C:/Windows/Fonts/simkai.ttf'#用系统自带的中文，wordcloud默认不识别中文
    ).generate(result_text)#初始化词云图片的一些参数

    image_colors=ImageColorGenerator(background)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

    plt.axis("off")
    plt.imshow(background,cmap=plt.cm.gray)#咋这个background和没加一样？佛啦
    wc.to_file('result.png')

#jieba中文分词使得词云显示不是显示一整句话
def jieba_text(text):
    jieba.add_word('测试')
    mywordlist=[]
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用 / 连接
    listStr='/'.join(seg_list)
    #打开停用词表
    f_stop=open('stopwords.txt',encoding='utf8')
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()
    
    f_stop_seg_list=f_stop_text.split("\n")

    for myword in listStr.split('/'):#去除停词
        if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)

if __name__ =='__main__':
    file_path=input('please input the path of the file:')
    data_analyze(file_path)