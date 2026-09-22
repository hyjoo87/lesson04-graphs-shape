import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

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
# 그래프 2. 장르 안의 영화별 총 관객 (트리맵)
# ==============================================================
st.header("그래프 2. 장르 안의 영화별 총 관객")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>",
)
fig2.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("(여기에 내용을 직접 작성해 주세요.)")

st.divider()

# ==============================================================
# 그래프 3. 총 관객수 분포 (히스토그램)
# ==============================================================
st.header("그래프 3. 총 관객수 분포")

N_BINS = 20

fig3 = px.histogram(df, x="total_audi", nbins=N_BINS)
fig3.update_traces(
    hovertemplate="구간: %{x}<br>영화 편수: %{y}편<extra></extra>",
)
fig3.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    bargap=0.05,
)

st.plotly_chart(fig3, use_container_width=True)

# 대부분의 영화가 몰려 있는 구간 계산
counts, bin_edges = np.histogram(df["total_audi"], bins=N_BINS)
max_idx = counts.argmax()
bin_start, bin_end = bin_edges[max_idx], bin_edges[max_idx + 1]

# 총 관객이 가장 많은 영화 계산
top_movie = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"대부분의 영화는 총 관객 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 몰려 있으며 "
    f"(전체 {len(df)}편 중 **{counts[max_idx]}편**), "
    f"가장 많은 관객을 동원한 영화는 **{top_movie['movieNm']}**"
    f"(총 관객 **{top_movie['total_audi']:,.0f}명**)입니다."
)

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("(여기에 내용을 직접 작성해 주세요.)")

st.divider()

# ==============================================================
# 그래프 4. 개봉일 스크린수와 총 관객의 관계 (산점도)
# ==============================================================
st.header("그래프 4. 개봉일 스크린수와 총 관객의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}관<br>총 관객: %{y:,}명<extra></extra>",
)
fig4.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("(여기에 내용을 직접 작성해 주세요.)")

st.divider()

# ==============================================================
# 그래프 5. 장르별 총 관객 분포 (박스플롯)
# ==============================================================
st.header("그래프 5. 장르별 총 관객 분포")

genre_counts_5 = df["genre"].value_counts()
valid_genres = genre_counts_5[genre_counts_5 >= 10].index
df_box = df[df["genre"].isin(valid_genres)]

fig5 = px.box(
    df_box,
    x="genre",
    y="total_audi",
    hover_name="movieNm",
    points="outliers",
)
fig5.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="장르 (10편 이상)",
    yaxis_title="총 관객 수",
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("(여기에 내용을 직접 작성해 주세요.)")

st.divider()

# ==============================================================
# 그래프 6. 개봉일 스크린수와 총 관객의 관계 (버블 차트)
# ==============================================================
st.header("그래프 6. 개봉일 스크린수와 총 관객의 관계 (첫 주 관객 크기 반영)")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=40,
)
fig6.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}관<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명<extra></extra>"
    ),
)
fig6.update_layout(
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("**📌 이 그래프로 알 수 있는 것:**")
st.info("(여기에 내용을 직접 작성해 주세요.)")

st.divider()

# ==============================================================
# 다음 그래프를 추가할 구역
# (아래에 새로운 그래프를 추가할 때는 st.header(\"그래프 7. ...\") 형태로
#  구역을 나누고, 그래프 아래에 '이 그래프로 알 수 있는 것' 자리를 넣어주세요.)
# ==============================================================
# ── 그래프 7. 국가에서 장르로 (선버스트) ──
st.header("7. 국가에서 장르로 (선버스트)")
df["대표국가"] = df["nation"].str.split("|").str[0]
counted = (df.groupby(["대표국가", "장르"], as_index=False)
             .agg(편수=("movieNm", "count")))
fig7 = px.sunburst(counted, path=["대표국가", "장르"], values="편수")
st.plotly_chart(fig7, width="stretch")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
