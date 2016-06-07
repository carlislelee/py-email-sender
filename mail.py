#!/usr/bin/python
# encoding=utf-8
# Filename: send_email.py
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import smtplib 
#from __future__ import with_statement
import ConfigParser
import sys


 
 
class SendEmail:
    def __init__(self, host, user, passwd):
        lInfo = user.split("@")
        self._user = user
        self._account = lInfo[0]
        self._me = self._account + "<" + self._user + ">"
        self._server = smtplib.SMTP() 
        self._server.connect(host) 
        self._server.login(self._account, passwd)
        print "login success"
     
    def sendTxtMail(self, to_list, sub, content, subtype='html'):   
        msg = MIMEText(content, _subtype=subtype, _charset='gb2312') 
        msg['Subject'] = sub 
        msg['From'] = self._me 
        msg['To'] = ";".join(to_list) 
        try:
            self._server.sendmail(self._me, to_list, msg.as_string())  
            return True 
        except Exception, e: 
            print str(e) 
            return False
         
    def sendAttachMail(self, to_list, sub, content,attachment_path, attachment_name, subtype='html'):
        msg = MIMEMultipart() 
        att1 = MIMEText(open(attachment_path,'rb').read(), 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"' % (attachment_name)
        msg.attach(att1)
        msg.attach(MIMEText(content, _subtype=subtype, _charset='gb2312'))
        msg['Subject'] = sub 
        msg['From'] = self._me
        msg['To'] = ";".join(to_list)
        try:
            self._server.sendmail(self._me, to_list, msg.as_string())  
            return True 
        except Exception, e: 
            print str(e) 
            return False

    def __del__(self):
        self._server.quit()
        self._server.close()
         

class CfgReader:
    def __init__(self , cfg_name):
        self._cfg = ConfigParser.ConfigParser()
        self._cfg.read(cfg_name)
    def getStrValueByKey(self, option, key):
       return self._cfg.get(option, key)
    def getHost(self):
      return self.getStrValueByKey("default","host")
    def getUser(self):
      return self.getStrValueByKey("default", "user")
    def getPwd(self):
       return self.getStrValueByKey("default", "pwd")
    def getSendToUser(self):
       return self.getStrValueByKey("default", "sendto")

##############################################################################
if __name__=='__main__':
    if len(sys.argv) != 4 :
      print len(sys.argv)
      print "error usage"
      #print "./sendMail.py cfg_path title content atts_path atts_show_name" 
      print "./sendMail.py cfg_path title content" 
      sys.exit(0)

    cfg_path=sys.argv[1]
    title=sys.argv[2]
    content=sys.argv[3]
    #atts_path=sys.argv[4]
    #atts_show_name=sys.argv[5]

    cfg = CfgReader(cfg_path)
    mail = SendEmail(cfg.getHost(), cfg.getUser(), cfg.getPwd())
    sendTo=cfg.getSendToUser().split(',')
    #if mail.sendAttachMail(sendTo, title, content, atts_path, atts_show_name):
    if mail.sendTxtMail(sendTo, title, content):
      print "send success"
    else:
      print "send error"

'''
#############################################################################         
mailto_list = ['caobaiyu@360.cn']
mail = SendEmail('smtp.126.com', 'dianjingmonitor@126.com', 'oniononion')
if mail.sendTxtMail(mailto_list, "test", "hello world£¡<br><br><h1>test<h1>"): 
    print "success" 
else: 
    print "error"
 
if mail.sendAttachMail(mailto_list, "test1", "hello world£¡<br><br><h1>test<h1>", '/data/hdp-ads-audit/user/caobaiyu/engineOut_stat_mapper.py','test.txt'): 
    print "success" 
else: 
    print "failed"
'''


     
