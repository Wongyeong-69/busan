# dashboard/tab5_school_count.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ✅ 운영체제 기본 한글 폰트 설정 (외부 폰트 파일 사용 안 함)
mpl.rc('font', family='Malgun Gothic')  # macOS는 'AppleGothic'
mpl.rcParams['axes.unicode_minus'] = False

def tab5_school_count():
    st.subheader("🏫 부산 동별 학교 수 시각화")

    file_path = "data/부산 학교 수.csv"
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"❌ CSV 파일 로드 실패: {e}")
        return

    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["동"], df["학교 수"], color="skyblue")

        ax.set_title("부산 동별 학교 수", fontsize=16)
        ax.set_xlabel("동", fontsize=12)
        ax.set_ylabel("학교 수", fontsize=12)
        plt.xticks(rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ 시각화 오류: {e}")
