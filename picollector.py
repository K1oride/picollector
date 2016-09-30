# coding=utf-8
'''
Created on Aug 19, 2016

@author: Charlie
'''

import sys, getopt

import downloader.Downloader as downloader
import scheduler.Scheduler as scheduler
from utils.GeneralUtils import *


def main():

    usage = '''
    Usage:
        -h --help show this message
        -f --fetch enter fetch-mode
        -d --download enter download-mode
        -p --path= set/show download path
        --dbconfig= set/show database config string

    '''
    shortopts = "hfdpp:"
    longopts = ["help", "path=","dbconfig=", "fetch", "download"]
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
    except getopt.GetoptError:
        print usage
        sys.exit(0)

    for op, value in opts:
        if op in ("-h", "--help"):
            print usage
            sys.exit(0)
        elif op in ("-f", "--fetch"):
            safeExec(scheduler.start)
        elif op in ("-d", "--download"):
            safeExec(downloader.start)
        elif op in ("-p", "--path"):
            setRshow(value, setDownloadPath, showDownloadPath)
        elif op in ("--dbconfig"):
            setRshow(value, setDBConfig, showDBConfig)

if __name__ == '__main__':
    main()
