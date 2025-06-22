import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def set_korean_font():
    font_path = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
    if not os.path.exists(font_path):
        st.warning("❗ NanumGothic.ttf 파일이 없습니다. 한글이 깨질 수 있습니다.")
        return

    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_name
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()
st.set_page_config(page_title="부산시 통합 시각화", layout="wide")

# ✅ 각 탭 함수 import
from dashboard.tab1_cctv import tab1_cctv
from dashboard.tab2_lights_vs_crime import tab2_lights_vs_crime 
from dashboard.tab3_oneperson_vs_lights import tab3_oneperson_vs_lights
from dashboard.tab4_police_count import tab4_police_count
from dashboard.tab5_school_count import tab5_school_count

st.title("📌부산시 통합 시각화 데시보드")

# ✅ 탭 순서: 학교 수 → 1인 가구 → 경찰서 수
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 CCTV 지도 + 범죄",
    "🏠 인구 대비 가로등 수",
    "🏫 부산 동별 학교 수",
    "📈 1인 가구 vs 범죄",
    "🚓 동별 경찰서 수"
])

# ✅ 탭 내용 연결
with tab1:
    tab1_cctv()
with tab2:
    tab2_lights_vs_crime()
with tab3:
    tab5_school_count()              # ✅ tab3: 학교 수
with tab4:
    tab3_oneperson_vs_lights()       # ✅ tab4: 1인 가구 vs 범죄
with tab5:
    tab4_police_count()              # ✅ tab5: 경찰서 수
