from numpy import *
from math import *
import requests,json
import config

class CallSignConverter:

    def __init__(self, cs,antenna=[37.1798694,-3.610038889,672]):
        self.callsign = cs
        self.antenna = antenna
        
    def getGPSPosition(self):
        self.callsign
        
        payload = {'name': self.callsign, "what": 'loc', "apikey" : config.APIKEY, "format": "json"}
        r = requests.get('http://api.aprs.fi/api/get', params=payload)
        ans = r.json()

        #print json.dumps(ans, indent=4, sort_keys=True)

        lat=float(ans["entries"][0]["lat"])
        lng=float(ans["entries"][0]["lng"])
                
        try: 
            el=float(ans["entries"][0]["altitude"])
        except:
            el=self.antenna[2]
      
        return [lat, lng, el]

    def getRotorsPosition(self):
        gpsPos = self.getGPSPosition()
        # calculos
        def distance_in_earth(latitud1,latitud2,longitud1,longitud2):
            distance_earth=6371672.0*acos(sin(latitud1*pi/180)*sin(latitud2*pi/180)+cos(latitud1*pi/180)*cos(latitud2*pi/180)*cos((longitud1-longitud2)*pi/180))       
            return distance_earth

        def calculate_distance(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2):  
            rt=6371672.0
            rs=6371000.0+elevation2
            distance=sqrt(rt**2+rs**2-2*rs*rt*cos(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt))   
            return distance

        def elevation_antenna(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2):
            rt=6371672.0
            rs=6371000.0+elevation2
            num=(calculate_distance(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2))**2
            num2=(tan(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt)*rt)**2
            num3= (rs-(rt/cos(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt)))**2
            deno1=2*calculate_distance(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2)*(tan(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt)*rt)
            final_elevation=acos((num+num2-num3)/deno1)
            #print final_elevation*180/pi    
            return final_elevation*180/pi

        def azimut(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2):    
            longi=abs( longitud1 - longitud2 ) 
            x=cos(latitud2*pi/180)*sin(longi*pi/180)
            y=(cos(latitud1*pi/180)*sin(latitud2*pi/180))
            aux=sin(latitud1*pi/180)*cos(latitud2*pi/180)*cos(longi*pi/180)
            y=y-aux
            final=atan2(x,y)*180/pi
            if longitud2<longitud1:
                final=360-final
            #print final
            return final        
        
        az=azimut(self.antenna[2],gpsPos[2],self.antenna[0],gpsPos[0],self.antenna[1],gpsPos[1]) 
        el=elevation_antenna(self.antenna[2],gpsPos[2],self.antenna[0],gpsPos[0],self.antenna[1],gpsPos[1])
        return [az,el]
        
        
class GPSConverter:

    def __init__(self, coord,antenna=[37.1798694,-3.610038889,672]):
        self.coordinates = coord
        self.antenna = antenna
        
    def coordinates_converter_latitude(self,degrees,minutes,seconds,ns):
        latitud1=degrees+minutes/60.0+seconds/3600.0
        if ns=="S":
            latitud1=-latitud1
        return latitud1

    def coordinates_converter_longitude(self,degrees,minutes,seconds,ew):
        longitud1=degrees+minutes/60.0+seconds/3600.0
        if ew=="W":
            longitud1=-longitud1
        return longitud1
        
    def getRotorsPosition(self):
        gpsPos = [self.coordinates_converter_latitude(self.coordinates[0],self.coordinates[1],self.coordinates[2],self.coordinates[3]),self.coordinates_converter_longitude(self.coordinates[4],self.coordinates[5],self.coordinates[6],self.coordinates[7]),self.coordinates[8]]
        
        # calculos
        def distance_in_earth(latitud1,latitud2,longitud1,longitud2):
            distance_earth=6371672.0*acos(sin(latitud1*pi/180)*sin(latitud2*pi/180)+cos(latitud1*pi/180)*cos(latitud2*pi/180)*cos((longitud1-longitud2)*pi/180))       
            return distance_earth

        def calculate_distance(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2):  
            rt=6371672.0
            rs=6371000.0+elevation2
            distance=sqrt(rt**2+rs**2-2*rs*rt*cos(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt))   
            return distance

        def elevation_antenna(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2):
            rt=6371672.0
            rs=6371000.0+elevation2
            num=(calculate_distance(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2))**2
            num2=(tan(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt)*rt)**2
            num3= (rs-(rt/cos(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt)))**2
            deno1=2*calculate_distance(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2)*(tan(distance_in_earth(latitud1,latitud2,longitud1,longitud2)/rt)*rt)
            final_elevation=acos((num+num2-num3)/deno1)
            #print final_elevation*180/pi    
            return final_elevation*180/pi

        def azimut(elevation1,elevation2,latitud1,latitud2,longitud1,longitud2):    
            longi=abs( longitud1 - longitud2 ) 
            x=cos(latitud2*pi/180)*sin(longi*pi/180)
            y=(cos(latitud1*pi/180)*sin(latitud2*pi/180))
            aux=sin(latitud1*pi/180)*cos(latitud2*pi/180)*cos(longi*pi/180)
            y=y-aux
            final=atan2(x,y)*180/pi
            if longitud2<longitud1:
                final=360-final
            #print final
            return final        
        
        az=azimut(self.antenna[2],gpsPos[2],self.antenna[0],gpsPos[0],self.antenna[1],gpsPos[1]) 
        el=elevation_antenna(self.antenna[2],gpsPos[2],self.antenna[0],gpsPos[0],self.antenna[1],gpsPos[1])
        return [az,el]