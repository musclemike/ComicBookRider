
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

import random
from blog.models import Post

from selenium import webdriver


class CrawledArticle():
    def __init__(self, image, link, title, content, date, categories, tags):
        self.image = image
        self.title = title
        self.content = content
        self.date = date
        self.link = link
        self.categories = categories
        self.tags = tags


class ArticleFetcher():
    def fetch(self):
            doc = BeautifulSoup(source_data, "lxml")

            url = "https://www.ign.com/comics"
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
            #response = requests.get(url, headers = headers)


            for article in doc.select("article"):

                image = article.select_one("img").attrs["src"]
                link = urljoin(url, article.select_one("a").attrs["href"])
                title = article.select(".item-title")[0].text
                if "-review" in image:
                    categories = "Review"
                else:
                    categories = "News"
                tags = ""
                article_url = link
                article_response = requests.get(article_url, headers=headers)
                art_doc = BeautifulSoup(article_response.text, "html.parser")

                content = art_doc.select("p")[0].text
                date = doc.select_one("a h3").attrs["data-timeago"]
                #date = date.replace("T", " ")
                #date = date[:-6]

                yield CrawledArticle(image, link, title, content, date, categories, tags)


def populate():

    fetcher = ArticleFetcher()

    #blogid = 1
    #counter = 0
    nono_list = ["Deals", "Sales", "Gift Card", "Today Only", "Sale"]

    for article in fetcher.fetch():
        check = any(item in article.title for item in nono_list)
        #if counter == N:
            #break
        if check:
            print("found one")
            continue
        else:

            #print(article.date+"\n"+article.image+"\n"+article.title+"\n"+article.content+"\n"+article.link)
            #print(article.date+"\n"+article.image+"\n"+article.title+"\n"+article.content+"<br><a href="+article.link+">Read More</a><br>\n\n")
            pst = Post.objects.get_or_create(author='IGN',  title=article.title, text = article.content, published_date=article.date, categories = article.categories, link = article.link, tags = article.tags, image = article.image )[0]

            #counter += 1
            #blogid += 1


chrome_path = r"C:\chromedriver_win32\chromedriver.exe"
options = webdriver.ChromeOptions()
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--incognito')
    #options.add_argument('--headless')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
driver = webdriver.Chrome(chrome_path, options=options)


driver.get("http://www.ign.com/?setccpref=US")
driver.get("https://www.ign.com/comics")
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    #match=False
    #while(match==False):
count = 0
while count < 10:
    lastCount = lenOfPage
    time.sleep(2)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    count += 1
        #if lastCount==lenOfPage:
            #match=True

source_data = driver.page_source


if __name__ == '__main__':
    print ('populating...')
    populate()
    print('populating complete')
