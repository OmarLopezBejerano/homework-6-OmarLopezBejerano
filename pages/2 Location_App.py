## Create a streamlit app where a user enters longitude and latitude and it creates a map with with a little icon over the spot that you selected. Again, post the python code for your app as well as a gif screen capture of it running.

import streamlit as st
import pandas as pd

st.title('Location App')
st.write("This app creates a map with a little icon over the spot that you selected by entering longitude and latitude. You can also enter an address and it will convert it to lat and lon for you.")
## Using geopy to convert address to lat and lon if needed.
from geopy.geocoders import Nominatim
loc = Nominatim(user_agent="Geopy Library")
address = st.text_input('Enter an address (optional)')

if address:
     getLoc = loc.geocode(address)
     latitude = getLoc.latitude
     longitude = getLoc.longitude
     st.write("Address is: " + getLoc.address)
     col1, col2 = st.columns(2)
     col1.metric(label="Latitude", value=latitude)
     col2.metric(label="Longitude", value=longitude)
else:
    latitude = st.number_input('Enter Latitude', value=37.76)
    longitude = st.number_input('Enter Longitude', value=-122.4)
    col1, col2 = st.columns(2)
    col1.metric(label="Latitude", value=latitude)
    col2.metric(label="Longitude", value=longitude)

location_df = pd.DataFrame(
     [[latitude, longitude]],
     columns=['lat', 'lon'])

st.map(location_df)
