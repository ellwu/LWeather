#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 20, 2014

@author: shenliang
'''


        

if __name__ == '__main__':
    
    from lweather.db import AreaDB
    from lweather.http import AreaHTTP
    
    areaDB = AreaDB('weather')
    areaHTTP = AreaHTTP()
    
    top_areas = areaHTTP.get_top_areas()
    areaDB.add_many(top_areas)
    
    def recur(area_code):
        print area_code
        areas = areaHTTP.get_child_areas(area_code)
        
        if len(areas) == 1 and areas[0][1].isdigit():
            areaDB.update(*areas[0])
            return
        
        areaDB.add_many(areas)
        
        for area in areas:
            recur(area[0])
            
    for top in top_areas:
        recur(top[0])
    
    areaDB.close()
    areaHTTP.close()
    
    
    
    