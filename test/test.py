'''
Created on Oct 20, 2014

@author: shenliang
'''
import unittest
from lweather.db import AreaDB


class TestAreaDB(unittest.TestCase):


    def testAdd(self):
        areaDB = AreaDB('weather.db')
        
        area_code = '01'
        area_name = 'beijing'
        areaDB.add(area_code, area_name)
        
        aArea = (area_code, area_name, None)
        
        bArea = areaDB.get('01')
        
        self.assertEqual(aArea, bArea, 'done')
        
    def testAddMany(self):
        areaDB = AreaDB('weather.db')
        
        areas = [
                 ('01','beijing'),
                 ('02','shanghai')
                ]
        areaDB.add_many(areas)
        
        self.assertEqual(areaDB.get('01')[1], 'beijing', 'done')
        self.assertEqual(areaDB.get('02')[1], 'shanghai', 'done')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()