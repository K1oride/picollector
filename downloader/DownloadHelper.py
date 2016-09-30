# coding=utf-8
'''
Created on Aug 19, 2016

@author: Charlie
'''
import os
import re

import requests

from utils.GeneralUtils import printSuccess, printWarning

def downloadPost(post_id, db, path=""):
    sql = "SELECT DISTINCT(pic_url) FROM t_pics WHERE post_id_fk = '" + str(post_id) + "'"
    pics = db.queryBySQL(sql)
    for i, pic in enumerate(pics):
        pic_url = pic[0]
        downloadPic(pic_url, path, "img_" + str(i) + getSufFromURL(pic_url))

def downloadPic(pic_url, path, filename):
    r = requests.get(pic_url)
    with open(path + filename, "wb") as pic:
        pic.write(r.content)
    printSuccess(filename + " downloaded!")

def getSufFromURL(url):
    pattern = re.compile('(\..{3,4})$', re.S)
    return re.findall(pattern, url)[0]

def mkdir(path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            # 如果不存在则创建目录
            printSuccess(u"偷偷新建了名字叫做 " + path + u' 的文件夹')
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            printWarning(u"名为 " + path + u'的文件夹已经存在')
            return False
