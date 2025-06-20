import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import numpy as np
import urllib.request
import os

# ✅ 한글 폰트 설정 함수
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

# ✅ 폰트 적용 실행
set_korean_font()

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

# ✅ 탭1 본문 함수
def tab1_cctv():
    col1, col2 = st.columns([1, 1.5])

    # ▶️ 그래프 및 표
    with col2:
        st.subheader("📊 CCTV 및 범죄 데이터 ")

        data = load_crime_data()
        option = st.radio("🔍 항목 선택", ["1. CCTV 개수 vs 범죄건수", "2. CCTV 대비 범죄율", "3. 범죄율 정렬"], horizontal=True)

        if option == "1. CCTV 개수 vs 범죄건수":
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.plot(data["경찰서"], data["CCTV개수"], label="CCTV 개수", marker='o', color='orange')
            ax1.plot(data["경찰서"], data["범죄건수"], label="범죄 건수", marker='s', color='orangered')
            ax1.set_title("지역별 CCTV 개수와 범죄 발생 건수 비교")
            ax1.set_xlabel("경찰서")
            ax1.set_ylabel("건수")
            ax1.set_xticks(np.arange(len(data)))
            ax1.set_xticklabels(data["경찰서"], rotation=45)
            ax1.legend()
            ax1.grid(True)
            st.pyplot(fig1)

            correlation = data["CCTV개수"].corr(data["범죄건수"])
            st.markdown(f"<p style='font-size: 12px; color: gray;'>📌 상관계수: <b>{correlation:.2f}</b></p>", unsafe_allow_html=True)

        elif option == "2. CCTV 대비 범죄율":
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(data["경찰서"], data["범죄율"], color='gray', alpha=0.6)
            ax2.set_title("지역별 CCTV 대비 범죄율")
            ax2.set_xlabel("경찰서")
            ax2.set_ylabel("범죄율")
            ax2.set_xticks(np.arange(len(data)))
            ax2.set_xticklabels(data["경찰서"], rotation=45)
            ax2.grid(axis='y', linestyle='--', alpha=0.5)
            st.pyplot(fig2)

        elif option == "3. 범죄율 정렬":
            data["범죄율"] = pd.to_numeric(data["범죄율"], errors='coerce')
            sorted_df = data.sort_values("범죄율", ascending=True).reset_index(drop=True)
            st.markdown("#### 📋 CCTV 대비 범죄율 낮은 순 정렬 표")
            st.dataframe(sorted_df, use_container_width=True)
