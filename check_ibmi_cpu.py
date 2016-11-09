#!/QOpenSys/usr/bin/python3

import config                                                                                                                       
from itoolkit import *                                                                                                              
import json                                                                                                                         
                                                                                                         
itool = iToolKit()                                                                                                                  
itool.add(iSqlQuery('si_cpu_query',"select CONFIGCPUS, CPU_CAP, CPU_RATE, CPU_MIN, CPU_AVG, CPU_MAX, CPU_SQL from QSYS2.SYSTEM_STATUS_INFO"))
itool.add(iSqlFetch('si_cpu_fetch'))                                                                                                
itool.add(iSqlFree('si_cpu_free'))                                                                                                  
#xmlservice                                                                                                                         
itool.call(config.itransport)                                                                                                       
#output 
SYSTEM_STATUS_INFO = itool.dict_out('si_cpu_fetch')                                                                                 
if 'error' in SYSTEM_STATUS_INFO:                                                                                                   
   print(SYSTEM_STATUS_INFO['error'])                                                                                               
else:                                                                                                                               
   #Determine state to pass to Nagios
   #CRITICAL = 2
   #WARNING = 1
   #OK = 0
   if float(SYSTEM_STATUS_INFO['row']['CPU_AVG']) > 90:
      print("CPU UTILIZATION IS IN CRITICAL STATUS: Configured CPUs: " +  SYSTEM_STATUS_INFO['row']["CONFIGCPUS"] + ", Configured CPU capacity: " + SYSTEM_STATUS_INFO['row']["CPU_CAP"] + ", CPU average: " + SYSTEM_STATUS_INFO['row']['CPU_AVG'] + ".|CPU average=" + SYSTEM_STATUS_INFO['row']['CPU_AVG'] + ";80;100;")
      exit(2)
   elif float(SYSTEM_STATUS_INFO['row']['CPU_AVG']) > 80:
      print("CPU UTILIZATION IS IN WARNING STATUS: Configured CPUs: " +  SYSTEM_STATUS_INFO['row']["CONFIGCPUS"] + ", Configured CPU capacity: " + SYSTEM_STATUS_INFO['row']["CPU_CAP"] + ", CPU average: " + SYSTEM_STATUS_INFO['row']['CPU_AVG'] + ".|CPU average=" + SYSTEM_STATUS_INFO['row']['CPU_AVG'] + ";80;100;")
      exit(1)
   else:
      print("CPU UTILIZATION IS IN OK STATUS: Configured CPUs: " +  SYSTEM_STATUS_INFO['row']["CONFIGCPUS"] + ", Configured CPU capacity: " + SYSTEM_STATUS_INFO['row']["CPU_CAP"] + ", CPU average: " + SYSTEM_STATUS_INFO['row']['CPU_AVG'] + ".|CPU average=" + SYSTEM_STATUS_INFO['row']['CPU_AVG'] + ";80;100;")
      exit(0)    