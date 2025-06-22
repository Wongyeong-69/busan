import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import urllib.request
import os
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# ✅ 한글 폰트 설정
def set_korean_font():
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://github.com/naver/nanumfont/blob/master/ttf/NanumGothic.ttf?raw=true"
            urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            st.error(f"❌ 한글 폰트 다운로드 실패: {e}")
            return
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False

# ✅ CCTV 데이터 로드
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

# ✅ 범죄 데이터 로드
@st.cache_data
def load_crime_data():
    df = pd.read_csv("data/경찰청_부산경찰서별_범죄현황_UTF8.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    data = df[['경찰서', '합계', 'cctv개수']].dropna()
    data.columns = ['경찰서', '범죄건수', 'CCTV개수']
    data["범죄율"] = data["범죄건수"] / data["CCTV개수"]
    return data.reset_index(drop=True)

# ✅ 탭 함수 정의
def tab1_cctv():
    set_korean_font()
    st.subheader("🗺️ CCTV 지도 및 범죄 분석")

    left_col, right_col = st.columns([1, 1.5])

    # ▶️ 왼쪽: CCTV 지도
    with left_col:
       # st.subheader("🗺 CCTV 위치 지도")
        df_vis = load_cctv_data()

        m = folium.Map(
            location=[df_vis["위도"].mean(), df_vis["경도"].mean()],
            zoom_start=11,
            tiles="OpenStreetMap"
        )
        marker_cluster = MarkerCluster().add_to(m)
        for _, row in df_vis.iterrows():
            popup = (
                f"<b>목적:</b> {row['목적']}<br>"
                f"<b>장소:</b> {row['설치장소']}<br>"
                f"<b>연도:</b> {row['설치연도']}<br>"
                f"<b>대수:</b> {row['대수']}"
            )
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=folium.Popup(popup, max_width=300)
            ).add_to(marker_cluster)

        st_folium(m, width=500, height=600)

    # ▶️ 오른쪽: 라디오 버튼 + 분석 결과
    with right_col:
        st.subheader("📊 CCTV 및 범죄 데이터 분석")

        # ✅ 라디오 버튼을 오른쪽 영역 최상단에 배치
        option = st.radio(
            "🔍 항목 선택",
            ["1. CCTV 개수 vs 범죄건수", "2. CCTV 대비 범죄율", "3. 범죄율 정렬"],
            horizontal=True,
            key="radio_inside"
        )

        data = load_crime_data()

        if option == "1. CCTV 개수 vs 범죄건수":
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data["경찰서"], data["CCTV개수"], label="CCTV 개수", marker='o', color='orange')
            ax.plot(data["경찰서"], data["범죄건수"], label="범죄 건수", marker='s', color='orangered')
            ax.set_title("지역별 CCTV 개수와 범죄 발생 건수 비교")
            ax.set_xlabel("경찰서")
            ax.set_ylabel("건수")
            ax.set_xticks(np.arange(len(data)))
            ax.set_xticklabels(data["경찰서"], rotation=45)
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            corr = data["CCTV개수"].corr(data["범죄건수"])
            st.markdown(f"<p style='font-size: 12px; color: gray;'>📌 상관계수: <b>{corr:.2f}</b></p>", unsafe_allow_html=True)

        elif option == "2. CCTV 대비 범죄율":
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(data["경찰서"], data["범죄율"], color='gray', alpha=0.6)
            ax.set_title("지역별 CCTV 대비 범죄율")
            ax.set_xlabel("경찰서")
            ax.set_ylabel("범죄율")
            ax.set_xticks(np.arange(len(data)))
            ax.set_xticklabels(data["경찰서"], rotation=45)
            ax.grid(axis='y', linestyle='--', alpha=0.5)
            st.pyplot(fig)

        elif option == "3. 범죄율 정렬":
            sorted_df = data.sort_values("범죄율", ascending=True).reset_index(drop=True)
            st.markdown("#### 📋 CCTV 대비 범죄율 낮은 순 정렬")
            st.dataframe(sorted_df, use_container_width=True)
