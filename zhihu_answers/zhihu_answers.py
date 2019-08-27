import requests
from re import findall
from urllib.parse import urlencode
from time import sleep
#爬取知乎回答，数量不太稳定，每个回答的offset不一样，大概在goal左右
def get_answers(question_id,goal):
    limit=5
    offset=5
    while True:
        base_url='https://www.zhihu.com/api/v4/questions/{}/answers?'.format(question_id)
        param={
            'include':'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info,paid_info_content;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
            'limit':str(limit),
            'offset':str(offset),
            'platform':'desktop',
            'sort_by':'default'
        }
        url=base_url+urlencode(param)
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        r=requests.get(url,headers=headers)
        json=r.json()
        datas=json['data']
        with open('zhihu_'+question_id+'.txt','a',encoding='utf-8') as f:
            for data in datas:
                contents=findall('<p>(.*?)</p>',data['content'])
                for content in contents:
                    f.write(content+'\n')
        if offset>=goal:
            break
        sleep(3)
        offset=offset+limit

if __name__ == '__main__':
    question_id=input('input the question_id:')
    goal=input('input the goal:')
    get_answers(question_id,int(goal))