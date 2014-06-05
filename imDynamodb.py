'''
Created on Jun 4, 2014

@author: marco
'''

import boto
#from boto.dynamodb2.table import Table
from boto.dynamodb.table import Table
import googleSprd


import datetime

AWS_ACCESS_KEY_ID = "AKIAJD6DQEJGVLX6D2YA"
SECRET_ACCESS_KEY = "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"

table = 'test-imhere-positions-2014-6'

#140605112027
STR_FORMAT = "%y%m%d%H%M"


def queryByDate(iccid, date_from, date_to):
    print boto.Version    
    
    filter_items = []
    
    conn = boto.connect_dynamodb( aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)    
    im_table = conn.get_table(table)
        
    items = im_table.query( iccid )
    
        
    for item in items:
        if item["datetime"] >= date_from and item["datetime"] <= date_to :
            filter_items.append(item) 
    
    return filter_items


if __name__ == '__main__':
    iccid = "89372021131217025480"
    date_from = "140605100649"
    date_to = "140605120823"
            
    results = queryByDate(iccid, date_from, date_to)
            
    gdict = {}
    gs = googleSprd.initGS()
    
    for item in results:
    #    print item
        dic = item.__dict__
        for k in dic["_updates"]:
            gdict[k]=dic["_updates"][k][1]
        gs.publishMsg(gdict.copy())
        
        print gdict
        gdict.clear()
    
    print "END"
    