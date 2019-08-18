import re
import requests
from time import sleep

#词云所需库
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_comments(id,number):
    f_comment=open("weibo_comment_"+id+".txt", "a", encoding="utf8")
    #写入txt文件时不知道为啥不能用with，只能这样然后关闭f

    global file_path#全局文件保存路径便于存储和读取
    file_path='weibo_comment_'+id+'.txt'
    base_url='https://m.weibo.cn/comments/hotflow?id='
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    proxies={
        'http':'xxx:xxx:xxx'
    }#被反爬虫了用代理即可

    count=0#微博评论数
    while count<number:
        if count==0:
            try:
                url=base_url+id+'&mid='+id+'&max_id_type=0'
                response=requests.get(url,headers=headers)
                json=response.json()
                max_id=json['data']['max_id']
                datas=json['data']['data']
                for data in datas:
                    comment=data['text']
                    label_filter = re.compile(r'</?\w+[^>]*>', re.S)#正则去表情，方便之后做词云分析
                    comment = re.sub(label_filter, '', comment)+'\n'#加换行符增加可读性
                    f_comment.write(comment)
                    count+=1
                    print("已获取"+str(count)+"条评论。")
            except Exception as e:
                print(e)
                continue
        else:
            try:
                sleep(3)#防止爬得过快被识别
                url=url+id+'max_id='+str(max_id)+'&max_id_type=0'
                response=requests.get(url,headers=headers)
                json=response.json()
                max_id=json['data']['max_id']
                datas=json['data']['data']
                for data in datas:
                    comment=data['text']
                    label_filter = re.compile(r'</?\w+[^>]*>', re.S)
                    comment = re.sub(label_filter, '', comment)+'\n'
                    f_comment.write(comment)
                    count+=1
                    print("已获取"+str(count)+"条评论。")
            except Exception as e:
                print(e)
                continue
    f_comment.close()

def data_analyze(file_path):
    f_analyze = open(file_path,'r',encoding='UTF-8').read()
    wordcloud = WordCloud(background_color="white",font_path="C:/Windows/Fonts/STFANGSO.ttf",width=1000, height=860, margin=2).generate(f_analyze)
    #字体路径可自己更改，wordcloud默认不识别中文

    wordcloud.to_file('result.png')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    f_analyze.close()

if __name__ == "__main__":
    file_path=''
    id=input('input the weibo comment id you want:')
    number=int(input('input the number you want of the comment:'))
    get_comments(id,number)
    data_analyze(file_path)