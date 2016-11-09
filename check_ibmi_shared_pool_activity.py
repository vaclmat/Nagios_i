#!/QOpenSys/usr/bin/python3                                                                                              
                                                                                                      
"""Shared memory pools activity.""" 
"""Warning criteria - Wait to Ineligible should not be more than 20% of your Active to Wait value"""
"""Critical criteria - Elapsed total faults for machine pool > 10, Transitions of threads from an active condition to an ineligible condition > 10 for all pools"""                                                                       
                                                                                                      
import config, sys                                                                                         
from itoolkit import *
from decimal import Decimal                                                                                
import json                                                                                           
                                                                                                      
                                                                   
itool = iToolKit()                                                                                    
itool.add(iSqlQuery('si_smpa_query',"select POOL_NAME, MAX_THREAD, CURR_THRD, INEL_THRD, ELAP_DBF, ELAP_NDBF, ELAP_TOTF, ELAP_DBP, ELAP_NDBP, ELAP_ATW, ELAP_WTI, ELAP_ATI from QSYS2.MEMORY_POOL_INFO"))
itool.add(iSqlFetch('si_smpa_fetch'))                                                                  
itool.add(iSqlFree('si_smpa_free'))                                                                    
#xmlservice                                                                                           
itool.call(config.itransport)                                                                         
#output
MEMORY_POOL_INFO = itool.dict_out('si_smpa_fetch')                                                                           
if 'error' in MEMORY_POOL_INFO:                                                                                             
   print(MEMORY_POOL_INFO['error'])                                                                                         
else:                                                                                                                         
   js = MEMORY_POOL_INFO['row']                      
   data = json.dumps(js)                   
   count = data.count('POOL_NAME')
   #print("Count=" + str(count))           
   #print("Data=" + data)                  
   i = 0                                   
   s = ''
   etotfbt = False
   eatibt = False
   ewtibeatw = False
   listomsp = []
   listwmsp = []
   while (i < count):                
      s = js[i]['POOL_NAME']
      
      #Count 20% of Active to Wait value
      result = float(js[i]['ELAP_ATW'])
      tpoatw = result / 5
      #print('20% of ATW = ' + str(tpoatw))
      #print('ELAP_WTI =' + js[i]['ELAP_WTI'])
      if (float(js[i]['ELAP_WTI']) > tpoatw):
          ewtibeatw = True
          listwmsp.append[s]
      
      #Elapsed total faults for machine pool > 10
      #print('Elapsed total faults for ' + s + ' = ' + js[i]['ELAP_TOTF'])
      if ((s == "*MACHINE") and (float(js[i]['ELAP_TOTF']) > 10)):
         etotfbt = True

      #Transitions of threads from an active condition to an ineligible condition > 10 for all pool
      if (float(js[i]['ELAP_ATI']) > 10):
         eatibt = True
         listomsp.append[s]
      
      i += 1
      
   #Determine state to pass to Nagios
   #CRITICAL = 2
   #WARNING = 1
   #OK = 0
   if eatibt or etotfbt:
    print("MEMORY POOLS ARE IN CRITICAL STATUS: affected pools are " + ''.join(listomsp))
    exit(2)
   elif ewtibeatw:
    print("MEMORY POOLS ARE IN WARNING STATUS: affected pools are " + ''.join(listwmsp))
    exit(1)
   else:
    print("MEMORY POOLS ARE IN OK STATUS: ")
    exit(0)   