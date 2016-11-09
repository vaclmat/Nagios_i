import os                            
import ibm_db                        
from itoolkit.db2.idb2call import *  
                                     
database='*LOCAL'                    
user ='*******'                      
password='*******'                   
                                     
itransport = iDB2Call(user, password)