# coding=utf-8
'''
Created on Aug 19, 2016

@author: Charlie
'''
from bs4 import BeautifulSoup

import re
import sqlalchemy

from utils.GeneralUtils import getPage, printWarning, printSuccess


class DivSpider(object):
    '''
    this spider aims to analysis index page of the site, find the navi bar,
    expand the div keyword dictionary, and save urls of all links for later user
    by PostSpider
    '''

    def __init__(self, site_id, db):
        self.db = db
        self.site_id = site_id
        self.site_url = self.getSiteInfo()[0]
        self.keyword = self.getSiteInfo()[1]
        self.scanned = self.getSiteInfo()[2]
        if self.scanned == 0:
            self.page = BeautifulSoup(getPage(self.site_url), "lxml")

    def getSiteInfo(self):
        sql = "SELECT site_url, keyword_found, scanned FROM t_sites WHERE site_id = '" + \
            str(self.site_id) + "'"
        return self.db.queryBySQL(sql)[0]

    def locateKeyword(self):
        pattern = re.compile(ur'.{0,5}' + self.keyword + ur'.{0,5}', re.S)
#         pattern = self.keyword
        return self.page.find('a', text=pattern)

    def locateNaviList(self):
        currentTag = 'a'
        target_unit = self.locateKeyword()
        # search the navigation bar until find the list structure
        while (target_unit.find_next_sibling(currentTag) == None or
               target_unit.find_previous_sibling(currentTag) == None):
            target_unit = target_unit.parent
            currentTag = target_unit.name
        return target_unit

    def processNaviList(self):
        target_unit = self.locateNaviList()
        navi_list = [target_unit]
        for item in target_unit.next_siblings:
            navi_list.append(item)
        for item in target_unit.previous_siblings:
            navi_list.append(item)

        for item in navi_list:
            if item != '\n':  # filter all '\n' nodes
                a = item.find('a')
                div_name = a.text.strip()
                div_url = self.site_url + a['href']
                self.expandDivPool(div_name)
                self.saveDiv(div_name, div_url)

    def saveDiv(self, div_name, div_url):
        try:
            self.db.add(self.db.divs, div_name=div_name,
                        div_url=div_url, site_id_fk=self.site_id,
                        scanned=False)
        except sqlalchemy.exc.IntegrityError:
            printWarning(div_url + ' already exists in divs')

    def expandDivPool(self, div_name):
        try:
            self.db.add(self.db.div_pool, div_name=div_name)
        except sqlalchemy.exc.IntegrityError:
            printWarning(div_name + ' already exists in div_pool')

    def start(self):
        if self.scanned == 1:
            printWarning("the site is already scanned " + self.site_url)
            return

        self.processNaviList()
        printSuccess(self.site_url + ' site division process done!')
        self.db.scan(self.db.sites, self.db.sites.c.site_id, self.site_id)
