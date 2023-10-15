import streamlit as st

# from dashboard import func
from model import get_area_llava, get_cost_of_installing, get_total_area
from energy import get_radiation_data
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static


def geocode_address(address):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "YourAppName/1.0 (your@email.com)"}

    response = requests.get(base_url, params=params, headers=headers)
    data = response.json()

    if not data:
        return None, None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    return lat, lon


# address = "1600 Amphitheatre Parkway, Mountain View, CA"
# lat, lon = geocode_address(address)
# print(f"Latitude: {lat}, Longitude: {lon}")


def main():
    st.title("Ecoverse")
    st.header("Helping in your solar energy journey")

    # Create a form
    with st.form(key="my_form"):
        address = st.text_input(label="Enter your address", placeholder="555 California Street, San Francisco")
        # my total sqft area is 500 and usable sqft area is 350
        description = st.text_area(
            label="(Optional) Tell us about your location",
            placeholder="What is the sq ft area, What is the usable area, Near San Marie Square",
        )
        image_data = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        # Create a submit button
        submit_button = st.form_submit_button(label="Submit")

    # Display the data after submission
    if submit_button:
        if address:
         st.write(f"Your address: {address}")
         # extracted sqft information from LLM
         new_sqft = get_total_area(description)
         # sqft = 100
         # Calculations:
         if not new_sqft:
         # @harsha to update LLM function. The output should be a float number not a string.
         # new_sqft = get_total_area(image)
            try:
                  new_sqft = get_area_llava(image_data)
            except Exception as e:
                  print(f"Visual QA output invalid {e}")
                  new_sqft = 100
         
         # define constants
         sq_meter_to_sq_ft = 10.76
         single_solar_panel_sq_ft = 15
         available_area_ratio = 0.33
         
         solar_panels = (new_sqft * available_area_ratio * sq_meter_to_sq_ft )/single_solar_panel_sq_ft  # @harsha to update open ai call.
         country_name = "USA"
         energy_produced = solar_panels * 0.3 # in kW  # @harsha to update open ai call.
         #cost = "$20,000"  # @harsha to update open ai call.
         cost = get_cost_of_installing(number_of_panels=solar_panels, country=country_name)

         cost_saved = "$1000"  # @harsha to update open ai call.
         green_score = 180  # @harsha to update open ai call.

         lat, lon = geocode_address(address)
         # Test data (40.767, -7.910)
         radiation_data = get_radiation_data((40.767, -7.910), new_sqft)

         # Show location
         # st.image(image=image, use_column_width=False)
         loc_df = pd.DataFrame({"latitude": lat, "longitude": lon}, index=[0])
         # print(loc_df)
         st.map(loc_df, latitude="latitude", longitude="longitude", size=20, color="#0044ff", zoom=10)
         # m = folium.Map(location=[40.767, -7.910], zoom_start=6)
         # folium_static(m)
         df = pd.DataFrame(radiation_data)
         df["time_new"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")
         st.title("Energy generated last day by hour.")
         st.line_chart(df.set_index("time")["Energy (kWh)"])
         # st.line_chart(df, y='Energy (kWh)')

         st.markdown(f"**Solar Panels in the given area:** {solar_panels}")
         st.write(f"Solar Panels in the given area: {solar_panels}, which will cost around {cost} USD")
         st.write(
               f"Based on the location and weather information, {energy_produced} will be the energy produced annualy"
         )
         st.write(f"Households in your location on an avg save {cost_saved} yearly")
         st.write(
               f"Your Green score would be {green_score}, You would be in top 66% to contribute in reducing carbon emissions"
         )


if __name__ == "__main__":
    main()
