from notificatorUtils import *
import os

json_file_path_aai = 'preAaiBulletinList.json'
url_webhook_aai = os.environ['WEBHOOK_AAIBULLETIN']
url_seoultech_aai_bulletin = "https://aai.seoultech.ac.kr/information/bulletin/"

curAaiBulletinList = getNoticeList(ori_url=url_seoultech_aai_bulletin)
copy_curAaiBulletinList = curAaiBulletinList.copy()
preAaiBulletinList = readJson(file_path=json_file_path_aai)
newAaiBulletinList = []

for idx in range( len(copy_curAaiBulletinList)):
    curNotice = copy_curAaiBulletinList.pop()
    for i in range( len(preAaiBulletinList)):
        preNotice = preAaiBulletinList.pop()
        if curNotice['title'] == preNotice['title']:
            curNotice = None
            break
        else:
            preAaiBulletinList.append( preNotice)
    if curNotice is not None:
        newAaiBulletinList.append(curNotice)
    
if len(newAaiBulletinList):
    notify(webhook_url= url_webhook_aai, source_url=url_seoultech_aai_bulletin ,notices= newAaiBulletinList)
    writeJson(  file_path=json_file_path_aai,notices=curAaiBulletinList)