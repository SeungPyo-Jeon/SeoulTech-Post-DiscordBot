# SeoulTech Bulletin Board Notification Discord Bot
서울과학기술대학교 게시판 알림을 위한 Discord bot 입니다.
![Image](https://github.com/user-attachments/assets/14b8ab95-4a9c-41e5-9cda-96a7bb42d058)

**Using Github Action Scheduling,**  
**Crawling bulletin board -> Ckeck new posts -> notify it by Discord**  

## Files
notificatorUtils.py ( Utils of crawling, json, discord webhook )  
notifyMainNotice.py ( "대학공지사항" scheduling file )  
--preMainNoticeList.json ( Json file for Checking )  
notifyAaiBulletin.py ( "인공지능응용학과" scheduling file )  
--preAaiBulletinList.json  ( Json file for Checking )  
