#!/QOpenSys/usr/bin/python3                                                                                                                           
                                                                                                                                   
"""Sign on failed attempts check."""                                                                                               
                                                                                                                                   
import configfpu                                                                                                                   
from itoolkit import *                                                                                                             
import json                                                                                                                        
from collections import Counter                                                                                                    
                                                                                                                                   
def sqlcmd():                                                                                                                      
   itool = iToolKit()                                                                                                              
   itool.add(iSqlQuery('ss_ufa_query',"SELECT USER_NAME, SIGNONINV, PRVSIGNON FROM QSYS2.USER_INFO WHERE SIGN_ON_ATTEMPTS_NOT_VALID > 0"))
   itool.add(iSqlFetch('ss_ufa_fetch'))                                                                                            
   itool.add(iSqlFree('ss_ufa_free'))                                                                                              
   #xmlservice                                                                                                                     
   itool.call(configfpu.itransport)                                                                                                
   #output                                                                                                                         
   SYSTEM_USER_INFO = itool.dict_out('ss_ufa_fetch')
   if 'error' in SYSTEM_USER_INFO:                                                             
      return SYSTEM_USER_INFO['error']                                                         
   else:                                                                                       
       return SYSTEM_USER_INFO                                                                 
                                                                                               
result = sqlcmd()                                                                              
if 'error' in result:                                                                          
   #print("Error in downloading data.")                                                        
   print("SIGNON ATTEMPTS OK: There is no unsuccessful attempt to signon system.")
   exit(0)
else:                                                                                          
   js = result['row']                                                                          
   #print(js)                                                                                  
   data = json.dumps(js)                                                                       
   count = data.count('USER_NAME')

   if (count == 1):
      if float(js['SIGNONINV']) > 2 :
         print("SIGNON ATTEMPTS CRITICAL: User " + js['USER_NAME'] + "attempts " + js['SIGNONINV'] + "unsuccessfully signon (last attempt " + js['PRVSIGNON'] + " ). ")
         exit(2)
      else:
          print("SIGNON ATTEMPTS WARNING: User " + js['USER_NAME'] + "attempts " + js['SIGNONINV'] + "unsuccessfully signon (last attempt " + js['PRVSIGNON'] + " ). ")
          exit(1)
          
   else:                                                                                       
      i = 0 
      status=1   
      statustxt=WARNING
      #print(str(count) + ':')                                                              
      while (i != count) :
         subs="User " + js[i]['USER_NAME'] + " attempts " + js[i]['SIGNONINV'] + "x unsuccessfully signon (last attempt " + js['PRVSIGNON'] + " ). "
         str = str + subs
         #print(js[i]['USER_NAME'] + ':' + js[i]['SIGNONINV'] + ':' + js['PRVSIGNON'] + ':')
         if float(js[i]['SIGNONINV']) > 2 :                                       
              status=2                                                                         
              statustxt=CRITICAL
              
         i += 1
         
      print("SIGNON ATTEMPTS " + statustxt + ": " + str)
      if status == 2 :
        exit(2)
      else:
        exit(1)