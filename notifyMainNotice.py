from notificatorUtils import * 
import os

json_file_path_main = 'preMainNoticeList.json'
url_webhook_main = = os.environ['WEBHOOK_MAINNOTICES']
url_seoultech_notice = "https://www.seoultech.ac.kr/service/info/notice/"

curMainNoticeList = getNoticeList(ori_url = url_seoultech_notice)
copy_curMainNoticeList = curMainNoticeList.copy()
preMainNoticeList = readJson(file_path=json_file_path_main)
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
    notify(webhook_url=url_webhook_main,source_url=url_seoultech_notice,notices= newMainNoticeList)
    writeJson(  file_path=json_file_path_main,notices=curMainNoticeList)