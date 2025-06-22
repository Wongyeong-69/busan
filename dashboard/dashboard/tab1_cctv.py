import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import urllib.request
import os

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

# ✅ 범죄 + CCTV 데이터 로드
@st.cache_data
def load_crime_data():
    df = pd.read_csv("data/경찰청_부산경찰서별_범죄현황_UTF8.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    data = df[['경찰서', '합계', 'cctv개수']].dropna()
    data.columns = ['경찰서', '범죄건수', 'CCTV개수']
    data["범죄율"] = data["범죄건수"] / data["CCTV개수"]
    return data.reset_index(drop=True)

# ✅ 메인 분석 탭
def tab1_cctv():
    set_korean_font()
    st.subheader("🗺️ CCTV 지도 및 범죄 분석")

    left_col, right_col = st.columns([1, 1.5])

    with right_col:
        st.subheader("📊 CCTV 및 범죄 데이터 분석")

        option = st.radio(
            "🔍 항목 선택",
            ["1. 인구수 대비 범죄율", "2. CCTV 개수 vs 범죄건수", "3. CCTV 대비 범죄율"],
            horizontal=True,
            key="radio_inside"
        )

        if option == "1. 인구수 대비 범죄율":
            # ✅ 데이터 로드
            crime_df = pd.read_csv("data/경찰청_부산경찰서별_범죄현황_UTF8.csv", encoding="utf-8-sig")
            crime_df.columns = crime_df.columns.str.strip()

            population_df = pd.read_csv("data/부산광역시 주민등록인구통계_20231231.csv", encoding="cp949")
            population_df.columns = ['경찰서', '인구수']

            # ✅ 병합 및 계산
            crime_df = crime_df[['경찰서', '합계']].copy()
            crime_df.columns = ['경찰서', '범죄건수']
            merged = pd.merge(crime_df, population_df, on='경찰서', how='inner')
            merged['범죄율(%)'] = (merged['범죄건수'] / merged['인구수']) * 100
            merged = merged.sort_values(by='범죄율(%)', ascending=False)

            # ✅ 시각화
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(merged['경찰서'], merged['범죄율(%)'], color='tomato')
            ax.set_title('부산시 인구 수 대비 범죄율 (%)')
            ax.set_xlabel('인구 수')
            ax.set_ylabel('범죄율 (%)')
            ax.set_xticks(range(len(merged)))
            ax.set_xticklabels(merged['경찰서'], rotation=45)
            ax.grid(axis='y', linestyle='--', alpha=0.4)
            st.pyplot(fig)

            st.markdown("✅ 인구수 대비 범죄율 상위 지역")
            st.dataframe(merged.reset_index(drop=True), use_container_width=True)

        elif option == "2. CCTV 개수 vs 범죄건수":
            data = load_crime_data()
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(data["경찰서"], data["CCTV개수"], label="CCTV 개수", marker='o', color='orange')
            ax.plot(data["경찰서"], data["범죄건수"], label="범죄 건수", marker='s', color='orangered')
            ax.set_title("지역별 CCTV 개수와 범죄 발생 건수 비교")
            ax.set_xlabel("동")
            ax.set_ylabel("건수")
            ax.set_xticks(np.arange(len(data)))
            ax.set_xticklabels(data["경찰서"], rotation=45)
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

            corr = data["CCTV개수"].corr(data["범죄건수"])
            st.markdown(f"<p style='font-size: 12px; color: gray;'>📌 상관계수: <b>{corr:.2f}</b></p>", unsafe_allow_html=True)

        elif option == "3. CCTV 대비 범죄율":
            data = load_crime_data()
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(data["경찰서"], data["범죄율"], color='gray', alpha=0.6)
            ax.set_title("지역별 CCTV 대비 범죄율")
            ax.set_xlabel("동")
            ax.set_ylabel("범죄율")
            ax.set_xticks(np.arange(len(data)))
            ax.set_xticklabels(data["경찰서"], rotation=45)
            ax.grid(axis='y', linestyle='--', alpha=0.5)
            st.pyplot(fig)
