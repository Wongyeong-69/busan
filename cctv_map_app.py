# cctv_map_app.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.font_manager as fm
import urllib.request
import os

def set_korean_font():
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        url = "https://github.com/naver/nanumfont/blob/master/ttf/NanumGothic.ttf?raw=true"
        urllib.request.urlretrieve(url, font_path)
    fm.fontManager.addfont(font_path)

@st.cache_data
def load_cctv_data():
    df = pd.read_excel("data/12_04_08_E_CCTV정보.xlsx", engine="openpyxl")
    cols = df.columns.tolist()
    find = lambda kw: next((c for c in cols if kw in c), None)
    return df.rename(columns={
        find("설치목적"): "목적",
        find("도로명주소"): "설치장소",
        find("위도"): "위도",
        find("경도"): "경도",
        find("설치연"): "설치연도",
        find("카메라대수"): "대수"
    }).dropna(subset=["위도", "경도"])

def main():
    st.set_page_config(page_title="🗺 CCTV 지도", layout="wide")
    st.title("🗺 CCTV 위치 지도 (독립 실행)")

    set_korean_font()
    df = load_cctv_data()

    m = folium.Map(location=[df["위도"].mean(), df["경도"].mean()], zoom_start=11)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        popup = f"""
        <b>목적:</b> {row['목적']}<br>
        <b>장소:</b> {row['설치장소']}<br>
        <b>연도:</b> {row['설치연도']}<br>
        <b>대수:</b> {row['대수']}
        """
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=folium.Popup(popup, max_width=300)
        ).add_to(marker_cluster)

    st_folium(m, width=900, height=600)

if __name__ == "__main__":
    main()
