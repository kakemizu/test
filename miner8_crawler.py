import urllib
import lxml.html
import re
import sys
from collections import defaultdict

#def get_news_info(news_urls):
def get_news_info():
	news_urls = ["http://miner8.com/ja/55042","http://miner8.com/ja/76213","http://miner8.com/ja/96748","http://miner8.com/ja/95446","http://miner8.com/ja/82183"]
	news_info = []

	for news_url in news_urls:
		info = defaultdict(list)

		html_string = urllib.urlopen(news_url).read().decode("utf-8")
		html_elem = lxml.html.fromstring(html_string)

		#url
		info["url"] = news_url
		print (info["url"])

		#title
		title = html_elem.xpath('//meta[@property="og:title"]')[0].get("content")
		if len(title) != 0:
			info["title"] = title
		else:
			info["title"] = None

		print ("   title : " + info["title"])

		#image_main
		image_main = html_elem.xpath('//meta[@property="og:image"]')[0].get("content")
		if len(image_main) != 0:
			info["image_main"] = image_main
		else:
			info["image_main"] = None

		#image
		image = html_elem.xpath('//div[@class="entry-content"]')[0]
		image_url = image.xpath('descendant::img[@src]')


		if len(image) != 0:
			for img in image_url:
				info["image"].append(img.get("src"))
		else:
			info["image"] = None

		print ("   image_main : " + info["image_main"])
		print (len(info["image"]))
		for img in info["image"]:
			print ("   image : " + img)

		#date
		predate = html_elem.xpath('//time')[0].text_content()
		if len(predate) != 0:
			year = ""
			month = ""
			day = ""

			year = predate[0:4].zfill(4)

			if(predate[5:2].isdigit()):
				month = predate[5:2].zfill(2)
			else:
				month = predate[5].zfill(2)

			if(predate[-3:-1].isdigit()):
				day = predate[-3:-1].zfill(2)
			else:
				day = predate[-2].zfill(2)

			date = year+month+day

			info["date"] = date
		else:
			info["date"] = None
		
		print ("   date : " + info["date"])

		#category
		categories = html_elem.xpath('//a[@rel="category tag"]')
		if len(categories) != 0:
			for category in categories:
				info["category"].append(category.text)
		else:
			info["category"] = None

		for cate in info["category"]:
			print ("   category : " + cate)
		#text

		#keyword
		keys = html_elem.xpath('//div[@class="post-keyword"]')[0]
		if len(keys) != 0:
			key = keys.xpath('descendant::a')

			for keyword in key:
				info["keyword"].append(keyword.text.rstrip(" "))
		else:
			info["keyword"] = None

		for key in info["keyword"]:
			print ("   keyword : " + key)

		#author
		author = html_elem.xpath('//a[@class="author-link"]')[0].text
		if len(author) != 0:
			info["author"] = author.strip()
		else:
			info["author"] = None

		print ("   author : " + info["author"])

		print ("------------------------------------------------")

	return news_info

	"""
	news_info = []
	info = {}

	for news_url in news_urls:
		html_string = urllib.urlopen(news_url).read().decode("utf-8")
		html_elem = lxml.html.fromstring(html_string)

		#url
		info["url"] = news_url
		print "url : " + info["url"]

		#title
		title = html_elem.xpath('//meta[@property="og:title"]')[0].get("content")
		if len(title) != 0:
			info["title"] = title
		else:
			info["title"] = None

		print "title : " + info["title"]

		#image
		image = html_elem.xpath('//meta[@property="og:image"]')[0].get("content")
		if len(image) != 0:
			info["image"] = image
		else:
			info["image"] = None

		print "image : " + info["image"]

		#date
		predate = html_elem.xpath('//time')[0].text_content()
		if len(predate) != 0:
			year = ""
			month = ""
			day = ""

			year = predate[0:4].zfill(4)

			if(predate[5:2].isdigit()):
				month = predate[5:2].zfill(2)
			else:
				month = predate[5].zfill(2)

			if(predate[-3:-1].isdigit()):
				day = predate[-3:-1].zfill(2)
			else:
				day = predate[-2].zfill(2)

			date = year+month+day

			info["date"] = date
		else:
			info["date"] = None
		
		print "date : " + info["date"]

		#category
		categories = html_elem.xpath('//a[@rel="category tag"]')
		if len(categories) != 0:
			if len(categories) == 1:
				info["category"] = categories[0].text
			else:
				category = ""
				for c in categories:
					category += c.text + ","
				info["category"] = category[0 : len(category) - 1]
		else:
			info["category"] = None

		print "category : " + info["category"]

		#text
		text = html_elem.xpath('//div[@class="entry-content"]')[0].text_content()
		info["text"] = text
		print info['text']

		#keyword
		key = html_elem.xpath('//div[@class="post-keyword"]')
		keywords = key[0].xpath('descendant::a')
		if len(keywords) != 0:
			if len(keywords) == 1:
				info["keyword"] = keywords[0].text
			else:
				keyword = ""
				for k in keywords:
					keyword += k.text + ","
				info["keyword"] = keyword[0 : len(keyword) - 1]
		else:
			info["keyword"] = None

		print "keyword : " + info["keyword"]

		#author
		author = html_elem.xpath('//a[@class="author-link"]')[0].text
		if len(author) != 0:
			info["author"] = author.strip()
		else:
			info["author"] = None

		print "author : " + info["author"]

	return news_info
	"""

