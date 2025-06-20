import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


def set_korean_font():
    font_path = "NanumGothic.ttf"  # 루트 디렉토리에 있어야 함
    if not os.path.exists(font_path):
        st.warning("❗ NanumGothic.ttf 파일이 없습니다. 한글이 깨질 수 있습니다.")
        return
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_name
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()  # 🔻 이거 꼭 실행해야 적용됨

# ✅ 가장 첫 줄에서 단 한 번 호출
st.set_page_config(page_title="부산시 통합 시각화", layout="wide")

# ✅ 각 탭 함수 import
from dashboard.tab1_cctv import tab1_cctv
from dashboard.tab2_lights_vs_crime import tab2_lights_vs_crime
from dashboard.tab3_oneperson_vs_lights import tab3_oneperson_vs_lights
from dashboard.tab4_police_count import tab4_police_count
from dashboard.tab5_school_count import tab5_school_count  # ✅ NEW

st.title("📊 부산에서 가장 안전한 동네는 어디일까?")

# ✅ 탭 순서 조정: 5번(학교 수)을 4번으로, 4번(경찰서 수)을 5번으로
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 CCTV 지도 + 범죄 ",
    "📈 가로등 vs 범죄",
    "🏠 1인 가구 vs 가로등",
    "🏫 부산 동별 학교 수",      # ✅ tab5 내용
    "🚓 동별 경찰서 수"          # ✅ tab4 내용
])

with tab1:
    tab1_cctv()
with tab2:
    tab2_lights_vs_crime()
with tab3:
    tab3_oneperson_vs_lights()
with tab4:
    tab5_school_count()   # ✅ 파일명 tab5_school_count.py
with tab5:
    tab4_police_count()   # ✅ 파일명 tab4_police_count.py
