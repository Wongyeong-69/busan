import streamlit as st

# 📌 페이지 설정
st.set_page_config(page_title="📌 부산시 통합 시각화 대시보드", layout="wide")

# 📌 탭별 함수 import
from dashboard.tab1_cctv import cctv_analysis_page
from dashboard.tab2_lights_vs_crime import tab2_lights_vs_crime
from dashboard.tab3_oneperson_vs_lights import tab3_oneperson_vs_lights
from dashboard.tab4_police_count import tab4_police_count
from dashboard.tab5_school_count import tab5_school_count

# 📌 대시보드 제목
st.title("📌 부산시 통합 시각화 대시보드")

# 🗺 CCTV 지도 페이지 안내 (사이드바에서 이동)
st.info("🗺 CCTV 지도는 좌측 사이드바의 '1_CCTV_지도' 페이지에서 확인해주세요.")

# 📊 탭 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 CCTV 분석",
    "💡 가로등 vs 범죄",
    "🏠 1인 가구 vs 가로등",
    "🏫 부산 동별 학교 수",
    "🚓 동별 경찰서 수"
])

with tab1:
    cctv_analysis_page()

with tab2:
    tab2_lights_vs_crime()

with tab3:
    tab3_oneperson_vs_lights()

with tab4:
    tab5_school_count()

with tab5:
    tab4_police_count()
