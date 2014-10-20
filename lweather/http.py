'''
Created on Oct 20, 2014

@author: shenliang
'''
import httplib

class AreaHTTP(object):
    '''
    AreaHTTP
    This class will download area data from http
    '''
    
    WEATHER_SERVICE_HOST = "m.weather.com.cn"
    TOP_AREA_URL = "http://m.weather.com.cn/data5/city.xml"
    CHILD_AREAS_URL_FORMAT = "http://m.weather.com.cn/data5/city{0}.xml"

    def __init__(self):
        '''
        Create a Area HTTP object
        '''
        self.conn = httplib.HTTPConnection(AreaHTTP.WEATHER_SERVICE_HOST)
        
    def __get_request(self, url):
        self.conn.request("GET", url)
        resp = self.conn.getresponse()
        status = resp.status
        data = resp.read()
        return status, data
    
    def get_top_areas(self):
        status, top_areas_resp = self.__get_request(AreaHTTP.TOP_AREA_URL)
        
        if status == 200:
            top_areas = []
            
            for area in top_areas_resp.split(','):
                kv = area.split('|')
                k = kv[0]
                v = kv[1].decode('utf-8')
                top_areas.append((k,v))
                
            return top_areas
        
    def get_child_areas(self, area_code):
        status, child_areas_resp = self.__get_request(AreaHTTP.CHILD_AREAS_URL_FORMAT.format(area_code))
        
        if status == 200:
            child_areas = []
            
            for area in child_areas_resp.split(','):
                kv = area.split('|')
                k = kv[0]
                v = kv[1].decode('utf-8')
                child_areas.append((k,v))
                
            return child_areas
        
    def close(self):
        self.conn.close()
     
if __name__ == '__main__':
    """
    l = ['01|beijing','02|shanghai']
    for a in l:
        print tuple(a.split('|'))
    """
    areaHTTP = AreaHTTP()
    print areaHTTP.get_child_areas('0101')
    areaHTTP.close()
    
    
        