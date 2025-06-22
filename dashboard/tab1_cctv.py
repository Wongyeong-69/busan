# dashboard/tab1_cctv.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import matplotlib as mpl
import urllib.request

import os

mpl.rc('font', family='Malgun Gothic')  # macOS는 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

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

# ✅ CCTV 데이터
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

# ✅ 범죄 데이터
@st.cache_data
def load_crime_data():
    df = pd.read_csv("data/경찰청_부산경찰서별_범죄현황_UTF8.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    data = df[['경찰서', '합계', 'cctv개수']].dropna()
    data.columns = ['경찰서', '범죄건수', 'CCTV개수']
    data["범죄율"] = data["범죄건수"] / data["CCTV개수"]
    return data.reset_index(drop=True)

def tab1_cctv():
    col1, col2 = st.columns([1, 1.5])

    with col2:
        st.subheader("📊 범죄 데이터")

        data = load_crime_data()
        option = st.radio("🔍", ["1. 범죄율 정렬", "2. CCTV 개수 vs 범죄건수", "3. CCTV 대비 범죄율"], horizontal=True)

        if option == "1. 범죄율 정렬":
            crime_df = pd.read_csv("data/경찰청_부산경찰서별_범죄현황_UTF8.csv", encoding="utf-8-sig")
            population_df = pd.read_csv("data/부산광역시 주민등록인구통계_20231231.csv", encoding='cp949')

            crime_df = crime_df[['경찰서', '합계']].copy()
            crime_df.columns = ['구군', '범죄건수']
            population_df.columns = ['구군', '인구수']

            replace_map = {
                "중부경찰서": "중구", "서부경찰서": "서구", "동부경찰서": "동구",
                "영도경찰서": "영도구", "부산진경찰서": "부산진구", "동래경찰서": "동래구",
                "남부경찰서": "남구", "북부경찰서": "북구", "해운대경찰서": "해운대구",
                "사하경찰서": "사하구", "금정경찰서": "금정구", "연제경찰서": "연제구",
                "수영경찰서": "수영구", "사상경찰서": "사상구", "기장경찰서": "기장군",
                "강서경찰서": "강서구"
            }
            crime_df['구군'] = crime_df['구군'].replace(replace_map)

            merged = pd.merge(crime_df, population_df, on='구군')
            merged['범죄율(%)'] = (merged['범죄건수'] / merged['인구수']) * 100
            merged = merged.sort_values(by='범죄율(%)', ascending=False)

            font_path = "NanumGothic.ttf"
            if os.path.exists(font_path):
                font_prop = fm.FontProperties(fname=font_path)
                plt.rc('font', family=font_prop.get_name())
            else:
                plt.rc('font', family='Malgun Gothic')

            plt.rcParams['axes.unicode_minus'] = False

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(merged['구군'], merged['범죄율(%)'], color='tomato')
            ax.set_title('부산시 구별 범죄율 (%)  (1만명 당)', fontsize=16)
            ax.set_xlabel('구군', fontsize=12)
            ax.set_ylabel('범죄율 (%)', fontsize=12)
            ax.set_xticks(np.arange(len(merged)))
            ax.set_xticklabels(merged['구군'], rotation=45)
            ax.grid(axis='y', linestyle='--', alpha=0.4)
            st.pyplot(fig)
            st.markdown("✅ 상위 범죄율 순 정렬")
            st.dataframe(merged.reset_index(drop=True))

        elif option == "2. CCTV 개수 vs 범죄건수":
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.plot(data["경찰서"], data["CCTV개수"], label="CCTV 개수", marker='o', color='orange')
            ax1.plot(data["경찰서"], data["범죄건수"], label="범죄 건수", marker='s', color='orangered')
            ax1.set_title("지역별 CCTV 개수와 범죄 발생 건수 비교")
            ax1.set_xlabel("동")
            ax1.set_ylabel("건수")
            ax1.set_xticks(np.arange(len(data)))
            ax1.set_xticklabels(data["경찰서"], rotation=45)
            ax1.legend()
            ax1.grid(True)
            st.pyplot(fig1)

            correlation = data["CCTV개수"].corr(data["범죄건수"])
            st.markdown(f"<p style='font-size: 12px; color: gray;'>📌 상관계수: <b>{correlation:.2f}</b></p>", unsafe_allow_html=True)

        elif option == "3. CCTV 대비 범죄율":
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(data["경찰서"], data["범죄율"], color='gray', alpha=0.6)
            ax2.set_title("지역별 CCTV 대비 범죄율")
            ax2.set_xlabel("경찰서")
            ax2.set_ylabel("범죄율")
            ax2.set_xticks(np.arange(len(data)))
            ax2.set_xticklabels(data["경찰서"], rotation=45)
            ax2.grid(axis='y', linestyle='--', alpha=0.5)
            st.pyplot(fig2)

