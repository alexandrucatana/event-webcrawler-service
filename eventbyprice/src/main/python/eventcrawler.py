import requests
from bs4 import BeautifulSoup
import os
import sys
import collections
import time
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
from multiprocessing import Lock as Mutex

import queue
import concurrent.futures
import threading
import logging

class Eventcrawler:
    """
    Class to search for events for a given price
    """
    event_url = url = 'https://www.eventbrite.com/d/'

    def __init__(self, country, city, price):
        self.country = country
        self.city = city
        self.price = price
        self.event_url += self.country + "--" + self.city + "/all-events/"

        self.weblistPipeline = queue.Queue(maxsize=10)

        self.mutex = Mutex()
        self.thread_no = cpu_count()
        self.pool = ThreadPool(self.thread_no)
        self.max_pages = 2
        self.event = threading.Event()

        self.startPipeline()


    def startPipeline(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            # producer
            executor.submit(self.getEvents, self.weblistPipeline, self.event)
            # consumers
            executor.submit(self.extract_event_price, self.weblistPipeline, self.event)
            executor.submit(self.extract_event_price, self.weblistPipeline, self.event)
            executor.submit(self.extract_event_price, self.weblistPipeline, self.event)
            executor.submit(self.extract_event_price, self.weblistPipeline, self.event)
            executor.submit(self.extract_event_price, self.weblistPipeline, self.event)
            executor.submit(self.extract_event_price, self.weblistPipeline, self.event)
            executor.submit(self.extract_event_price, self.weblistPipeline, self.event)

            self.event.set()

    def getEvents(self, weblistPipeline, event):
        while not event.is_set():
            for page in range(1, self.max_pages):
                full_url = self.event_url + '?page=' + str(page)
                source_code = requests.get(full_url)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "lxml")

                linkContainer = soup.findAll("ul", {"class": "search-main-content__events-list"})[0]. \
                    findAll("a", {"tabindex": "0"})

                for link in linkContainer:
                    eventUrl = link.get('href')
                    weblistPipeline.put(eventUrl)
                    #eventName = link.get('aria-label')
                    #print (href, " , ", eventName[len("See more of "):len(eventName)])


    def extract_event_price(self, weblistPipeline, event):
        while not event.is_set() or not weblistPipeline.empty():
            eventName = weblistPipeline.get()
            webhtml = requests.get(eventName)
            soup = BeautifulSoup(webhtml.content, 'html.parser')
            obj = soup.find('div', {'class': 'js-display-price'})
            if not isinstance(obj, type(None)):
                price = obj.text
                if(any(i.isdigit() for i in price)):
                    print("Price= ", price)


if __name__ == "__main__":
    start_time = time.time()

    if(len(sys.argv) != 4):
        print("Run this program with following arguments:  1. country, 2. city, 3.price")
        sys.exit()

    Eventcrawler(sys.argv[1], sys.argv[2], sys.argv[3])

    print("--- %s seconds ---" % (time.time() - start_time))
