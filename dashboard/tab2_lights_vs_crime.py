import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정
font_path = "NanumGothic.ttf"
if os.path.exists(font_path):
    fontprop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    st.error("❌ NanumGothic.ttf 폰트 파일이 존재하지 않습니다.")
    st.stop()

# ✅ 인구수 데이터
population_dict = {
    "중부": 11786, "동래": 35220, "영도": 20116, "동부": 18603,
    "부산진": 70609, "서부": 20760, "남부": 40521, "해운대": 50516,
    "사상": 36299, "금정": 40412, "사하": 46442, "연제": 30846,
    "강서": 17355, "북부": 36975, "기장": 22500
}

# ✅ 가로등 수 데이터
lights_dict = {
    "중부": 5112, "동래": 8499, "영도": 3220, "동부": 4018,
    "부산진": 9720, "서부": 3876, "남부": 5211, "해운대": 10333,
    "사상": 5891, "금정": 6715, "사하": 7342, "연제": 6384,
    "강서": 3456, "북부": 7030, "기장": 4881
}

# ✅ 데이터 처리
@st.cache_data
def load_data():
    df = pd.read_csv("data/경찰청_부산경찰서별_범죄현황_UTF8.csv")
    df = df.rename(columns={"경찰서": "구"})
    df = df[df["구"].notna()]
    df["구"] = df["구"].astype(str)
    df["인구수"] = df["구"].map(population_dict)
    df["가로등수"] = df["구"].map(lights_dict)
    df = df[df["인구수"].notna() & df["가로등수"].notna()]
    df["범죄율(1만명당)"] = (df["합계"] / df["인구수"]) * 10000
    return df

# ✅ 탭 함수
def tab2_lights_vs_crime():
    st.subheader("💡 구별 가로등 수 대비 범죄율 비교")

    df = load_data()
    df = df.sort_values("범죄율(1만명당)", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df["구"], df["범죄율(1만명당)"], color="salmon")
    ax.set_title("부산 구별 인구 1만명당 범죄율", fontproperties=fontprop)
    ax.set_xlabel("구", fontproperties=fontprop)
    ax.set_ylabel("범죄율 (인구 1만명당)", fontproperties=fontprop)
    ax.set_xticklabels(df["구"], rotation=45, fontproperties=fontprop)

    st.pyplot(fig)



# # dashboard/tab2_lights_vs_crime.py

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# import os
# import urllib.request

# # ─── 한글 폰트 설정 ───
# win_font = "C:\\Windows\\Fonts\\malgun.ttf"
# if os.path.exists(win_font):
#     font_path = win_font
# else:
#     font_path = "NanumGothic.ttf"
#     if not os.path.exists(font_path):
#         try:
#             url = (
#                 "https://github.com/naver/nanumfont/"
#                 "blob/master/ttf/NanumGothic.ttf?raw=true"
#             )
#             urllib.request.urlretrieve(url, font_path)
#         except Exception as e:
#             st.error(f"❌ 한글 폰트 로드 실패: {e}")
#             font_path = None

# # ✅ FontProperties 객체로 폰트 설정
# if font_path:
#     fontprop = fm.FontProperties(fname=font_path)
#     plt.rcParams['axes.unicode_minus'] = False
# else:
#     fontprop = None

# # ─── 데이터 로더 ───
# @st.cache_data
# def load_lights_data(path="data/가로등현황.csv"):
#     df = pd.read_csv(path, encoding="utf-8")
#     df.columns = df.columns.str.strip()
#     df = df.dropna(axis=1, how='all')
#     if '관리부서' in df.columns:
#         df = df.rename(columns={'관리부서': '지역'})
#     else:
#         df = df.rename(columns={df.columns[-2]: '지역'})
#     sum_cols = [c for c in df.columns if '합계' in c]
#     if not sum_cols:
#         raise KeyError(f"❌ 가로등 합계 칼럼을 찾을 수 없습니다: {df.columns.tolist()}")
#     df = df.rename(columns={sum_cols[0]: '합계_가로등'})
#     return df[['지역', '합계_가로등']]

# @st.cache_data
# def load_crime_data(path="data/경찰청_범죄현황.csv"):
#     df = pd.read_csv(path, encoding="utf-8")
#     df.columns = df.columns.str.strip()
#     crime_keys = ["살인", "강도", "성범죄", "폭력"]
#     df['합계_범죄'] = df[crime_keys].sum(axis=1)
#     if '지역' not in df.columns:
#         for c in df.columns:
#             if "관서" in c or "지역" in c:
#                 df = df.rename(columns={c: '지역'})
#                 break
#     return df[['지역', '합계_범죄']]

# # ─── 탭 함수 ───
# def tab2_lights_vs_crime():
#     st.subheader("지역별 가로등 수 vs 5대 범죄 발생 수")

#     try:
#         df_l = load_lights_data()
#         df_c = load_crime_data()

#         merged = pd.merge(df_l, df_c, on='지역')

#         fig, ax = plt.subplots(figsize=(12, 6), dpi=80)
#         ax.plot(merged['지역'], merged['합계_가로등'], marker='o', label='가로등 수', color='green')
#         ax.plot(merged['지역'], merged['합계_범죄'], marker='s', label='범죄 발생 수', color='red')

#         ax.set_xticks(range(len(merged)))
#         ax.set_xticklabels(merged['지역'], rotation=45, fontproperties=fontprop)
#         ax.set_xlabel("지역", fontproperties=fontprop)
#         ax.set_ylabel("건수", fontproperties=fontprop)
#         ax.set_title("지역별 가로등 수와 범죄 발생 수 비교", fontproperties=fontprop)
#         ax.legend(prop=fontprop)
#         ax.grid(True)

#         st.pyplot(fig)

#     except Exception as e:
#         st.error(f"❌ 범죄/가로등 시각화 오류: {type(e).__name__}: {e}")
