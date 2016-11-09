#!/QOpenSys/usr/bin/python3                                                                                                               
                                                                                                                                    
"""Calculate transfer bytes on XSM line."""                                                                                         
                                                                                                                                    
import config                                                                                                                       
from itoolkit import *                                                                                                              
import json                                                                                                                         
from mysql_db_cls import p_mysql_db                                                                                                 
#import pymysql                                                                                                                     
                                                                                                                                    
def jdefault(o):                                                                                                                    
   return o.__dict__                                                                                                                
                                                                                                                                    
def sqlcmd():                                                                                                                       
   itool = iToolKit()                                                                                                               
   itool.add(iSqlQuery('si_netstat_query',"SELECT RMT_PORT, LOCAL_PORT, BYTES_OUT, BYTES_IN, CT_RETRANS FROM QSYS2.NETSTAT_INFO WHERE REMOTE_ADDRESS='192.168.55.1'"))
   itool.add(iSqlFetch('si_netstat_fetch'))                                                                                         
   itool.add(iSqlFree('si_netstat_free'))
   #xmlservice                                             
   itool.call(config.itransport)                           
   #output                                                 
   SYSTEM_STATUS_INFO = itool.dict_out('si_netstat_fetch') 
   if 'error' in SYSTEM_STATUS_INFO:                       
      return SYSTEM_STATUS_INFO['error']                   
   else:                                                   
       return SYSTEM_STATUS_INFO['row']                    
                                                           
def inssqlcmd(a):                                          
   global b                                                
   global c                                                
   global d                                                
   global e                                                
   global f                                                
                                                           
   db = p_mysql_db()                                       
   try:
      db.cursor.execute("UPDATE NETSTAT_INFO SET  LOCAL_PORT = %s, REMOTE_PORT = %s, BYTES_IN = %s, BYTES_OUT = %s, CT_RETRANS = %s WHERE ID = %s",(b,c,d,e,f,a))
      db.conn.commit()                                                                             
   except:                                                                                         
      db.conn.rollback()                                                                           
                                                                                                   
   db.close()                                                                                      
                                                                                                   
def rtvsqlcmd(g):                                                                                  
                                                                                                   
   db = p_mysql_db()                                                                               
   try:                                                                                            
      db.cursor.execute("SELECT local_port, remote_port, bytes_in, bytes_out, ct_retrans FROM netstat_info WHERE id = %s ",(g))
      data = db.cursor.fetchone()                                                                  
      return data                                                                                  
   except:                                                                                         
      return 'error'                                                                               
                                                                                                   
   db.close()
   
result = sqlcmd()                   
#print(result)                      
                                    
                                    
if result != '*** error stmt1':     
   olddata1 = rtvsqlcmd(g = 1)      
   #print(olddata1)                 
   olddata2 = rtvsqlcmd(g = 2)      
   #print(olddata2)                 
   b = int(result[0]['LOCAL_PORT']) 
   c = int(result[0]['RMT_PORT'])   
   d = int(result[0]['BYTES_IN'])   
   e = int(result[0]['BYTES_OUT'])  
   f = int(result[0]['CT_RETRANS']) 
   newdata1 = inssqlcmd(a = 1)      
   #print(newdata1)                 
   b = int(result[1]['LOCAL_PORT']) 
   c = int(result[1]['RMT_PORT'])                    
   d = int(result[1]['BYTES_IN'])                    
   e = int(result[1]['BYTES_OUT'])                   
   f = int(result[1]['CT_RETRANS'])                  
   newdata2 = inssqlcmd(a = 2)                       
   #print(newdata2)                                  
   if result[0]['RMT_PORT'] == result[1]['RMT_PORT']:
      #print("Source location")                      
      cbi = int(result[1]['BYTES_OUT']) - olddata2[3]
      print("NETSTAT OK: " + str(cbi) + " bytes sent remotely, |Bytes sent remotely= " + str(cbi) + ";500000;800000;")                        
   else:                                             
      #print("Target location")                      
      cbi = int(result[0]['BYTES_IN']) - olddata1[2] 
      print("NETSTAT OK: " + str(cbi) + " bytes received locally, |Bytes received locally=" + str(cbi) + ";500000;800000;")                        
else:                                                
   #print("Error in downloading data.")              
   print("NETSTAT CRITICAL : Error in downloading data")                                         