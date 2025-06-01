import streamlit as st
from mysommeiler import search_wine, recommand_wine,describe_dish_flavor
import base64

st.title('Sommelier AI')
col1, col2 = st.columns([3, 1])

with col1:
    uploaded_image = st.file_uploader('이미지 업로드 하세요', type=['jpg', 'jpeg', 'png'])
    user_prompt = st.text_input('프롬프트를 입력하세요', '이 요리에 잘 어울리는 와인을 추천해 주세요')

with col2:
    if uploaded_image:
        st.image(uploaded_image,caption='업로드된 요리 이미지', use_container_width=True)    

with col1:  # 같은 with 절은 동일하게 동작
    if st.button('추천하기'):
        if not uploaded_image:
            st.warning('이미지를 업로드 해주세요')
        else:
            with st.spinner('1단계 : 요리의 맛과 향을 분석하는 중...'):
                # 이미지 데이터를 base64로 변환 (byte → base64 문자열)
                image_bytes = uploaded_image.read()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')

                # 함수에 base64 문자열과 사용자 텍스트 전달
                dish_flavor = describe_dish_flavor(base64_image, '이 요리의 맛과 향과 같은 특징을 한글로 분석해 주세요')

                st.markdown('### 요리의 맛과 향 분석 결과')
                st.info(dish_flavor)

            with st.spinner('2단계 : 요리에 어울리는 와인 리뷰를 검색하는 중...'):
                wine_search_result = search_wine(dish_flavor)
                st.markdown('###  와인 리뷰 검색 결과')
                st.text(wine_search_result['wine_reviews'])

            with st.spinner('3단계 : AI 소믈리에가 와인 페어링에 대한 추천 와인을 생성하는 중...'):
                pass

            st.success('추천이 완료되었습니다!')