def get_news_urls(page_urls):
	news_urls = []
	counter = 0
 
	for page_url in page_urls:
		counter += 1
		html_string = urllib.urlopen(page_url).read().decode("utf-8")
		html_elem = lxml.html.fromstring(html_string)

		articles_left = html_elem.xpath('//div[@class="list-left"]')

		for article_left in articles_left:
			link = article_left.xpath('descendant::a')
			url = link[0].get("href")

			news_urls.append(url)

		sys.stdout.write("\r   get news url ... " + str(int(float(counter * 100) / len(page_urls))) + "%")

	return news_urls

def get_page_urls(news_path_urls):
	page_urls = []

	for path_url in news_path_urls:
		search_url = path_url
		page_urls.append(path_url)

		while True:

			html_string = urllib.urlopen(search_url).read().decode("utf-8")
			html_elem = lxml.html.fromstring(html_string)

			next_page = html_elem.xpath('//a[@class="next page-numbers"]')

			if len(next_page) != 0:
				next_page_url = next_page[0].get('href')
				page_urls.append(next_page_url)
				search_url = next_page_url

			else:
				print ("   end : " + path_url)
				break

	return page_urls

def get_news_path_urls(miner8):
	news_path_urls = []

	html_string = urllib.urlopen(miner8).read().decode("utf-8")
	html_elem = lxml.html.fromstring(html_string)

	header = html_elem.xpath('//header[@id="masthead"]')
	li = header[0].xpath('descendant::li')
	for link in li:
		a = link.xpath('descendant::a')
		url = a[0].get('href')
		news_path_urls.append(url)

	return news_path_urls

def result(result):
	print ("")

	for r in result:
		print (r)

	print ("")

if __name__ == '__main__':

	get_news_info()




	"""
	miner8 = "http://miner8.com/"
	language = "ja/"

	print "start get_news_path_urls"
	news_path_urls = get_news_path_urls(miner8 + language)
	print "finish get_news_path_urls"
	print ""

	#result(news_path_urls)

	print "start get_page_urls"
	page_urls = get_page_urls(news_path_urls)
	print "finish get_page_urls"
	print ""

	#result(page_urls)

	print "start get_news_urls"
	news_urls = get_news_urls(page_urls)
	print "finish get_news_urls"
	print ""

	#result(news_urls)
	#news_urls=[]
	print "start get_news_info"
	get_news_info(news_urls)
	#print "finish get_news_info"
	print ""
	"""


else:
	print ("This isn't main.")