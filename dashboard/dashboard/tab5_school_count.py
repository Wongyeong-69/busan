import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request

# ─── 한글 폰트 설정 ───
win_font = "C:\\Windows\\Fonts\\malgun.ttf"
if os.path.exists(win_font):
    font_path = win_font
else:
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        try:
            url = (
                "https://github.com/naver/nanumfont/"
                "blob/master/ttf/NanumGothic.ttf?raw=true"
            )
            urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            st.error(f"❌ 한글 폰트 로드 실패: {e}")
            font_path = None

if font_path:
    fontprop = fm.FontProperties(fname=font_path)
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = fontprop.get_name()  # ✅ 전역 폰트 설정
else:
    fontprop = None

# ─── 탭5 함수 ───
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
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df["동"], rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ 시각화 오류: {type(e).__name__}: {e}")
