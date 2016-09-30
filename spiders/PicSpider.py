# coding=utf-8
'''
Created on Aug 19, 2016

@author: Charlie
'''
from bs4 import BeautifulSoup
from utils.GeneralUtils import getPage, printWarning, printSuccess, safeExec

import sqlalchemy


class PicSpider(object):
    '''
    classdocs
    '''

    def __init__(self, post_id, db):
        self.db = db
        self.post_id = post_id
        self.post_url = self.getPostInfo()[0]
        self.scanned = self.getPostInfo()[1]

        self.page = None
        self.count = 0

    def getPostInfo(self):
        sql = "SELECT post_url, scanned FROM t_posts WHERE post_id = '" + \
            str(self.post_id) + "'"
        return self.db.queryBySQL(sql)[0]

    def getPicList(self):
        return self.page.find_all('img')

    def processPicList(self, pic_list):
        for pic in pic_list:
            pic_url = pic['src']
            self.savePic(pic_url)

    def savePic(self, pic_url):
        try:
            self.db.add(self.db.pics, pic_url=pic_url,
                        downloaded=False, post_id_fk=self.post_id)
            self.count += 1
        except sqlalchemy.exc.IntegrityError:
            printWarning(pic_url + " already exists!")

    def start(self):
        if self.scanned == 1:
            printWarning("the post is already scanned " + self.post_url)
            return
        else:
            self.page = BeautifulSoup(getPage(self.post_url), "lxml")

        self.processPicList(self.getPicList())
        printSuccess(self.post_url + "----" +
                     str(self.count) + ' pics fetched')
        self.db.scan(self.db.posts, self.db.posts.c.post_id, self.post_id)
