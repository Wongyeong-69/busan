import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

def tab2_lights_vs_crime():
    st.subheader("💡 부산 구별 인구당 가로등 수 비교")

    light_file = "data/가로등현황.csv"
    pop_file = "data/부산광역시 주민등록인구통계_20231231.csv"

    try:
        # 인코딩 직접 지정
        light_df = pd.read_csv(light_file, encoding='utf-8-sig')  # 또는 'cp949'
        pop_df = pd.read_csv(pop_file, encoding='cp949')          # 한글 포함된 엑셀 변환 CSV는 보통 cp949
    except Exception as e:
        st.error(f"❌ 파일 로드 오류: {e}")
        return

    try:
        light_df = light_df.rename(columns={light_df.columns[0]: "구군", light_df.columns[-1]: "가로등수"})
        pop_df = pop_df.rename(columns={pop_df.columns[0]: "구군", pop_df.columns[-1]: "인구수"})

        light_df["가로등수"] = light_df["가로등수"].astype(str).str.replace(",", "").astype(int)
        pop_df["인구수"] = pop_df["인구수"].astype(str).str.replace(",", "").astype(int)

        df = pd.merge(light_df, pop_df, on="구군")
        df["1만명당 가로등 수"] = df["가로등수"] / (df["인구수"] / 10000)
        df = df.sort_values(by="1만명당 가로등 수", ascending=False)
    except Exception as e:
        st.error(f"❌ 데이터 처리 오류: {e}")
        return

    # ✅ 폰트 설정
    font_path = "NanumGothic.ttf"
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())
    else:
        plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    # ✅ 시각화
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df["구군"], df["1만명당 가로등 수"], color="gold")
    ax.set_title("부산 구별 인구 1만명당 가로등 수")
    ax.set_xlabel("구군")
    ax.set_ylabel("1만명당 가로등 수")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    st.pyplot(fig)


    #st.dataframe(df.reset_index(drop=True))




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
