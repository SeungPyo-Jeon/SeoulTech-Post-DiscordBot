from notificatorUtils import *
import os

json_file_path_graduate = 'preGraduateBulletinList.json'
url_webhook_graduate = os.environ['WEBHOOK_GRADUATEBULLETIN']
url_seoultech_graduate_bulletin = "https://www.seoultech.ac.kr/service/info/graduate/"

curGraduateBulletinList = getNoticeList(ori_url=url_seoultech_graduate_bulletin)
copy_curGraduateBulletinList = curGraduateBulletinList.copy()
preGraduateBulletinList = readJson(file_path=json_file_path_graduate)
newGraduateBulletinList = []

for idx in range( len(copy_curGraduateBulletinList)):
    curNotice = copy_curGraduateBulletinList.pop()
    for i in range( len(preGraduateBulletinList)):
        preNotice = preGraduateBulletinList.pop()
        if curNotice['title'] == preNotice['title']:
            curNotice = None
            break
        else:
            preGraduateBulletinList.insert(0, preNotice)
    if curNotice is not None:
        newGraduateBulletinList.insert(0, curNotice)
    
if len(newGraduateBulletinList):
    notify(webhook_url= url_webhook_graduate, source_url=url_seoultech_graduate_bulletin ,notices= newGraduateBulletinList)
    writeJson(  file_path=json_file_path_graduate,notices=curGraduateBulletinList)
