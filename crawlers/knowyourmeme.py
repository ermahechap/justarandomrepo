'''
knowyourmeme.com image crawler:
-------------------------------------------
Script designed to specifically crawl meme templates to be used in ml(and self enjoyment).

url: https://knowyourmeme.com/photos/templates/page/<page_number>
So, as you can see, we are lucky enough that knowyoumeme has pagination here


IMPORTANT: check robots.txt
* http://www.useragentstring.com/pages/useragentstring.php
* https://knowyourmeme.com/robots.txt

Also, check that the folder where you are going to save the images already exists...
too lazy to write something that creates the folder
'''
from bs4 import BeautifulSoup as bs
import requests
import shutil
import json
import time
import sys
import os

url = 'https://knowyourmeme.com'
img_save_path = 'templates/'
json_save_path = 'data.json'
paging_path = '/photos/templates/page/'
headers = {'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

pages = 47 #remeber to check number of pages beforehand
ids = 1
structure = {}

#crawls template and tags
def img_crawls(template_path, headers):
	site_url = url + template_path
	t0 = time.time()
	r = requests.get(site_url, headers = headers)
	response_delay = time.time()-t0
	
	data = r.text
	soup = bs(data, 'lxml')
	
	section = soup.body.find(id='content')
	left = section.find(id='maru')
	right = section.find(class_='right').select('.sidebar_box')[0]

	template_url = left.select('div#photo_wrapper a')[0]['href']
	taglist = right.select('p#tag_list a')
	tags = [str(tag.string) for tag in taglist]
	
	time.sleep(10*response_delay)
	return {'site_url': site_url, 
					'template_url': template_url,
					'tags': tags}

for i in range(1,pages):
	page_url = url + paging_path + str(i)
	r = requests.get(page_url, headers = headers)
	data = r.text
	soup = bs(data,'lxml')
	section = soup.body.find(id='content').find(id='maru').find(id="infinite-scroll-wrapper")

	urls = section.select("div.item a")
	for template in urls:
		template_path = template['href']
		info = img_crawls(template_path, headers)
		print(info['site_url']) #### DEBUG
		# store
		structure[ids]=info 
		img_type = '.' + info['template_url'].split('.')[-1]
		if not img_type in ['.jpg','.png','.jpeg'] :
			img_type='.jpeg'
		img_get = requests.get(info['template_url'], stream = True)
		with open(img_save_path + str(ids) + img_type, 'wb') as out_file:
			shutil.copyfileobj(img_get.raw, out_file)
			print('Image '+str(ids)+' crawled...') #### DEBUG
		del img_get
		ids+=1
	time.sleep(5)

with open(json_save_path,'w') as out_file:
	json.dump(structure,out_file)

