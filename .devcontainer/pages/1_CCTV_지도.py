# pages/1_CCTV_지도.py

import streamlit as st
from dashboard.tab1_cctv import cctv_map_page

st.set_page_config(page_title="🗺 CCTV 지도", layout="wide")
st.title("🗺 CCTV 위치 지도")

cctv_map_page()
