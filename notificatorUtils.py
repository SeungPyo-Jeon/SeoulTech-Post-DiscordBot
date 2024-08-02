from bs4 import BeautifulSoup
import requests
import json
from discord_webhook import DiscordWebhook,DiscordEmbed

url_seoultech = "https://www.seoultech.ac.kr"

def getNoticeList( ori_url ):
    list_Notice =[]
    html_Notice = requests.get(ori_url).text
    bs_Notice = BeautifulSoup(html_Notice, 'html.parser').select('tr.body_tr')

    for idx in range( len(bs_Notice) ):
        column = bs_Notice[idx]

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
        
        list_Notice.append( {"title": title, "href":href,"date":date, "color":color} )
    return list_Notice

def writeJson( file_path, notices):
    dict_Notice = {}
    for idx in range( len(notices)):
        dict_Notice[idx] = notices[idx]
    with open(file_path, 'w') as f:
        json.dump( dict_Notice, f)
        
def readJson( file_path):
    with open( file_path, 'r') as f:
        notices = json.load(f)
    notices = list( v for k,v in notices.items() )
    return notices

def notify( webhook_url, source_url,notices):
    for notice in notices:
        webhook = DiscordWebhook(url=webhook_url)
        req_content = requests.get(source_url+notice['href']).text
        src_content_img = BeautifulSoup(req_content, 'html.parser').select_one('td.cont').select('img')
        embed = DiscordEmbed(title=notice['title'],
                            description=source_url+notice['href'],
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