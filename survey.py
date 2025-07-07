import streamlit as st
import pandas as pd
from datetime import datetime
import os # 파일 존재 여부 확인 및 삭제를 위해 추가

# CSV 파일 경로
CSV_FILE = "survey_responses.csv"

def get_survey_data():
    """기존 설문 응답 데이터를 불러옵니다. 파일이 없으면 빈 DataFrame을 반환합니다."""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

def save_survey_data(data):
    """새로운 응답 데이터를 CSV 파일에 추가합니다."""
    try:
        # 기존 데이터 불러오기
        df = get_survey_data()
        
        # 새로운 응답을 DataFrame으로 변환
        new_row_df = pd.DataFrame([data])

        # 기존 데이터와 새 데이터 합치기
        # 컬럼 순서가 다를 수 있으므로 concat 후 다시 정렬
        updated_df = pd.concat([df, new_row_df], ignore_index=True)
        
        # 모든 컬럼이 문자열 타입이 되도록 변환 (향후 데이터 처리 용이)
        updated_df = updated_df.astype(str)

        updated_df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig') # 한글 깨짐 방지를 위해 'utf-8-sig' 사용
        st.success("설문 응답이 성공적으로 저장되었습니다.")
    except Exception as e:
        st.error(f"CSV 파일 저장 중 오류 발생: {e}")

