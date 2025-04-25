import pandas as pd
import math

def cartisian(a_rad, b_rad, r=6371):
    x = round(r * b_rad)
    y = round(r * math.log(math.tan(math.pi / 4 + a_rad / 2)))
    return (x, y)

def process_coordinates(file):
    df = pd.read_csv(file)
    
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        raise ValueError("Uploaded file must contain 'latitude' and 'longitude' columns.")
    
    cartisians = []
    for index, row in df.iterrows():
        if -90 < row['latitude'] < 90 and -180 <= row['longitude'] <= 180:
            lat_rad = math.radians(row['latitude'])
            lon_rad = math.radians(row['longitude'])
            cartisians.append(cartisian(lat_rad, lon_rad))
        else:
            cartisians.append((0, 0))
    
    return pd.DataFrame(cartisians, columns=['x', 'y'])