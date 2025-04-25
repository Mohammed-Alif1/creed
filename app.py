import streamlit as st
import pandas as pd
import pydeck as pdk
from backend import process_coordinates

st.title("Coordinate Conversion Dashboard")

uploaded_file = st.file_uploader("Upload your coordinates CSV file", type="csv")

if uploaded_file is not None:
    try:
        dout = process_coordinates(uploaded_file)
        st.write("Processed Data:")
        st.dataframe(dout)
        st.download_button(
            label="Download Processed Data as CSV",
            data=dout.to_csv(index=False),
            file_name="processed_data.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(str(e))

st.subheader("Enter Coordinates to Visualize on Map")
latitude_input = st.number_input("Enter Latitude (-90 to 90)", min_value=-90.0, max_value=90.0, step=0.01)
longitude_input = st.number_input("Enter Longitude (-180 to 180)", min_value=-180.0, max_value=180.0, step=0.01)

if latitude_input and longitude_input:
    map_data = pd.DataFrame([{'latitude': latitude_input, 'longitude': longitude_input}])
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