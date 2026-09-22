import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일(openDt)이 여덟 자리 숫자 형식이므로 날짜형으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")

    # 장르가 세로막대 기호(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

# ------------------------------------------------------------
# 제목 및 소개
# ------------------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    """
최근 1년간 박스오피스 10위권에 든 영화 가운데, 이 기간에 개봉한 **216편**의 데이터를 바탕으로
영화들이 어떻게 **분포**하고, 각 항목이 서로 어떤 **관계**를 가지는지 살펴봅니다.
"""
)
st.divider()

# ==============================================================
# 그래프 1. 장르별 영화 편수 (도넛 그래프)
# ==============================================================
st.header("그래프 1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = go.Figure(
    data=[
        go.Pie(
            labels=genre_counts["genre"],
            values=genre_counts["count"],
            hole=0.45,
            hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
        )
    ]
)
fig1.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    legend_title_text="장르",
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("(여기에 내용을 직접 작성해 주세요.)")

st.divider()

# ==============================================================
# 다음 그래프를 추가할 구역
# (아래에 새로운 그래프를 추가할 때는 st.header(\"그래프 2. ...\") 형태로
#  구역을 나누고, 그래프 아래에 '이 그래프로 알 수 있는 것' 자리를 넣어주세요.)
# ==============================================================
