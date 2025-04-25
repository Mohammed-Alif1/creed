import pandas as pd
import math
r = 6371

cartisians = []

def cartisian(a_rad, b_rad):
    x = round(r * b_rad)
    y = round(r * math.log(math.tan(math.pi / 4 + a_rad / 2)))
    cartisians.append((x, y))  
    print(x,y)

df = pd.read_csv('coordinates.csv')

for index, row in df.iterrows():
    if(-90<row['latitude']<90) and (-180<=row['longitude']<=180):
        print(index)
        latitude = math.radians(row['latitude'])  
        longitude = math.radians(row['longitude'])  
        cartisian(latitude, longitude) 
    else:
        cartisians.append((0,0))

dout = pd.DataFrame(cartisians, columns=['x','y'])
dout.to_csv('outp.csv', index=False)
