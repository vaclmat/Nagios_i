#!/QOpenSys/usr/bin/python3

import config                                                                                                                       
from itoolkit import *                                                                                                              
import json                                                                                                                         
                                                                                                         
itool = iToolKit()                                                                                                                  
itool.add(iSqlQuery('si_sasp_query',"select SYS_STG, AUX_STG, SYS_RATE from QSYS2.SYSTEM_STATUS_INFO"))
itool.add(iSqlFetch('si_sasp_fetch'))                                                                                                
itool.add(iSqlFree('si_sasp_free'))                                                                                                  
#xmlservice                                                                                                                         
itool.call(config.itransport)                                                                                                       
#output 
SYSTEM_ASP_INFO = itool.dict_out('si_sasp_fetch')                                                                                 
if 'error' in SYSTEM_ASP_INFO:                                                                                                   
   print(SYSTEM_ASP_INFO['error'])                                                                                               
else:                                                                                                                               
   #Determine state to pass to Nagios
   #CRITICAL = 2
   #WARNING = 1
   #OK = 0
   if float(SYSTEM_ASP_INFO['row']['SYS_RATE']) > 90:
      print("SYSTEM ASP IS IN CRITICAL STATUS: System ASP capacity: " +  SYSTEM_ASP_INFO['row']["SYS_STG"] + ", Auxilary capacity: " + SYSTEM_ASP_INFO['row']["AUX_STG"] + ", System ASP Rate: " + SYSTEM_ASP_INFO['row']['SYS_RATE'] + ".| System ASP Rate=" + SYSTEM_ASP_INFO['row']['SYS_RATE'] + ";80;100;")
      exit(2)
   elif float(SYSTEM_ASP_INFO['row']['SYS_RATE']) > 80:
      print("SYSTEM ASP IS IN WARNING STATUS: ConfigSystem ASP capacity: " +  SYSTEM_ASP_INFO['row']["SYS_STG"] + ", Auxilary capacity: " + SYSTEM_ASP_INFO['row']["AUX_STG"] + ", System ASP Rate: " + SYSTEM_ASP_INFO['row']['SYS_RATE'] + ".| System ASP Rate=" + SYSTEM_ASP_INFO['row']['SYS_RATE'] + ";80;100;")
      exit(1)
   else:
      print("SYSTEM ASP IS IN OK STATUS: System ASP capacity: " +  SYSTEM_ASP_INFO['row']["SYS_STG"] + ", Auxilary capacity: " + SYSTEM_ASP_INFO['row']["AUX_STG"] + ", System ASP Rate: " + SYSTEM_ASP_INFO['row']['SYS_RATE'] + ".| System ASP Rate=" + SYSTEM_ASP_INFO['row']['SYS_RATE'] + ";80;100;")
      exit(0)