# -*- coding: utf-8 -*-

#import urllib.request
import sys
import requests
import json
import re
#from datetime import datetime
import datetime
from html.parser import HTMLParser  



class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.str1 = ''
		self.str2 = ''

	def handle_starttag(self, tag, attrs):
		if tag == "input":
			if len(attrs) == 0:
				pass
			else:
				#print(attrs)
				for (variable, value) in attrs:
					if value == "StBoardDb":
						#print(attrs[2][1])
						self.str1 = attrs[2][1]
						#print(str1)
						#print(attrs)
					if value == 'StDocUNID':
						self.str2 = attrs[2][1]
						
class HtmlParserMenu(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.flag = False
		self.str=''
			
	def handle_entityref(self, name):
		if self.flag == True:
			print(name)
		
	def handle_data(self, data):
		if self.flag == True :
			#print(data)
			#print("dd")
			self.str += data
			pass
	def handle_starttag(self, tag, attrs):
		#print(tag)
		if tag == 'p':
			#print(tag)
			#print('a')
			self.flag = True
			
	def handle_endtag(self,tag):
		#print(tag)
		if tag == 'p':
			self.flag = False
			self.str += '\n'
			#pass
			


def Login():
	url_login= "http://oa.xinwei.com.cn/names.nsf?Login"
	url_json = "http://oa.xinwei.com.cn/servlet/digishell/dataService"
	body = {#'%%ModDate':'0000000000000000',
		'Remote_Addr':'172.16.2.62',
		'$$HTMLFrontMatter':'<!DOCTYPE html>',
		'RedirectTo':'/Produce/WeboaConfig.nsf/index.html',
		'$PublicAccess':'1',
		'ReasonType':'0',
		#'%%ModDate':'0871326800000070',
		'Username':'用户名',
		'Password':'密码'
		}
	data1 = {'widget_ZXTZ':{'count':6,'field':['StPostTime','StTitle','@DocumentUniqueID'],'path':'bbs/DigiFlowBBSNew.nsf','type':'GetDocFromView','view':'TodayView'},
			'widget_ZLZL':{'count':6,'field':['StPubDate','StTitle','@DocumentUniqueID'],'path':'Application/DigiFlowInfoPublish.nsf','type':'GetDocFromView','view':'PublishDoneViewForZL_ALL'},
			'widget_SJZL':{'count':6,'field':['StPubDate','StTitle','@DocumentUniqueID'],'path':'Application/DigiFlowInfoPublish.nsf','type':'GetDocFromView','view':'PublishDoneViewForSJZL_ALL'}
			}
	head1 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'	
			}
	head2 = {'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest'
			}
			
	s = requests.session()
	r = s.post(url_login, data = body, headers = head1)
	
	r = s.post(url_json, json = data1, headers = head2)
	return s,r
	
def matchDate(json_data, date):
	json_dict = json.loads(json_data)
	list = json_dict['widget_ZXTZ']['items']
	for x in list:
		#print(x['StTitle'])
		st = str(x['StTitle'])
		st = st[2:-2]
		m = re.match(r'(\d+)月(\d+)[日,号]菜单',st)
		if m:
			month = m.group(1)
			day = m.group(2)
			if((int(month) == int(date[0])) and (int(day) == int(date[1])) ):
				#print(st)
				#print(x['@DocumentUniqueID'])		
				url = 'http://oa.xinwei.com.cn/bbs/DigiFlowBBSNew.nsf/0/%s?opendocument' % str(x['@DocumentUniqueID'])[2:-2]
				return url
			else:
				return None

def getMenu(url, s):
	head = {#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			#'Accept-Language':'zh-CN,zh;q=0.8',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 			
			}
	r = s.get(url, headers = head)
	hp = MyHTMLParser()
	hp.feed(r.text)
	hp.close()
	url_menu = 'http://oa.xinwei.com.cn/bbs/%s/0/%s?opendocument' % (hp.str1,hp.str2)
	r = s.get(url_menu, headers = head)
	
	hpm = HtmlParserMenu()
	hpm.feed(r.text)
	hpm.close()
	
	return hpm.str

import itchat	
import time
import threading

if __name__ == '__main__':
	today = datetime.date.today()
	month_m = today.strftime('%m')
	day_m = today.strftime('%d')
	print(month_m,day_m)
	#(s,r) = Login()
	#url_menuLink = matchDate(r.text, (7,7))
	#menu = getMenu(url_menuLink, s)
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	#print(msg['Sex'])
	#print(msg['Type'])
	#print(msg['FromUserName'])
	#print(msg['ToUserName'])
	#print(msg['Content'])
	#print(msg['Text'])
	#print(msg['User'])
	#print(msg['User']['Sex'])
	#print(msg['User']['NickName'])
	#print('-------------')
	#print(msg.text)
	print(a)
	print(msg.text)
	return msg.text
	flag = False
	if (msg.text == '今天') or (msg.text == 'today'):
		today = datetime.date.today()
		month_m = today.strftime('%m')
		day_m = today.strftime('%d')
		flag = True
		currentday = '今天'
		#print('aa')
	if msg.text == 'yesterday' or msg.text == '昨天':
		flag = True
		oneday = datetime.timedelta(days=1)
		yesterday = datetime.date.today() - oneday
		month_m = yesterday.strftime('%m')
		day_m = yesterday.strftime('%d')
		currentday = '昨天'
		
	if msg.text == '前天' :
		flag = True
		oneday = datetime.timedelta(days=2)
		yesterday = datetime.date.today() - oneday
		month_m = yesterday.strftime('%m')
		day_m = yesterday.strftime('%d')
		currentday = '前天'
		
	if flag == True:
		#flag = False
		#print('bb')
		#return "dd"
		(s,r) = Login()
		url_menuLink = matchDate(r.text, (month_m,day_m))
		if url_menuLink == None:
			restr = '%s无菜单' % currentday
			return restr
		menu = getMenu(url_menuLink, s)
		return menu
		
	#return "sdf"
	
def test():
	while True:	
		time.sleep(2)	
		print(1)
		itchat.send('hhh')
		
	
 
a = 0
itchat.auto_login(hotReload = True,enableCmdQR=True)
itchat.run(debug=False,blockThread=False)

#t = threading.Thread(target=test, name = "test")
#t.start()
while True:
	time.sleep(5)	

	print(a)
	a = a+1
	itchat.send('hhh')
	pass
	#with open('./tt.txt','w',encoding='utf-8') as f:
		#f.write(r.text)
	#	f.write(menu)


#2.考虑无法访问
#3日期变化

