'''
Created on Aug 19, 2016

@author: Charlie
'''

from sqlalchemy import *
from utils.GeneralUtils import num2bool

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class DBSupport(object):
    
    def __init__(self):
        with open("config/db.txt") as f:
            dbAccess = f.read()
        self.engine = create_engine(dbAccess, pool_recycle=3600)
        self.metadata = MetaData()
        self.sites = Table('t_sites', self.metadata,
                           Column('site_id', Integer, primary_key=True),
                           Column('site_url', String(50), unique=True, nullable=False),
                           Column('scanned', Boolean),
                           Column('keyword_found', String(20)))
        self.div_pool = Table('t_div_pool', self.metadata,
                              Column('div_id', Integer, primary_key=True),
                              Column('div_name', String(20), unique=True, nullable=False))
        self.divs = Table('t_divs', self.metadata,
                           Column('div_id', Integer, primary_key=True),
                           Column('div_name', String(20), nullable=False),
                           Column('div_url', String(50), nullable=False, unique=True),
                           Column('scanned', Boolean),
                           Column('site_id_fk', ForeignKey('t_sites.site_id')))
        self.posts = Table('t_posts', self.metadata,
                           Column('post_id', Integer, primary_key=True),
                           Column('post_name', String(200), nullable=False),
                           Column('post_url', String(50), nullable=False, unique=True),
                           Column('post_date', String(10)),
                           Column('scanned', Boolean),
                           Column('div_id_fk', ForeignKey('t_divs.div_id')))
        self.pics = Table('t_pics', self.metadata,
                          Column('pic_id', Integer, primary_key=True),
                          Column('pic_url', String(150), nullable=False),
                          Column('downloaded', Boolean),
                          Column('post_id_fk', ForeignKey('t_posts.post_id')))
        self.metadata.create_all(self.engine)
     
    def add(self, table, **kw):
        ins = insert(table).values(kw)
        with self.engine.connect() as conn:
            result = conn.execute(ins)
        return result

    def queryBySQL(self, sql):
        with self.engine.connect() as conn:
            result = conn.execute(sql).fetchall()
        return result
    
    def scan(self, table, id_col, uid):
        u = update(table).values(scanned=True).where(id_col == uid)
        with self.engine.connect() as conn:
            conn.execute(u)

def showSiteList(db):
    sites = db.queryBySQL('SELECT site_id, site_url, scanned FROM t_sites')
    print "Currently avaliable sites:"
    print "{:>3}  {:<40} {}".format("id", "url", "scanned")
    for site in sites:
        print "{:>3}: {:<40} {}".format(site[0], site[1], num2bool(site[2]))
               