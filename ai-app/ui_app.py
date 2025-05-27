import streamlit as st
import pandas as pd
import pickle

# Load model
with open("feyn_symbolic_regression_model_23_05.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Prediction App")

# Nhập dữ liệu
geo_lat = st.number_input("Latitude (geo_lat)", min_value=0)
geo_lon = st.number_input("Longitude (geo_lon)", min_value=0)
region = st.number_input("Region")
building_type = st.number_input("Building Type")
level = st.number_input("Level", min_value=0)
levels = st.number_input("Total levels", min_value=0)
rooms = st.number_input("Rooms", min_value=0)
area = st.number_input("Area (m²)", min_value=0)
kitchen_area = st.number_input("Kitchen area (m²)", min_value=0)
object_type = st.number_input("Object Type")
level_to_levels = st.number_input("Level to Levels Ratio", value=level / levels)
year = st.number_input("Year Built", min_value=0)
month = st.number_input("Month", min_value=0)

# Tạo input dataframe
input_df = pd.DataFrame([{
    "geo_lat": geo_lat,
    "geo_lon": geo_lon,
    "region": region,
    "building_type": building_type,
    "level": level,
    "levels": levels,
    "rooms": rooms,
    "area": area,
    "kitchen_area": kitchen_area,
    "object_type": object_type,
    "level_to_levels": level_to_levels,
    "year": year,
    "month": month
}])

# Dự đoán
if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    st.success(f"Prediction result: {prediction:.2f}")
