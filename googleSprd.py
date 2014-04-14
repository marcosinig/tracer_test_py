'''
Created on 11/apr/2014

@author: i'm Developer
'''

import gdata.spreadsheet.service
import threading
import Queue
import datetime


cDate = "date"
#cCcid = "CCID"
cEvent = "Event"
cError = "Error"

class GMsg():    
    def __init__(self, date, event, error=""):
        self.__row={}
        self.__row[cDate]=date
 #       self.__row[cCcid]=ccid
        self.__row[cEvent]=event
        self.__row[cError]=error

    def printD(self):
        str (self.__row)
    
    def getDict(self):
        return self.__row
    

class GSpread(threading.Thread):
    __email = 'xperiatimspa@gmail.com'
    __password =  '5xerqtjy'    
    __sprdKey = '0AgpyaIjVpPvrdGJDVkdBZGM2UW1pVHNnZlllazRHNlE'
    
    '''
    classdocs
    '''
    def __init__(self, ccid):
        super(self.__class__, self).__init__()
        self.__msgQueue = Queue.Queue()
        self.__ccid = ccid
        self.start()
        
        self.__spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        self.__spr_client.debug = True
        self.__spr_client.email = GSpread.__email
        self.__spr_client.password = GSpread.__password 
        self.__spr_client.source = 'Tracer spreadsheet'
        self.__spr_client.ProgrammaticLogin()
        self.spreadsheet_key = GSpread.__sprdKey
        
        #defualt worksheet, should be mapped with the ccid            
        self.worksheet_id = 'od6'
        
        
    def publish_row_thread(self):
        msg = self.__msgQueue.get()
        self.__spr_client.InsertRow(msg.getDict(), key=self.spreadsheet_key, wksht_id=self.worksheet_id)
        if self.log==1:
            print("Row submitted:")
            msg.printD()
        msg.task_done()    
    
    def run(self):
        while True:            
            self.publish_row_thread()
            
    def publishMsg(self, msg):
        self.__msgQueue.put_nowait(msg)

def testPublish():
    print("Start test Publish on Google")
    gs = GSpread("89372021131217026926") 
    print("Creating msg to publisg")
    gM = GMsg(datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S"), "Activation", "Ok")
    gM.printD()
    print("Now will be published..")
    gs.publishMsg(gM)
    
if __name__ == "__main__":
    testPublish()
    pass


        