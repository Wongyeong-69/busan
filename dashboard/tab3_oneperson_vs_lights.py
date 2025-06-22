import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def tab3_oneperson_vs_lights():
    st.subheader("🏠 부산 경찰서별 1인 가구 수 vs 범죄 ")

    # ✅ 한글 폰트 설정
    font_path = "NanumGothic.ttf"
    if os.path.exists(font_path):
        fontprop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = fontprop.get_name()
    else:
        st.error("❌ NanumGothic.ttf 폰트 파일이 없습니다.")
        return
    plt.rcParams['axes.unicode_minus'] = False

    # ✅ CSV 파일 로드
    file_path = "data/경찰청_부산경찰서별_범죄현황_UTF8.csv"
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"❌ CSV 파일 로드 실패: {e}")
        return

    # ✅ 1인 가구 수 데이터 (직접 입력)
    one_person_households = {
        "중부": 11786, "동래": 35220, "영도": 20116, "동부": 18603,
        "부산진": 70609, "서부": 20760, "남부": 40521, "해운대": 50516,
        "사상": 36299, "금정": 40412, "사하": 46442, "연제": 30846,
        "강서": 17355, "북부": 36975, "기장": 22500
    }

    # ✅ 필요한 데이터 추출
    df_filtered = df[df["구분"] == "경찰서"][["경찰서", "합계"]].dropna()
    df_filtered["합계"] = df_filtered["합계"].astype(float)
    df_filtered["1인 가구"] = df_filtered["경찰서"].map(one_person_households)

    # ✅ 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))
    index = range(len(df_filtered))
    bar_width = 0.35

    ax.bar(index, df_filtered["합계"], bar_width, label="범죄 합계")
    ax.bar([i + bar_width for i in index], df_filtered["1인 가구"], bar_width, label="1인 가구 수")

    ax.set_xlabel("경찰서")
    ax.set_ylabel("건수")
    ax.set_title("1인 가구 수 vs 범죄 합계")
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(df_filtered["경찰서"])
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
