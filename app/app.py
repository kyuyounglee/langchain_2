import streamlit as st
from sommeiler import search_wine, recommand_wine,describe_dish_flavor

st.title('Sommelier AI')

uploaded_image = st.file_uploader('이미지 업로드 하세요')
user_prompt = st.text_input('프롬프트를 입력하세요','이 요리에 잘 어울리는 와인을 추천해 주세요')