# dashboard/tab4_police_count.py

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
<<<<<<< HEAD
    plt.rcParams['font.family'] = fontprop.get_name()  # ✅ 전역 설정
=======
    plt.rcParams['font.family'] = fontprop.get_name()  # ✅ 전체 그래프에 적용
>>>>>>> 8e0557a (부산 시각화 대시보드 업로드)
else:
    fontprop = None

# ─── 데이터 로더 ───
@st.cache_data
def load_police_data(path="data/부산동별경찰서.csv"):
    df = pd.read_csv(path, encoding="utf-8")
    df.columns = df.columns.str.strip()
    return df

# ─── 키워드 컬럼 찾기 ───
def find_column(df, keywords):
    for col in df.columns:
        if any(kw in col for kw in keywords):
            return col
    return None

# ─── 탭 함수 ───
def tab4_police_count():
    st.subheader("🚓 부산 동별 경찰서 수")

    try:
        df = load_police_data()
        region_col = find_column(df, ["지역", "동별", "경찰서", "관할"])
        count_col = find_column(df, ["수", "개수", "건수"])

        if not region_col or not count_col:
            raise KeyError(f"❌ 필요한 컬럼을 찾을 수 없습니다: {list(df.columns)}")

        df = df.rename(columns={region_col: "지역", count_col: "개수"})
        df = df.sort_values("개수", ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df["지역"], df["개수"], color="skyblue")

        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df["지역"], rotation=45, fontproperties=fontprop)  # ✅ 한글 명시
        ax.set_xlabel("지역", fontproperties=fontprop)                        # ✅ 한글 명시
        ax.set_ylabel("경찰서 수", fontproperties=fontprop)                   # ✅ 한글 명시
        ax.set_title("부산 동별 경찰서 수", fontproperties=fontprop)         # ✅ 한글 명시

        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h,
                f"{int(h)}",
                ha="center",
                va="bottom",
                fontproperties=fontprop                                         # ✅ 숫자에도 한글 폰트 적용
            )

        st.pyplot(fig)

    except KeyError as ke:
        st.error(str(ke))
    except Exception as e:
        st.error(f"❌ 시각화 오류: {type(e).__name__}: {e}")
