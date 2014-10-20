#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 20, 2014

@author: shenliang
'''

import sqlite3
import httplib

def http_connection(host):
    return httplib.HTTPConnection(host)

def http_request(conn, method, uri):
    conn.request(method, uri)
    resp = conn.getresponse()
    status = resp.status
    data = resp.read()
    return status, data

def get_top_areas(conn, service_url):
    """
    return top areas list
    like: ['01|beijing', '02|shanghai',....]
    """
    status, top_areas_resp = http_request(conn, "GET", service_url)
    if status == 200:
        return top_areas_resp.split(',')

def get_child_areas(conn, service_url):
    status, child_areas = http_request(conn, "GET", service_url)
    if status == 200:
        return child_areas.split(',')

def create_db(db_file_name):
    """create_db
    create a sqlite3 db with given db file name
    it will create an area table for storing area codes and names and weather ids
    """
    cx = sqlite3.connect(db_file_name)  # @UndefinedVariable
    cur = cx.cursor()
    
    drop_exists_tbl="""drop table if exists area"""
    cur.execute(drop_exists_tbl)
    area_tbl_sql = """
    create table area (area_code varchar(10) primary key, area_name varchar(10), weather_code varchar(10))"""
    cur.execute(area_tbl_sql)
    
    cur.close()
    cx.close()
    
def connect_db(db_file_name):
    """
    connect to weather db and return context and cursor
    """
    cx = sqlite3.connect(db_file_name)  # @UndefinedVariable
    return cx, cx.cursor()
    
def add_area(cursor, area):
    """
    add area into db
    """
    cursor.execute("insert into area(area_code, area_name) values(?, ?)", (area.area_code, area.area_name))
    
def set_weather_code(cursor, area_code, weather_code):
    """
    set area weather code by area code
    """
    cursor.execute("update area set weather_code = ? where area_code = ?", (weather_code, area_code))
    
class Area(object):
    """
    Area Object to represent record
    """
    def __init__(self, key_value_str):
        kvs = key_value_str.split('|')
        self.area_code = kvs[0]
        self.area_name = kvs[1].decode('utf-8')

def recur_area(http_conn, db_cur, area_code):
    
    child_areas = get_child_areas(http_conn, 'http://m.weather.com.cn/data5/city' + area_code + '.xml')

    for area_str in child_areas:
        kvs = area_str.split('|')
        key = kvs[0]
        value = kvs[1]
        if value.isdigit():
            set_weather_code(cur, key, value)
            break
        print area_str
        add_area(cur, Area(area_str))
        recur_area(http_conn, db_cur, key)


if __name__ == '__main__':

    db_file_name = 'weather.db'
    
    create_db(db_file_name)
    
    cx, cur = connect_db(db_file_name)

    http_conn = http_connection('m.weather.com.cn')
    
    top_areas = get_top_areas(http_conn,'http://m.weather.com.cn/data5/city.xml')
    
    for area_str in top_areas:
        add_area(cur, Area(area_str))
        recur_area(http_conn, cur, area_str.split('|')[0])
        cx.commit()

    http_conn.close()

    cx.commit()
    cur.close()
    cx.close()
if __name__ == '__main__':
    pass