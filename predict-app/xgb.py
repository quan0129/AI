import streamlit as st
import pandas as pd
import pickle

@st.cache_resource
def load_model():
    with open(r"xgboost_v1.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("🏠 Dự đoán giá bất động sản")

level = st.number_input("Tầng (level)", min_value=0)
rooms = st.number_input("Số phòng (rooms)", min_value=0)
area = st.number_input("Diện tích (area)", min_value=0.0)
kitchen_area = st.number_input("Diện tích bếp (kitchen_area)", min_value=0.0)
geo_lat = st.number_input("Vĩ độ (geo_lat)", format="%.6f")
geo_lon = st.number_input("Kinh độ (geo_lon)", format="%.6f")
building_type = st.number_input("Loại toà nhà (building_type)", min_value=0)
object_type = st.number_input("Loại tài sản (object_type)", min_value=0)
level_to_levels = st.number_input("Tỷ lệ tầng (level / max_levels)", min_value=0.0)
year = st.number_input("Năm (year)", min_value=1900, max_value=2100, value=2025)
month = st.number_input("Tháng (month)", min_value=1, max_value=12)
area_to_rooms = st.number_input("Diện tích / số phòng (area/rooms)", min_value=0.0)

# Dự đoán khi nhấn nút
if st.button("🔮 Dự đoán giá"):
    input_df = pd.DataFrame([{
        "level": level,
        "rooms": rooms,
        "area": area,
        "kitchen_area": kitchen_area,
        "geo_lat": geo_lat,
        "geo_lon": geo_lon,
        "building_type": building_type,
        "object_type": object_type,
        "level_to_levels": level_to_levels,
        "year": year,
        "month": month,
        "area_to_rooms": area_to_rooms,
    }])

    prediction = model.predict(input_df)[0]
    st.success(f"💰 Giá dự đoán: {prediction:,.0f} rúp")
