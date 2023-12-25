#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 13:27:07 2023

@author: lukasgartmair
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:59:26 2023

@author: lukasgartmair
"""

import sqlite3

def initialize_db_connection():

    con = sqlite3.connect("database/cards.db")
    
    cur = con.cursor()

    return cur

def get_settlements(cur):

    res = cur.execute("SELECT * FROM SETTLEMENTS")
    
    settlements = res.fetchall()
    
    return settlements

def parse_results(results):
    
    parsed_results = [s[0].split(",") for s in results]
    
    return parsed_results

def get_settlements_from_database():
    
    cur = initialize_db_connection()
    
    settlements = get_settlements(cur)
    
    settlements = parse_results(settlements)
    
    return settlements