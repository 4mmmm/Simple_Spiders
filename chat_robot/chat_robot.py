import requests
#调用图灵机器人123的api，其实不算爬虫，算是调用一个网站的api，笔者较懒，干脆也放在这个repo里了
#首先你当然得申请图灵机器人官网的一个机器人
#本来可以写进微信和qq的，但腾讯抓得属实严，把微信和qq的网页版直接取消了，属实杀敌八百，自损一千，搞得我替代方法还没想出来，只能先用控制台

def reply(msg,key,userid):
    api_url='http://www.tuling123.com/openapi/api'
    data={
        'key':key,
        'info':msg,
        'userid':userid
        }
    r=requests.post(api_url,data).json()
    print('人工智障：',r['text'])

key=input('input your robot key:')#输入你在图灵机器人官网机器人的key
userid=input('input your robot userid:')#输入你在图灵机器人官网机器人的userid
while True:
    msg=input('我：')
    if msg=='给爷爬':#输入给爷爬退出
        break
    reply(msg,key,userid)