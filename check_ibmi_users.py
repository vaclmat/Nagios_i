#!/QOpenSys/usr/bin/python3                       
                                
"""Number of logged users"""    
                                
import config                   
from itoolkit import *          
import json                     
from collections import Counter 
                                
                                
def uniq(input):                
   global fco                   
   if input not in output:      
      output.append(input)      
      fco += 1                  
                                
                                
def jdefault(o):                
   return o.__dict__                                                                                                                
                                                                                                                                    
def sqlcmd():                                                                                                                       
   itool = iToolKit()                                                                                                               
   itool.add(iSqlQuery('si_users_query',"select AUTHORIZATION_NAME from TABLE(QSYS2.ACTIVE_JOB_INFO('NO', '','','')) AS X where JOB_TYPE='INT'"))
   itool.add(iSqlFetch('si_users_fetch'))                                                                                           
   itool.add(iSqlFree('si_users_free'))                                                                                             
   #xmlservice                                                                                                                      
   itool.call(config.itransport)                                                                                                    
   #output                                                                                                                          
   ACTIVE_USERS = itool.dict_out('si_users_fetch')                                                                                  
   if 'error' in ACTIVE_USERS:                                                                                                      
      return ACTIVE_USERS['error']                                                                                                  
   else:                                                                                                                            
       return ACTIVE_USERS                                                                                                          
                                                                                                                                    
result = sqlcmd()                                                                                                                   
if 'error' in result:                                                                                                               
   if result == '*** error stmt1' :             
      print("Active users OK: 0 users currently logged in 0 sessions.|Active users: 0;80;100;")                   
   else:                                        
      print("Active users UNKNOWN: Plugin error." + result)                      
                                                
else:                                           
   js = result['row']                           
   data = json.dumps(js)                        
   count = data.count('AUTHORIZATION_NAME')     
   #print("Count=" + str(count))                
   #print("Data=" + data)                       
   i = 0                                        
   s = ''                                       
   fco = 0                                      
   output = []                                  
   if count == 1 :                              
      s = js['AUTHORIZATION_NAME']              
      uniq(s)                                   
   else:                                
     while (i < count):                 
        s = js[i]['AUTHORIZATION_NAME'] 
        uniq(s)                         
        i += 1                          
                                        
   #print(s)                            
                                        
   #uniq(s,fco)                         
   #print(output)
   if fco > 100:
      print("Active users CRITICAL: " + str(fco) + " users currently logged in " + str(count) + " sessions.|Active users: " + str(fco) + ";80;100;")  
      exit(2)
   elif fco > 80:
      print("Active users WARNING: " + str(fco) + " users currently logged in " + str(count) + " sessions.|Active users: " + str(fco) + ";80;100;")
      exit(1)
   else:
      print("Active users OK: " + str(fco) + " users currently logged in " + str(count) + " sessions.|Active users: " + str(fco) + ";80;100;")
      exit(0)
  