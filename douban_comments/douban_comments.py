import requests

from bs4 import BeautifulSoup
from time import sleep

def get_comments(id,pages):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    start=0
    while start<=20*(pages-1):
        url='https://movie.douban.com/subject/'+id+'/comments?start='+str(start)+'&limit=20&sort=new_score&status=P&comments_only=1'
        r=requests.get(url,headers=headers)
        soup=BeautifulSoup(r.json()['html'],'lxml')
        #json返回居然是类似于html的网页代码，说好的json文件易于人编写和阅读呢？
        comments=soup.find_all('span',attrs={'class':'short'})
        print('正在爬取','第',start/20+1,'页')
        with open('douban_comments'+id+'.txt','a+',encoding='utf-8') as f:
            for comment in comments:
                f.write(comment.string+'\n')
        start+=20
        sleep(3)#防止爬取过快被反爬虫

#纠结了一哈要不要把数据分析这一块单独写成py文件，毕竟每次都写一遍这个函数属实累成傻狗，

if __name__ == '__main__':
    id=input('please input the id of the movie:')
    pages=input('please input the pages of the movie comments:')
    get_comments(id,int(pages))