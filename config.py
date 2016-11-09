import os                            
import ibm_db                        
from itoolkit.db2.idb2call import *  
                                     
database='*LOCAL'                    
user ='NAGIOS'                       
password='********'                  
                                     
itransport = iDB2Call(user, password)