st.set_page_config(
    page_title="우리 반 설문조사",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("👨‍🏫 우리 반 설문조사 👩‍🏫")
st.write("1학기를 돌아보고 2학기를 더욱 즐겁게 만들기 위한 설문조사입니다. 솔직하게 답변해주세요!")
st.markdown("---")

with st.form(key="class_survey_form"):
    st.subheader("친구에 대한 질문")
    st.write("각 질문에 대해 해당하는 친구 3명을 선택하거나 직접 입력해주세요. (익명으로 진행됩니다.)")

    # 학생 이름 목록 (예시) - 실제 학생 이름으로 변경해주세요.
    # 학생 수가 많다면 이 목록을 파일에서 불러오거나 데이터베이스에서 가져오는 것이 좋습니다.
    student_names = ["선택 안 함", "김철수", "이영희", "박지민", "최현우", "정예은", "이지수", "강민준", "윤서연", "한동현", "기타 직접 입력"]

    # 1. 우리 반에 웃음을 제공해주는 친구(3명)
    st.write("1. 우리 반에 웃음을 제공해주는 친구 (최대 3명)")
    friends_laughter = st.multiselect(
        "웃음을 제공해주는 친구를 선택해주세요:",
        options=student_names,
        key="laughter_friends",
        max_selections=3
    )
    friends_laughter_etc = ""
    if "기타 직접 입력" in friends_laughter:
        friends_laughter_etc = st.text_input("직접 입력 (웃음을 제공해주는 친구):", key="laughter_friends_etc")

    # 2. 우리 반에서 나와 가장 많이 함께한 친구(3명)
    st.write("2. 우리 반에서 나와 가장 많이 함께한 친구 (최대 3명)")
    friends_together = st.multiselect(
        "가장 많이 함께한 친구를 선택해주세요:",
        options=student_names,
        key="together_friends",
        max_selections=3
    )
    friends_together_etc = ""
    if "기타 직접 입력" in friends_together:
        friends_together_etc = st.text_input("직접 입력 (가장 많이 함께한 친구):", key="together_friends_etc")

    # 3. 우리 반에서 가장 친절한 것 같은 친구(3명)
    st.write("3. 우리 반에서 가장 친절한 것 같은 친구 (최대 3명)")
    friends_kind = st.multiselect(
        "가장 친절한 친구를 선택해주세요:",
        options=student_names,
        key="kind_friends",
        max_selections=3
    )
    friends_kind_etc = ""
    if "기타 직접 입력" in friends_kind:
        friends_kind_etc = st.text_input("직접 입력 (가장 친절한 친구):", key="kind_friends_etc")

    # 4. 우리 반에서 나의 비밀을 잘 지켜줄 것 같은 친구(3명)
    st.write("4. 우리 반에서 나의 비밀을 잘 지켜줄 것 같은 친구 (최대 3명)")
    friends_secret = st.multiselect(
        "비밀을 잘 지켜줄 것 같은 친구를 선택해주세요:",
        options=student_names,
        key="secret_friends",
        max_selections=3
    )
    friends_secret_etc = ""
    if "기타 직접 입력" in friends_secret:
        friends_secret_etc = st.text_input("직접 입력 (비밀을 잘 지켜줄 것 같은 친구):", key="secret_friends_etc")

    # 5. 우리 반에서 졸업식 날 눈물을 흘릴 것 같은 친구(3명)
    st.write("5. 우리 반에서 졸업식 날 눈물을 흘릴 것 같은 친구 (최대 3명)")
    friends_cry = st.multiselect(
        "졸업식 날 눈물을 흘릴 것 같은 친구를 선택해주세요:",
        options=student_names,
        key="cry_friends",
        max_selections=3
    )
    friends_cry_etc = ""
    if "기타 직접 입력" in friends_cry:
        friends_cry_etc = st.text_input("직접 입력 (졸업식 날 눈물을 흘릴 것 같은 친구):", key="cry_friends_etc")

    # 6. 우리 반에서 2학기에 더 가까워지고 싶은 친구(3명)
    st.write("6. 2학기에 더 가까워지고 싶은 친구 (최대 3명)")
    friends_closer = st.multiselect(
        "2학기에 더 가까워지고 싶은 친구를 선택해주세요:",
        options=student_names,
        key="closer_friends",
        max_selections=3
    )
    friends_closer_etc = ""
    if "기타 직접 입력" in friends_closer:
        friends_closer_etc = st.text_input("직접 입력 (2학기에 더 가까워지고 싶은 친구):", key="closer_friends_etc")

    st.markdown("---")
    st.subheader("자유 응답 질문")

    # 7. 1학기 동안 기억에 남는 에피소드
    episode = st.text_area("7. 1학기 동안 기억에 남는 에피소드는 무엇인가요?", key="episode")

    # 8. 1학기를 보내며 아쉬웠던 일
    regret = st.text_area("8. 1학기를 보내며 아쉬웠던 일은 무엇인가요?", key="regret")

    # 9. 2학기의 다짐
    resolution = st.text_area("9. 2학기에는 어떤 다짐을 하고 싶나요?", key="resolution")

    # 10. 졸업하기 전에 학급에서 해보고 싶은 일
    wish = st.text_area("10. 졸업하기 전에 학급에서 꼭 해보고 싶은 일이 있다면 알려주세요!", key="wish")

    # 11. 담임선생님에게 하고 싶은 말
    message_to_teacher = st.text_area("11. 담임선생님에게 하고 싶은 말이 있다면 자유롭게 남겨주세요.", key="message_to_teacher")

    st.markdown("---")
    submitted = st.form_submit_button("설문 제출하기")

    if submitted:
        # 각 질문에 대한 답변을 딕셔너리로 저장
        response_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "1. 웃음을 주는 친구": ", ".join([f for f in friends_laughter if f != "기타 직접 입력"]) + (f" ({friends_laughter_etc})" if friends_laughter_etc else ""),
            "2. 가장 많이 함께한 친구": ", ".join([f for f in friends_together if f != "기타 직접 입력"]) + (f" ({friends_together_etc})" if friends_together_etc else ""),
            "3. 가장 친절한 친구": ", ".join([f for f in friends_kind if f != "기타 직접 입력"]) + (f" ({friends_kind_etc})" if friends_kind_etc else ""),
            "4. 비밀을 지켜줄 친구": ", ".join([f for f in friends_secret if f != "기타 직접 입력"]) + (f" ({friends_secret_etc})" if friends_secret_etc else ""),
            "5. 졸업식 날 눈물 흘릴 친구": ", ".join([f for f in friends_cry if f != "기타 직접 입력"]) + (f" ({friends_cry_etc})" if friends_cry_etc else ""),
            "6. 2학기 더 가까워지고 싶은 친구": ", ".join([f for f in friends_closer if f != "기타 직접 입력"]) + (f" ({friends_closer_etc})" if friends_closer_etc else ""),
            "7. 기억에 남는 에피소드": episode,
            "8. 아쉬웠던 일": regret,
            "9. 2학기 다짐": resolution,
            "10. 졸업 전 해보고 싶은 일": wish,
            "11. 담임선생님께 하고 싶은 말": message_to_teacher,
        }

        save_survey_data(response_data)
        st.balloons() # 설문 제출 후 풍선 효과

st.markdown("---")
st.subheader("선생님용: 설문 결과 다운로드")

# 현재까지 저장된 데이터를 불러와서 다운로드 버튼에 연결
current_data = get_survey_data()

if not current_data.empty:
    # DataFrame을 CSV 문자열로 변환 (한글 인코딩 포함)
    csv_string = current_data.to_csv(index=False, encoding='utf-8-sig')
    
    st.download_button(
        label="설문 결과 엑셀(CSV) 파일로 다운로드",
        data=csv_string,
        file_name="class_survey_results.csv",
        mime="text/csv",
        help="클릭하면 현재까지 제출된 모든 설문 응답이 CSV 파일로 다운로드됩니다. 이 파일을 엑셀에서 열 수 있습니다."
    )
    st.info("설문 결과는 'class_survey_results.csv' 파일로 다운로드되며, 이 파일은 Microsoft Excel, Google Sheets 등에서 열 수 있습니다.")
else:
    st.info("아직 제출된 설문 응답이 없습니다.")

# (선택 사항) 설문 결과 미리보기 (선생님만 볼 수 있도록 비밀번호 등으로 보호할 수 있습니다.)
# st.subheader("설문 결과 미리보기 (개발용)")
# st.dataframe(current_data)
