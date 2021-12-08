# coding=utf-8
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth 
from requests_html import HTMLSession
import time
import datetime

def get_questions(url):
    title_list=[];
    session = HTMLSession()
    resp = session.get(url)    
    questions = resp.html.find('fieldset', first=True).find('.div_question')
    for i, q in enumerate(questions):
        title=q.find('.div_title_question_all', first=True).text
        title_list.append(title)
        time.sleep(0.05)
    return title_list

def get_answers(questions):
    answers=[]
    for q in questions:
        length=len(answers)
        for key in data_lib.keys():
            if key in q:
                answers.append(data_lib[key]) 
                break
        if(length==len(answers)):
            answers.append(" ") 
    return answers

async def auto_fill(answers):
    
    browser = await launch({
        'executablePath': open("./config.txt","r").read(),
        'headless': False,
        'args': ['--no-sandbox', '--window-size=1366,850']
    })
    page = await browser.newPage()
    await page.setViewport({'width':1366,'height':768})
    await stealth(page)
    await page.goto(url)
    try:
        for i in range(0,len(answers)):
            await page.type('#q%d'%(i+1), answers[i])
        await asyncio.sleep(0.8) 
        submit = await page.querySelector('#submit_button')
        await submit.click()
        await asyncio.sleep(0.5)
    except Exception as e:
        input("[!]发生错误，请手动提交！")
        exit(0)
    else:
        return
    
def enjoy_it(url):
    print('\r\n[*]开始爬取问卷内容')
    questions=get_questions(url)
    print(questions)
    print('[*]尝试获取答案')
    answers=get_answers(questions)
    print(answers)
    print('[*]开始自动填写')
    asyncio.get_event_loop().run_until_complete(auto_fill(answers))

print("#BUCT自动志愿v2.2")
print("#by:Lpb QQ:2206080975")
try:
    data_lib=eval(open("./data_lib.txt","r+",encoding='utf-8').read())
    print("[*]读入数据... ...")
except IOError:
    print("[!]未找到data_lib.txt或者数据格式不正确!")
    input("[*]按下任意键结束")
    exit(0)
else:
    print("[*]读入数据完成")
url=input("[>]问卷地址：")
fill_time=input("[>]开始时间（年 月 日 时 分）：")
fill_time=fill_time.split(' ')
start_time = datetime.datetime(int(fill_time[0]),int(fill_time[1]),int(fill_time[2]),int(fill_time[3]),int(fill_time[4]),1)
print("[*]正在等待... ...")
while(True):
    dtn = datetime.datetime.now()  
    print('\r'+str(dtn).split('.')[0],end='',flush=True)
    if dtn > start_time:
        enjoy_it(url) 
        input("[*]按下任意键结束")
        exit(0)

