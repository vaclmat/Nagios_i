#!/QOpenSys/usr/bin/python3

import config                                                                                                                       
from itoolkit import *                                                                                                              
import json                                                                                                                         
                                                                                                         
itool = iToolKit()                                                                                                                  
itool.add(iSqlQuery('si_jobs_query',"SELECT TOTAL_JOBS_IN_SYSTEM, MAXIMUM_JOBS_IN_SYSTEM, ACTIVE_JOBS_IN_SYSTEM, INTERACTIVE_JOBS_IN_SYSTEM, ELAPSED_TIME FROM TABLE(QSYS2.SYSTEM_STATUS(RESET_STATISTICS=>'YES')) X"))
itool.add(iSqlFetch('si_jobs_fetch'))                                                                                                
itool.add(iSqlFree('si_jobs_free'))                                                                                                  
#xmlservice                                                                                                                         
itool.call(config.itransport)                                                                                                       
#output 
Active_jobs_INFO = itool.dict_out('si_jobs_fetch')                                                                                 
if 'error' in Active_jobs_INFO:                                                                                                   
   print(Active_jobs_INFO['error'])                                                                                               
else:                                                                                                                               
   #Determine state to pass to Nagios
   #CRITICAL = 2
   #WARNING = 1
   #OK = 0
   if float(Active_jobs_INFO['row']['ACTIVE_JOBS_IN_SYSTEM']) > 500:
      print("ACTIVE JOBS ARE IN CRITICAL STATUS: Active Jobs: " +  Active_jobs_INFO['row']["ACTIVE_JOBS_IN_SYSTEM"] + " | Active jobs = " + Active_jobs_INFO['row']["ACTIVE_JOBS_IN_SYSTEM"] + ";300;500;")
      exit(2)
   elif float(Active_jobs_INFO['row']['ACTIVE_JOBS_IN_SYSTEM']) > 300:
      print("ACTIVE JOBS ARE IN WARNING STATUS: Active Jobs: " +  Active_jobs_INFO['row']["ACTIVE_JOBS_IN_SYSTEM"] + " | Active jobs = " + Active_jobs_INFO['row']["ACTIVE_JOBS_IN_SYSTEM"] + ";300;500;")
      exit(1)
   else:
      print("ACTIVE JOBS ARE IN OK STATUS: Active Jobs: " +  Active_jobs_INFO['row']["ACTIVE_JOBS_IN_SYSTEM"] + " | Active jobs = " + Active_jobs_INFO['row']["ACTIVE_JOBS_IN_SYSTEM"] + ";300;500;")
      exit(0)