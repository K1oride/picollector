'''
Created on Aug 19, 2016

@author: Charlie
'''
import string
import exceptions

from utils.DBUtils import DBSupport, showSiteList
from utils.GeneralUtils import num2bool, safeExec
from spiders.DivSpider import DivSpider
from spiders.PostSpider import PostSpider
from spiders.PicSpider import PicSpider


def start():
    showStatus()
    r = raw_input("Enter number to fetch site or enter nothing to fetch keywords: ")
    if r == "":
        initSiteSpider()
    else:
        try:
            processSite(string.atoi(r))
        except exceptions.ValueError:
            print "invalid input!"

def showStatus():
    db = DBSupport()
    showSiteList(db)
    
def initSiteSpider():
    print "feature to be added"

def processSite(site_id):
    db = DBSupport()
    safeExec(DivSpider(site_id=site_id, db=db).start)
    div_id_list = db.queryBySQL("SELECT div_id FROM t_divs WHERE site_id_fk='" + str(site_id) + "'")
    
    for div_id_tuple in div_id_list:
        div_id = div_id_tuple[0]
        safeExec(PostSpider(div_id, db).start)
        
        post_id_list = db.queryBySQL("SELECT post_id FROM t_posts WHERE div_id_fk='" + str(div_id) + "'")
        for post_id_tuple in post_id_list:
            post_id = post_id_tuple[0]
            safeExec(PicSpider(post_id, db).start)
            
    
