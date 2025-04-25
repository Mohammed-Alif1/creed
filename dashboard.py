import pandas as pd
import streamlit as st
import math
import pydeck as pdk

# Title of the Dashboard
st.title("Coordinate Conversion Dashboard")

# Upload CSV File
uploaded_file = st.file_uploader("Upload your coordinates CSV file", type="csv")

# Process Data
if uploaded_file is not None:
    # Read CSV File
    df = pd.read_csv(uploaded_file)
    
    # Check for Latitude and Longitude
    if 'latitude' in df.columns and 'longitude' in df.columns:
        r = 6371
        cartisians = []
        
        def cartisian(a_rad, b_rad):
            x = round(r * b_rad)
            y = round(r * math.log(math.tan(math.pi / 4 + a_rad / 2)))
            return (x, y)
        
        for index, row in df.iterrows():
            if -90 < row['latitude'] < 90 and -180 <= row['longitude'] <= 180:
                latitude = math.radians(row['latitude'])
                longitude = math.radians(row['longitude'])
                cartisians.append(cartisian(latitude, longitude))
            else:
                cartisians.append((0, 0))
        
        # Create Output DataFrame
        dout = pd.DataFrame(cartisians, columns=['x', 'y'])

        # Display Data
        st.write("Processed Data:")
        st.dataframe(dout)
        
        # Download Processed CSV
        st.download_button(
            label="Download Processed Data as CSV",
            data=dout.to_csv(index=False),
            file_name="processed_data.csv",
            mime="text/csv"
        )
    else:
        st.error("Uploaded file must contain 'latitude' and 'longitude' columns.")

# Additional Feature: Enter Coordinates
st.subheader("Enter Coordinates to Visualize on Map")
latitude_input = st.number_input("Enter Latitude (-90 to 90)", min_value=-90.0, max_value=90.0, step=0.01)
longitude_input = st.number_input("Enter Longitude (-180 to 180)", min_value=-180.0, max_value=180.0, step=0.01)

# Show Coordinates on Map
if latitude_input and longitude_input:
    map_data = pd.DataFrame(
        [{'latitude': latitude_input, 'longitude': longitude_input}]
    )
    st.write("Map Visualization:")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=latitude_input,
            longitude=longitude_input,
            zoom=10,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 30, 160]',
                get_radius=10000,
            ),
        ],
    ))