
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
        for page in range(1,11):
            url = "https://www.cbr.com/category/comics/news/page/" + str(page) + "/"

            print (url)

            #while url != "":

            time.sleep(1)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
            response = requests.get(url, headers = headers)
            doc = BeautifulSoup(response.text, "html.parser")
            article_url = ""
            article_response = ""
            art_doc = ""


            count = 0
            for article in doc.select("article"):
                if count == 19 :
                    break
                try:
                    image = article.select_one("source").attrs["data-srcset"]
                except KeyError:
                    image = article.select_one("source").attrs["srcset"]
                except AttributeError:
                    if article.select_one("h1").string == "CBR – Privacy Policy":
                        break
                link = urljoin(url, article.select("a")[0].attrs["href"])
                title = article.select_one(".bc-title-link").string

                if "-review" in image:
                    categories = "Review"
                else:
                    categories = "News"
                tags = "CBR"
                article_url = link
                article_response = requests.get(article_url, headers=headers)
                art_doc = BeautifulSoup(article_response.text, "html.parser")

                content = art_doc.select("p")[0].text
                date = doc.select(".bc-date")[count].attrs["datetime"]
                image = (image.split())[0]




                yield CrawledArticle(image, link, title, content, date, categories, tags)
                count += 1


def populate():

    fetcher = ArticleFetcher()

    for article in fetcher.fetch():
        #if Post.objects.filter(title=article.title).exists():

        try:
            pst = Post.objects.get_or_create(author='CBR',  title=article.title, text = article.content, published_date=article.date, categories = article.categories, link = article.link, tags = article.tags, image = article.image )[0]
            print("found new article")
        except django.db.utils.IntegrityError:
            print("duplicate found")




if __name__ == '__main__':
    print ('populating...')
    populate()
    print('populating complete')
