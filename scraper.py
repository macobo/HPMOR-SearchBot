import time
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

client = MongoClient()
db = client.hpmor_database

def fixnewlines(text):
    "Removes extra whitespace in html body"
    return " ".join(text.split("\n"))

def crawl(chapter):
    r = requests.get('http://hpmor.com/chapter/{}'.format(chapter))
    title = fixnewlines(pq(r.text)('#chapter-title').text())
    paragraphs = pq(r.text)("#storycontent > p")
    contents = [fixnewlines(p.text) for p in paragraphs if p.text is not None]
    return {
        "title": title,
        "contents": contents
    }, r

db.chapters.drop()
chapter_id = 1
while True:
    results, response = crawl(chapter_id)
    if response.status_code != 200:
        print("No chapter at", chapter_id, ", stopping")
        break
    #print(results)
    id_ = db.chapters.insert(results)
    print(results["title"], id_)
    chapter_id += 1
    time.sleep(3)