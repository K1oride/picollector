# coding=utf-8
'''
Created on Aug 21, 2016

@author: Charlie
'''

from downloader.DownloadHelper import downloadPost, mkdir
from utils.DBUtils import DBSupport, showSiteList
from utils.GeneralUtils import *
from utils.GeneralUtils import printSuccess

def start():
    db = DBSupport()
    showSiteList(db)
    selectByNum("Enter number to select site you want to download from: ",
                 showDivList, db)
    div_id = selectByNum("Enter number to select div you want to download from: ",
                         lambda x: x)
    selectRange("Enter start index: ", "Enter end Index: ",
                startDownload, db, div_id)

def showDivList(site_id, db):
    div_list = db.queryBySQL("SELECT div_id, div_name, scanned FROM t_divs"\
                             + " WHERE site_id_fk='" + str(site_id) + "'")
    print '{:>3}  {:<20} {}'.format("id", "name", "scanned")
    for div in div_list:
        div_id, div_name, scanned = div
        print ur'{:>3}: {:<20} {}   '.format(div_id, div_name, num2bool(scanned)),
        showDivInfo(div_id, db)
    
def showDivInfo(div_id, db):
    div_info = db.queryBySQL("SELECT count(*) FROM t_posts"\
                             + " WHERE div_id_fk='" + str(div_id) + "'")
    total_post = div_info[0][0]
    print "The div has " + str(total_post) + " posts"
    
def startDownload(start_index, end_index, db, div_id):
    printSuccess("download start")
    post_id_rows = db.queryBySQL("SELECT post_id FROM t_posts WHERE "\
                                 + "div_id_fk='" + str(div_id) + "'")
    post_id_list = [row.post_id for row in post_id_rows]
                            
    for post_id in post_id_list[start_index:end_index]:
        div_name = db.queryBySQL("SELECT div_name FROM t_divs"\
                                 + " WHERE div_id = '" + str(div_id) + "'")[0][0]
        post_name, post_date = db.queryBySQL("SELECT post_name, post_date FROM t_posts"\
                                             + " WHERE post_id = '" + str(post_id) + "'")[0]
        path = getDownloadPath() + div_name + ur"/" + post_date + ur"/" + post_name + ur"/"
        if mkdir(path):
            downloadPost(post_id, db, path)
    
    printSuccess("download finish!")    
