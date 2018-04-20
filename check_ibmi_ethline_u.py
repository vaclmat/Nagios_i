#!/QOpenSys/usr/bin/python3                                                                                                               
                                                                                                                                    
"""Calculate transfer bytes on ETHLINE line."""                                                                                         
                                                                                                                                    
import config                                                                                                                       
from itoolkit import *                                                                                                              
import json
import ibm_db                                                                                                                        
#from mysql_db_cls import p_mysql_db                                                                                                 
#import pymysql                                                                                                                     
                                                                                                                                    
def jdefault(o):                                                                                                                    
   return o.__dict__    
   
def uniq(input1,input2):                
   global l_fco,r_fco                  
   if input1 not in l_output:      
      l_output.append(input1)
      l_fco += 1
   if input2 not in r_output:      
      r_output.append(input2)
      r_fco += 1
                                                                                                                                    
def sqlcmd():                                                                                                                       
   itool = iToolKit()                                                                                                               
   itool.add(iSqlQuery('si_netstat_query',"SELECT RMT_PORT, LOCAL_PORT, BYTES_OUT, BYTES_IN, CT_RETRANS FROM QSYS2.NETSTAT_INFO WHERE LOCAL_ADDRESS='192.168.100.51'"))
   itool.add(iSqlFetch('si_netstat_fetch'))                                                                                         
   itool.add(iSqlFree('si_netstat_free'))
   #xmlservice                                             
   itool.call(config.itransport)                           
   #output                                                 
   SYSTEM_STATUS_INFO = itool.dict_out('si_netstat_fetch') 
   if 'error' in SYSTEM_STATUS_INFO:                       
      return SYSTEM_STATUS_INFO['error']                   
   else:                                                   
       return SYSTEM_STATUS_INFO                    
                                                           
def inssqlcmd():                                          
   global id                                                
   global bi                                                
   global bo 
   #print("ID: " + str(id) + ", BI: " + str(bi) + ", BO: " + str(bo) + ".")
   itool = iToolKit(iparm=1)                                                                                                               
   itool.add(iSqlPrepare('netstat_info_prep', "UPDATE NAGIOS.NETSTAT_INFO SET BYTES_IN=?, BYTES_OUT=? WHERE ID=?"))
   itool.add(iSqlExecute('netstat_info_exec')
    .addParm(iSqlParm('pm1',str(bi)))
    .addParm(iSqlParm('pm2',str(bo)))
    .addParm(iSqlParm('pm3',str(id)))
    )
   itool.add(iSqlFetch('netstat_info_fetch'))
   itool.add(iSqlFree('netstat_info_free'))
   
   #xmlservice                                             
   itool.call(config.itransport)                           
   #output                                                 
   NETSTAT_INFO_U = itool.dict_out('netstat_info_fetch') 
   if 'error' in NETSTAT_INFO_U:                       
      return NETSTAT_INFO_U['error']                   
   else:                                                   
       return NETSTAT_INFO_U                                    
      
   
                                                                                                   
def rtvsqlcmd():                                                                                  
                                                                                                   
   
   itool = iToolKit()                                                                                                               
   itool.add(iSqlQuery('si_netstat_info_query',"SELECT * FROM NAGIOS.NETSTAT_INFO WHERE ID=2"))
   itool.add(iSqlFetch('si_netstat_info_fetch'))                                                                                         
   itool.add(iSqlFree('si_netstat_info_free'))
   #xmlservice                                             
   itool.call(config.itransport)                           
   #output                                                 
   NETSTAT_INFO = itool.dict_out('si_netstat_info_fetch') 
   if 'error' in NETSTAT_INFO:                       
      return NETSTAT_INFO['error']                   
   else:                                                   
       return NETSTAT_INFO['row']
   
result = sqlcmd()                   
#print(result) 
if 'error' in result:                                                                                                                                                     
      print("Communication bandwith UNKNOWN: Plugin error." + result)                      
                                                
else:                                           
   js = result['row']                           
   data = json.dumps(js)                        
   count = data.count('BYTES_IN')     
   #print("Count=" + str(count))                
   #print("Data=" + data)                       
   i = 0                                        
   rx = 0
   tx = 0
   l_fco = 0 
   r_fco = 0
   l_output = []
   r_output = []
   l_ports = ''
   r_ports = ''
   if count == 1 :                              
      rx = int(js['BYTES_IN'])
      tx = int(js['BYTES_OUT']) 
      l_ports = js['LOCAL_PORT'] 
      r_ports = js['RMT_PORT']
      uniq(l_ports,r_ports)
   else:                                
     while (i < count):                 
        rx = int(js[i]['BYTES_IN']) + rx
        tx = int(js[i]['BYTES_OUT']) + tx
        l_ports = js[i]['LOCAL_PORT']
        r_ports = js[i]['RMT_PORT']
        uniq(l_ports,r_ports)
        i += 1

     #print ("RX=" + str(rx))
     #print ("TX=" + str(tx))
     #print ("Communication on local ports:" + str(l_output))
     #print ("Communication on remote ports:" + str(r_output))
     #olddata2 = rtvsqlcmd()      
     #print(olddata2)
     #bi = int(olddata2['BYTES_IN'])
     #bo = int(olddata2['BYTES_OUT'])
     #id = 1
     #rxf = rx - bi
     #txf = tx - bo
     #result = inssqlcmd()
     #print(result)
     #bi = rx
     #bo = tx
     #id = 2
     #result = inssqlcmd()
     #print(result)
     print("NETSTAT OK: BYTES_IN =" + str(rx) + ", BYTES_OUT = " + str(tx) + " on local ports: " + str(l_output) + ", on remote ports: " + str(r_output) + ". | BYTES_IN = " + str(rx) + ", BYTES_OUT = " + str(tx) )
'''                                    
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
   print("NETSTAT CRITICAL : Error in downloading data") '''                                        
