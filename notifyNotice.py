from bs4 import BeautifulSoup
import requests
import json
from discord_webhook import DiscordWebhook,DiscordEmbed
import os

json_file_path = 'preMainNoticeList.json'
url_webhook = os.environ['WEBHOOK_MAINNOTICES']
url_seoultech_notice = "https://www.seoultech.ac.kr/service/info/notice/"
url_seoultech = "https://www.seoultech.ac.kr"
html_MainNotice = requests.get(url_seoultech_notice).text
bs_MainNotice = BeautifulSoup(html_MainNotice, 'html.parser').select('tr.body_tr')

def getMainNoticeList():
    list_MainNotice =[]
    
    for idx in range( len(bs_MainNotice) ):
        column = bs_MainNotice[idx]

        title = None
        href = None
        date = None
        color = None
        td_title = column.select('td')[1].select_one('a')
        if td_title is not None: # 일반글 or 공지글일때
            title = td_title.text.strip()
            href = column.select_one('td.dn2 a').attrs['href']
            color = "03b2f8"
        else: #최상단공지글 일때
            title = column.select_one('div').text.strip()
            href = column.select_one('a').attrs['href']
            color = "000000"
        date = column.select('td.dn5')[-1].text
        
        list_MainNotice.append( {"title": title, "href":href,"date":date, "color":color} )
    return list_MainNotice

def writeJson( file_path, notices):
    dict_MainNotice = {}
    for idx in range( len(notices)):
        dict_MainNotice[idx] = notices[idx]
    with open(file_path, 'w') as f:
        json.dump( dict_MainNotice, f)
        
def readJson( file_path):
    with open( file_path, 'r') as f:
        notices = json.load(f)
    notices = list( v for k,v in notices.items() )
    return notices

def notify( notices):
    for notice in notices:
        webhook = DiscordWebhook(url=url_webhook)
        req_content = requests.get(url_seoultech_notice+notice['href']).text
        src_content_img = BeautifulSoup(req_content, 'html.parser').select_one('td.cont').select('img')
        embed = DiscordEmbed(title=notice['title'],
                            description=url_seoultech_notice+notice['href'],
                              color=notice['color'])
        if len(src_content_img):
            print(src_content_img[0]['src'])
            if src_content_img[0]['src'].startswith('http'):
                embed.set_image(url=src_content_img[0]['src'])
            else:
                embed.set_image(url=url_seoultech+src_content_img[0]['src'])
                
        webhook.add_embed(embed)
        response = webhook.execute()
        print(response)

curMainNoticeList = getMainNoticeList()
copy_curMainNoticeList = curMainNoticeList.copy()
preMainNoticeList = readJson(file_path=json_file_path)
newMainNoticeList = []

for idx in range( len(copy_curMainNoticeList)):
    curNotice = copy_curMainNoticeList.pop()
    for i in range( len(preMainNoticeList)):
        preNotice = preMainNoticeList.pop()
        if curNotice['title'] == preNotice['title']:
            curNotice = None
            break
        else:
            preMainNoticeList.append( preNotice)
    if curNotice is not None:
        newMainNoticeList.append(curNotice)
    
if len(newMainNoticeList):
    notify(newMainNoticeList)
    writeJson(  file_path=json_file_path,notices=curMainNoticeList)