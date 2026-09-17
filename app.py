from pathlib import Path

import streamlit as st
import pandas as pd


st.set_page_config(
    page_title='판매 대시보드',
    page_icon='🆓',
    layout='wide',
)

TARGET_DIR = 'data'
TARGET_CSV = 'data.csv'

BASE_DIR = Path(__file__).resolve().parent  #프로젝트 루트 디렉토리
DATA_PATH = BASE_DIR/ TARGET_DIR / TARGET_CSV

df = pd.read_csv(DATA_PATH)

st.title('판매 대시보드')

with st.sidebar:
     st.header('조회조건')
     region = st.selectbox(
        '지역', #['전체','서울','대전']
    ['전체','서울','대전'])

     minimum_sales = st.slider('최소매출',
          min_value=0,
          max_value=int(df['sales'].max()),
          value=0,
          step=500_000,)

filtered = df[df['sales'] >= minimum_sales].copy()

if region != '전체':
    filtered = filtered[
        filtered['region'] == region
    ]


## KPI
## 1. 총매출
## 2. 총판매량
## 3. kpi 계산에 사용된 데이터 행수(조회 건수)

# 1. 총매출
total_sales = filtered['sales'].sum()

# 2. 총판매량
total_amount = filtered['quantity'].sum()

# 4. 조회건수
total_rows = len(filtered)

# 3. 평균 매출
if total_rows > 0:
    average_sales = filtered['sales'].mean()
else:
    average_sales = 0

col1, col2, col3, col4 = st.columns(4)

# 1. 총 매출 kpi
with col1:
    st.metric(
        label = '총 매출',
        value = f'{total_sales:,}원',
        border = True, )

with col2:
    st.metric(
        label = '총 판매량',
        value = f'{total_amount:,}개',
        border = True,
    )
with col3:
    st.metric(
        label = '평균 매출',
        value = f'{average_sales:,.0f}원',
        border = True,
    )
with col4:
    st.metric(
        label = '조회건수',
        value = f'{total_rows:,}건',
        border = True,
    )


st.divider()

if filtered.empty:
    st.warning('조건에 맞는 데이터가 없습니다.')
else:

    monthly_sales = filtered.groupby('month')['sales']

    left, right = st.columns([2,1])
    with left:
        st.subheader('월별매출')

        st.line_chart(monthly_sales,
                      x='month',
                      y='sales',)


    with right:
        st.subheader('조회 데이터')

        st.dataframe(filtered,
                     hide_index=True,
                     column_config=
                     {'quantity': st.column_config.NumberColumn()