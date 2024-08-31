# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 19:58:23 2024

@author: tfiket

Simple subroutine to calculate distance from hypocentre to the station
coordinates in lat_hypo, lon_hypo, depth_hypo (km)
lat_sta, lon_sta, height_sta (km)

assumed P wave velocity 5.8 km/s since majority of Croatian earthquakes 
have hypocentres in the 0-15 km depth range

see for instance:
Josip Stipčević, Hrvoje Tkalčić, Marijan Herak, Snježana Markušić, 
Davorka Herak, Crustal and uppermost mantle structure beneath the External
Dinarides, Croatia, determined from teleseismic receiver functions, 
Geophysical Journal International, Volume 185, Issue 3, June 2011, 
Pages 1103–1119, https://doi.org/10.1111/j.1365-246X.2011.05004.x
    
"""

import math

def calculate_distance_and_pwave_time(hypo_lat, hypo_lon, hypo_depth, station_lat, station_lon, station_height):
    # Convert degrees to radians
    hypo_lat_rad = math.radians(hypo_lat)
    hypo_lon_rad = math.radians(hypo_lon)
    station_lat_rad = math.radians(station_lat)
    station_lon_rad = math.radians(station_lon)
    
    # Earth's radius in kilometers
    earth_radius = 6371.0
    
    # Calculate great-circle distance (Haversine formula)
    delta_lat = station_lat_rad - hypo_lat_rad
    delta_lon = station_lon_rad - hypo_lon_rad
    
    a = math.sin(delta_lat/2)**2 + math.cos(hypo_lat_rad) * math.cos(station_lat_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    surface_distance = earth_radius * c  # Great-circle distance in kilometers
    
    # Consider the height of the station and depth of the hypocenter
    hypo_elevation = -hypo_depth  # depth is below Earth's surface
    station_elevation = station_height
    
    # Calculate 3D distance
    vertical_difference = station_elevation - hypo_elevation
    total_distance = math.sqrt(surface_distance**2 + vertical_difference**2)  # in kilometers
    
    # P-wave velocity (km/s)
    vp = 5.8 # 8.0 km/s 
    # S-wave velocity (km/s) (Balkan model)
    vs = 3.48
    
    # Calculate P and S wave travel time
    travel_time_p = total_distance / vp  # in seconds
    travel_time_s = total_distance / vs  # in seconds
    
    return total_distance, travel_time_p, travel_time_s

# Example usage (Petrinja earthquake December 29-th,2020):
hypo_lat = 45.41629     # Latitude of hypocenter
hypo_lon = 	16.20806    # Longitude of hypocenter
hypo_depth = 13.64      # Depth of hypocenter in kilometers

#station zagreb
station_lat = 45.827084 # Latitude of seismic station
station_lon = 15.98687  # Longitude of seismic station
station_height = 0.179  # Height of seismic station in kilometers (above sea level)

distance, p_wave_time, s_wave_time = calculate_distance_and_pwave_time(hypo_lat, hypo_lon, hypo_depth, station_lat, station_lon, station_height)
print(f"Distance: {distance:.2f} km")
print(f"P-wave Travel Time: {p_wave_time:.2f} seconds")
print(f"S-wave Travel Time: {s_wave_time:.2f} seconds")
print(f"EEW Response Time: {s_wave_time-p_wave_time:.2f} seconds")

