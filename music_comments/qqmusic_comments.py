import requests
from urllib.parse import urlencode
from time import sleep

def get_comments(topid,nums):
    pagenum=-1
    lasthotcommentid='song_237773700_1308046920_1568390631_1152921504623704244_1568900596'
    while True:
        pagenum=pagenum+1
        base_url='https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?'
        param={
            'g_tk':'5381',
            'loginUin':'0',
            'hostUin':'0',
            'format':'json',
            'inCharset':'utf8',
            'outCharset':'GB2312',
            'notice':'0',
            'platform':'yqq.json',
            'needNewCode':'0',
            'cid':'205360772',
            'reqtype':'2',
            'biztype':'1',
            'topid':topid,
            'cmd':'8',
            'needmusiccrit':'0',
            'pagenum':str(pagenum),
            'pagesize':'25',
            'lasthotcommentid':lasthotcommentid,
            'domain':'qq.com',
            'ct':'24',
            'cv':'10101010'
        }
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        url=base_url+urlencode(param)
        r=requests.get(url,headers=headers)
        json=r.json()
        comments=json['comment']['commentlist']
        with open('qqmusic'+topid+'.txt','a',encoding='utf-8') as f:
            for comment in comments:
                data=comment['rootcommentcontent']
                lasthotcommentid=comment['rootcommentid']
                f.write(data+'\n')
        if pagenum>=nums-1:
            break
        sleep(3)

if __name__ == '__main__':
    topid='237773700'       #歌曲不同时会变
    nums=input('the pages:')
    get_comments(topid,int(nums))