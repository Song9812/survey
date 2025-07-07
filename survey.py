import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. 설문조사 질문 정의 ---
# 앙케이트 문항을 딕셔너리로 정의합니다.
# 'type': 질문 유형 (text, selectbox, slider, radio)
# 'options': selectbox나 radio, slider에 필요한 옵션
survey_questions = {
    "name": {"title": "이름 (선택 사항)", "type": "text"},
    "class_name": {"title": "반 (예: 1학년 3반)", "type": "text"},
    "q1": {"title": "이번 학기 동안 가장 기억에 남는 학급 활동은 무엇인가요?", "type": "text"},
    "q2": {"title": "가장 좋았던 수업은 무엇이었고, 그 이유는 무엇인가요?", "type": "text"},
    "q3": {"title": "다음 학기에 학급에서 어떤 활동을 추가하고 싶으신가요?", "type": "text"},
    "q4": {"title": "본인의 학급 기여도에 대해 5점 척도로 평가해주세요. (1: 전혀 기여하지 못함, 5: 매우 많이 기여함)", "type": "radio", "options": [1, 2, 3, 4, 5]},
    "q5": {"title": "학급 분위기는 전반적으로 어떠했다고 생각하나요?", "type": "selectbox", "options": ["매우 좋았다", "좋았다", "보통이었다", "나빴다", "매우 나빴다"]},
    "q6": {"title": "선생님께 하고 싶은 말이 있다면 자유롭게 적어주세요.", "type": "text"},
}

# --- 2. Streamlit UI 구성 ---
st.set_page_config(page_title="학기말 학급 앙케이트", layout="centered")

st.title("👨‍🏫 학기말 학급 앙케이트")
st.write("이번 학기 동안의 학급 생활에 대한 여러분의 소중한 의견을 듣기 위한 설문입니다.")
st.write("솔직하고 자유로운 답변 부탁드립니다. 답변 내용은 통계적인 목적으로만 사용되며, 개인적인 내용은 공개되지 않습니다.")
st.markdown("---")

with st.form(key='class_survey_form'):
    st.header("✨ 설문 참여")

    # 응답 저장 딕셔너리
    responses = {}

    # 사용자 기본 정보
    responses['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for key, item in survey_questions.items():
        if item["type"] == "text":
            responses[key] = st.text_area(f"{item['title']}", key=key)
        elif item["type"] == "selectbox":
            responses[key] = st.selectbox(f"{item['title']}", item['options'], key=key)
        elif item["type"] == "slider":
            responses[key] = st.slider(f"{item['title']}", min_value=item['options'][0], max_value=item['options'][1], step=1, key=key)
        elif item["type"] == "radio":
            responses[key] = st.radio(f"{item['title']}", item['options'], key=key, horizontal=True)

    st.markdown("---")
    submit_button = st.form_submit_button(label='앙케이트 제출하기')

    if submit_button:
        # 모든 필수 질문에 대한 답변 확인 (필요시 추가)
        # 예시: 이름과 반은 선택 사항으로 두었으므로, 필수로 만들 경우 이곳에서 체크
        # if not responses['name'] or not responses['class_name']:
        #     st.error("이름과 반은 필수 입력 사항입니다.")
        # else:

        # --- 3. 데이터 처리 및 저장 ---
        excel_file = "class_survey_results.xlsx"
        
        # 새로운 응답을 DataFrame으로 변환
        new_df = pd.DataFrame([responses])

        if os.path.exists(excel_file):
            # 파일이 존재하면 기존 데이터를 불러와서 추가
            existing_df = pd.read_excel(excel_file)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            # 파일이 없으면 새 DataFrame을 사용
            updated_df = new_df

        try:
            updated_df.to_excel(excel_file, index=False)
            st.success("앙케이트가 성공적으로 제출되었습니다. 감사합니다!")
            st.balloons() # 제출 성공 시 풍선 애니메이션
            # 제출 후 입력 필드 초기화 (필요시)
            st.experimental_rerun() # 페이지 새로고침으로 입력 필드 초기화
        except Exception as e:
            st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")

st.markdown("---")
st.markdown("© 2024 학급 앙케이트 프로그램")
