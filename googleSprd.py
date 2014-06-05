'''
Created on 11/apr/2014

@author: i'm Developer
'''

import gdata.spreadsheet.service
import threading
import Queue
import datetime


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
        self.__spr_client.debug = False
        self.__spr_client.email = GSpread.__email
        self.__spr_client.password = GSpread.__password 
        self.__spr_client.source = 'Tracer spreadsheet'
        self.__spr_client.ProgrammaticLogin()
        self.spreadsheet_key = GSpread.__sprdKey
        
        #defualt worksheet, should be mapped with the ccid            
        self.worksheet_id = 'od6'
        
        
    def _publish_row_thread(self):
        msg = self.__msgQueue.get()
        #self.__spr_client.InsertRow(msg.getDict(), key=self.spreadsheet_key, wksht_id=self.worksheet_id)
        
        #print "Row to be submitted " + msg
        self.__spr_client.InsertRow(msg, key=self.spreadsheet_key, wksht_id=self.worksheet_id)
                
        #print("Row submitted:")
        #msg.printD()
        
        self.__msgQueue.task_done()    
    
    def run(self):
        while True:            
            self._publish_row_thread()
            
    def publishMsg(self, msg):
        self.__msgQueue.put_nowait(msg)

 
    
def initGS():
    gs = GSpread("89372021131217026926")
    return gs 
    
    
if __name__ == "__main__":
    #testPublish2()
    
    pass



# cDate = "date"
# #cCcid = "CCID"
# cEvent = "Event"
# cError = "Error"
# 
# class GMsg():    
#     def __init__(self, date, event, error=""):
#         self.__row={}
#         self.__row[cDate]=date
#  #       self.__row[cCcid]=ccid
#         self.__row[cEvent]=event
#         self.__row[cError]=error
# 
#     def printD(self):
#         str (self.__row)
#     
#     def getDict(self):
#         return self.__row
# 
# def testPublish():
#     print("Start test Publish on Google")
#     gs = GSpread("89372021131217026926") 
#     print("Creating msg to publisg")
#     gM = GMsg(datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S"), "Activation", "Ok")
#     gM.printD()
#     print("Now will be published..")
#     gs.publishMsg(gM)
# 
# 
# def testPublish2():
#     print("Start test Publish on Google")
#     gs = GSpread("89372021131217026926") 
#     print("Creating msg to publisg")
#     d = {}
#     d[cDate]= "test1"
#     d[cEvent]= "test2"
#     
#     print("Now will be published..")
#     gs.publishMsg(d)            