# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 20:21:21 2021

@author: Abhimanyu Das
"""

import threading
import endpoint
import scraper

if __name__ == "__main__":
    t1 = threading.Thread(target=endpoint.run)
    t2 = threading.Thread(target=scraper.run)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()