'''
Created on Aug 19, 2016

@author: Charlie
'''


class SiteSpider(object):
    '''
    this spider is used to fetch site url based on google search result with keywords in keywords pool 
    the search result is carefully analyzed
    '''

    def __init__(self, db):
        self.db = db
        