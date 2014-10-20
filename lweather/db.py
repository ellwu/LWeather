#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 20, 2014

@author: shenliang
'''

import sqlite3

class AreaDB(object):
    """
    Area
    This class will do the db operations for area data like save area data/weather data into db table
    """
    DROP_AREA_TBL_SQL = """
        drop table if exists area;
        """
    CREATE_AREA_TBL_SQL = """
        create table area (
            area_code varchar(10) primary key, 
            area_name varchar(10), 
            weather_code varchar(10));
        """
    INSERT_AREA_SQL = "insert into area(area_code, area_name) values(?, ?)";
    
    UPDATE_AREA_SQL = "update area set weather_code = ? where area_code = ?"
    
    
    def __init__(self, db_name):
        # create db to store area and weather data
        self.__create_db(db_name)
        # connec to db
        self.db_context, self.db_cursor = self.__connect_db(db_name);
        
    
    def __create_db(self, db_name):
        """
        __create_db
        create a sqlite3 db with given db file name
        it will create an area table for storing area codes and names and weather ids
        """
        cx = sqlite3.connect(db_name)  # @UndefinedVariable
        cur = cx.cursor()
        
        cur.execute(AreaDB.DROP_AREA_TBL_SQL)        
        cur.execute(AreaDB.CREATE_AREA_TBL_SQL)
        
        cur.close()
        cx.close()
        
            
    def __connect_db(self, db_name):
        """
        connect to a area db and return a context and a cursor
        """
        cx = sqlite3.connect(db_name)  # @UndefinedVariable
        
        return cx, cx.cursor()
    
    def __add(self, area_code, area_name):
        """
        add area into db
        """
        self.db_cursor.execute(AreaDB.INSERT_AREA_SQL, (area_code, area_name))
        
        self.db_context.commit()
        
        
    def __add_many(self, areas):
        """
        add many areas at one time
        areas like:
        [
            ('01','beijing'),
            ('02','shanghai')
        ]
        """
        self.db_cursor.executemany(AreaDB.INSERT_AREA_SQL,areas)
        
        self.db_context.commit()
        
    def __update(self, area_code, weather_code):
        """
        set weather code for given area
        """
        self.db_cursor.execute(AreaDB.UPDATE_AREA_SQL, (weather_code, area_code))
        
        self.db_context.commit()
        
    