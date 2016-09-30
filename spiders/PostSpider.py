# coding=utf-8
'''
Created on Aug 19, 2016

@author: Charlie
'''

from bs4 import BeautifulSoup
from utils.GeneralUtils import getPage, printSuccess, printWarning, safeExec

import sqlalchemy
import re


class PostSpider(object):
    '''
    this spider fetches the url of posts based on the division url,
    and managed to fetch all posts based on the navigation
    '''

    def __init__(self, div_id, db):
        self.db = db
        self.div_id = div_id
        self.div_url = self.getDivInfo()[0]
        self.scanned = self.getDivInfo()[1]
        self.site_url = self.getSiteInfo()

        self.current_url = self.div_url
        if self.scanned == 0:
            self.current_page = BeautifulSoup(getPage(self.div_url), "lxml")

        self.list_feature = None
        self.count = 0

    def getDivInfo(self):
        sql = "SELECT div_url, scanned FROM t_divs WHERE div_id = '" + \
            str(self.div_id) + "'"
        return self.db.queryBySQL(sql)[0]

    def getSiteInfo(self):
        pattern = re.compile(r'(http(?:s)?://.+?)/', re.S)
        return re.findall(pattern, self.div_url)[0]

    # locate the tag node feature of post list, and the url for next page
    def locatePostList(self):
        self.list_feature = "box list channel"

    def processPostList(self):
        div = self.current_page.find(class_=self.list_feature)
        a_set = div.find('ul').find_all('a')
        for a in a_set:
            post_name = a.text
            post_url = self.site_url + a['href']
            post_date = self.getDate(post_name)
            safeExec(self.savePost, post_name, post_url, post_date)

    def savePost(self, post_name, post_url, post_date=None):
        try:
            self.db.add(self.db.posts, post_name=post_name,
                        post_url=post_url, post_date=post_date,
                        scanned=False, div_id_fk=self.div_id)
            self.count += 1
        except sqlalchemy.exc.IntegrityError:
            printWarning(post_url + " already exists!")

    def getDate(self, post_name):
        pattern = re.compile('\d\d-\d\d', re.S)
        return re.findall(pattern, post_name)[0]

    def getNextPage(self):
        a = self.current_page.find('a', text='下一页')
        if a is not None and self.site_url + a['href'] != self.current_url:
            self.current_url = self.site_url + a['href']
            current_page = getPage(self.current_url)
            self.current_page = BeautifulSoup(current_page, "lxml")
            printSuccess('current_page: ' + self.current_url)
            return True
        else:
            printSuccess('reach the end!')
            return False

    def start(self):
        # if the div is already scanned
        if self.scanned == 1:
            printWarning("the div is already scanned " + self.div_url)
            return
            
        self.locatePostList()
        self.processPostList()
        while self.getNextPage():
            self.processPostList()
        printSuccess("done!" + str(self.count) + " posts fetched")
        self.db.scan(self.db.divs, self.db.divs.c.div_id, self.div_id)
