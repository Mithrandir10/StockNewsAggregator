from __future__ import absolute_import, unicode_literals

import requests
from time import sleep
import csv
import os
from os import link
from bs4 import BeautifulSoup

from celery import shared_task
from .models import News
from celery.schedules import crontab




@shared_task()
def news_task():
    News.objects.all().delete()
    print('Collecting news article..')
    for i in range(1,2):
      url=f"https://www.livemint.com/companies/page-{i}"
      page_response = requests.get(url, timeout=240)
      page_content = BeautifulSoup(page_response.content, "lxml")
      main_content=page_content.findAll('li',class_="clearfix")
      hline=page_content.findAll('h2', class_="headline")
      datediv=page_content.findAll('div',class_="headlineSec")
      for i in datediv:
       j=i.find('h2',class_="headline").text.strip()
       k=i.find('span',class_="fl date").text.strip()
       l=i.find('h2',class_="headline")
       x=l.find('a',href=True)
       x=x['href']
       page_secondary=requests.get(x,timeout=240)
       page_content_sec=BeautifulSoup(page_secondary.content,"lxml")
       try:
          desc=page_content_sec.find("ul",class_="highlights").text.strip()
       except:
          desc="No description available"
       count=k.find("Updated:")
       print(count)
       if(count==-1):
        count=17-8      
       k=k[count+8:]
       j=j.encode('unicode-escape').decode('utf-8')

       print({'title':j,'description': desc,
                 'pubdate': k,'link':x})

       News.objects.create(
                title=j,
                description=desc,
                pubdate=k,
                link=x,
                news_bool=False
            )

news_task()



