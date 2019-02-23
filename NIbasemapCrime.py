from mpl_toolkits.basemap import Basemap
from matplotlib import pylab as plt
import pandas as pd
import numpy as np
import os

##read in crime data

crime_data = pd.read_csv(os.getcwd()+"/2018-12-northern-ireland-street.csv")
#filter data for null values in latitude
crime_data_lat_filtered = crime_data[crime_data['Latitude'].isna()==False]
crime_lat = crime_data_lat_filtered['Latitude']
crime_lon = crime_data_lat_filtered['Longitude']

##build the map
m = Basemap(projection='aeqd',lon_0=-6.801,lat_0=54.5973,width=225000,height=135000,resolution='f')
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='green',lake_color='aqua')
m.drawcoastlines()
m.drawstates() 

### Plot crime_data on the map
crime_types = np.unique(crime_data['Crime type'])
for crime in crime_types:
    crime_lat = crime_data_lat_filtered[crime_data_lat_filtered['Crime type']==crime].Latitude
    crime_lon = crime_data_lat_filtered[crime_data_lat_filtered['Crime type']==crime].Longitude
    lat,lon = list(crime_lat),list(crime_lon) #convert to numpy array
    x,y = m(lon,lat)
    m.plot(x,y,'.',markersize=13,alpha=.5,label=str(crime))
    

plt.title('NIBasemap/Crime Data')
plt.legend(loc="lower left")
plt.show()


