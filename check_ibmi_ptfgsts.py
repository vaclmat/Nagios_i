#!/QOpenSys/usr/bin/python3 

import config                  
from itoolkit import *      
import json                 

itool = iToolKit()                                                           
                                                                              
itool.add(iSqlQuery('si_ptfga_query',"Select GRP_CRNCY, GRP_ID, GRP_TITLE, GRP_LVL, GRP_IBMLVL, GRP_LSTUPD, GRP_RLS, GRP_SYSSTS from SYSTOOLS.GROUP_PTF_CURRENCY ORDER BY ptf_group_level_available - ptf_group_level_installed DESC"))
itool.add(iSqlFetch('si_ptfga_fetch'))
                                                                              
itool.add(iSqlFree('si_ptfga_free'))                                         
                                                                              
#xmlservice                                                                  
                                                                              
itool.call(config.itransport)                                                
                                                                              
#output     

PTFGRP_STATUS_INFO = itool.dict_out('si_ptfga_fetch') 
                                                       
if 'error' in PTFGRP_STATUS_INFO:                     
    print(PTFGRP_STATUS_INFO['error'])                 
    exit(2)                                            
else:                                                 
    #Determine state to pass to Nagios                 
    #CRITICAL = 2                                      
    #WARNING = 1                                       
    #OK = 0                                            
    js = PTFGRP_STATUS_INFO['row']                     
    data = json.dumps(js)                              
    count = data.count('GRP_ID')                                              
    #print("Count=" + str(count))                                             
    #print("Data=" + data)                                                    
    if (count == 1):                                                          
        if js['GRP_CRNCY'] == 'UPDATE AVAILABLE' :                             
           print("PTG GROUP STATUS IS WARNING: PTF GROUP " + js['GRP_TITLE'] + " has IBM level " + js['GRP_IBMLVL'] + " versus installed level " + js['GRP_LVL'] + ". ")                                                                 
           exit(1)                                                             
    else:                                                                     
        i = 0                                                                  
        status=0                                                               
        statustxt='OK'                                                         
        s=""                                                                   
        #print("Count=" + str(count))                                          
                                                                              
        while (i != count) :                                                   
          #print("I =" + str(i))                                              
          #print("PTF GROUP "  + js[i]['GRP_TITLE'] + " has status " + js[i]['GRP_CRNCY'] )                                                                
          if js[i]['GRP_CRNCY'] == 'UPDATE AVAILABLE' :                       
             print("PTF GROUP "  + js[i]['GRP_TITLE'])                       
             subs="PTF GROUP " + js[i]['GRP_TITLE'] + " has IBM level " + js[i]['GRP_IBMLVL'] + " versus installed level " + js[i]['GRP_LVL'] + "., "      
             s = s + subs                                                     
             status=1                                                         
             statustxt='WARNING'
          i += 1                                               
                                                             
        print("PTF GROUP STATUS IS " + statustxt + ": " + s)    
        if status == 1 :                                        
          exit(1)                                               
        else:                                                   
          exit(0)