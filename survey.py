import streamlit as st
import pandas as pd
from datetime import datetime
import os # 파일 존재 여부 확인 및 삭제를 위해 추가

# --- 설정 ---
# CSV 파일 경로 (Streamlit 앱이 실행되는 동일 디렉토리에 저장됩니다.)
CSV_FILE = "survey_responses.csv"

# 학생 이름 목록 (예시) - 실제 학생 이름으로 변경해주세요!
# 학생 수가 많다면 이 목록을 파일에서 불러오거나 다른 곳에서 관리하는 것이 좋습니다.
STUDENT_NAMES = [
    "선택 안 함", "김철수", "이영희", "박지민", "최현우", "정예은", 
    "이지수", "강민준", "윤서연", "한동현", "서아영", "김준", "박채원", 
    "이도윤", "최유진", "정재민", "문성민", "고은서", "조하준", "임지아",
    "기타 직접 입력"
]

# --- 데이터 로드 및 저장 함수 ---
def get_survey_data():
    """
    기존 설문 응답 데이터를 불러옵니다.
    파일이 없으면 빈 DataFrame을 반환합니다.
    한글 깨짐 방지를 위해 'utf-8-sig' 인코딩으로 시도합니다.
    """
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE, encoding='utf-8-sig')
        except UnicodeDecodeError:
            # utf-8-sig로 읽기 실패 시, 다른 인코딩으로 시도할 수 있지만,
            # 대부분의 경우 utf-8-sig가 Excel 호환성을 높여줍니다.
            st.warning(f"'{CSV_FILE}' 파일을 'utf-8-sig'로 읽는 데 실패했습니다. 'utf-8'로 다시 시도합니다.")
            return pd.read_csv(CSV_FILE, encoding='utf-8')
        except Exception as e:
            st.error(f"CSV 파일 로드 중 예상치 못한 오류 발생: {e}")
            return pd.DataFrame() # 오류 발생 시 빈 DataFrame 반환
    return pd.DataFrame()

def save_survey_data(data):
    """
    새로운 응답 데이터를 CSV 파일에 추가합니다.
    한글 깨짐 방지를 위해 'utf-8-sig' 인코딩을 사용합니다.
    """
    try:
        df = get_survey_data() # 기존 데이터 불러오기
        
        # 새로운 응답을 DataFrame으로 변환
        new_row_df = pd.DataFrame([data])

        # 기존 데이터와 새 데이터 합치기
        # 컬럼 순서가 다를 수 있으므로 concat 후 다시 정렬
        updated_df = pd.concat([df, new_row_df], ignore_index=True)
        
        # 모든 컬럼이 문자열 타입이 되도록 변환 (데이터 일관성 유지)
        updated_df = updated_df.astype(str)

        # ⭐️ 중요: 한글 깨짐 방지를 위해 'utf-8-sig' 사용
        updated_df.to_csv(CSV_FILE, index=False, encoding='utf-8-sig') 
        st.success("설문 응답이 성공적으로 저장되었습니다.")
    except Exception as e:
        st.error(f"CSV 파일 저장 중 오류 발생: {e}")

# --- Streamlit 페이지 설정 ---
st.set_page_config(
    page_title="우리 반 설문조사", # 브라우저 탭에 표시되는 제목
    layout="centered", # 페이지 레이아웃 (wide 또는 centered)
    initial_sidebar_state="auto", # 사이드바 초기 상태 (auto, expanded, collapsed)
)

st.title("👨‍🏫 우리 반 설문조사 👩‍🏫")
st.write("1학기를 돌아보고 2학기를 더욱 즐겁게 만들기 위한 설문조사입니다. 솔직하게 답변해주세요!")
st.markdown("---")

# --- 설문 폼 ---
with st.form(key="class_survey_form"):
    st.subheader("친구에 대한 질문")
    st.write("각 질문에 대해 해당하는 친구 **최대 3명**을 선택하거나 직접 입력해주세요. (익명으로 진행됩니다.)")

    # 1. 우리 반에 웃음을 제공해주는 친구(3명)
    st.markdown("**1. 우리 반에 웃음을 제공해주는 친구**")
    friends_laughter = st.multiselect(
        "웃음을 제공해주는 친구를 선택해주세요:",
        options=STUDENT_NAMES,
        key="laughter_friends",
        max_selections=3
    )
    friends_laughter_etc = ""
    if "기타 직접 입력" in friends_laughter:
        friends_laughter_etc = st.text_input("직접 입력 (웃음을 제공해주는 친구):", key="laughter_friends_etc")

    # 2. 우리 반에서 나와 가장 많이 함께한 친구(3명)
    st.markdown("**2. 우리 반에서 나와 가장 많이 함께한 친구**")
    friends_together = st.multiselect(
        "가장 많이 함께한 친구를 선택해주세요:",
        options=STUDENT_NAMES,
        key="together_friends",
        max_selections=3
    )
    friends_together_etc = ""
    if "기타 직접 입력" in friends_together:
        friends_together_etc = st.text_input("직접 입력 (가장 많이 함께한 친구):", key="together_friends_etc")

    # 3. 우리 반에서 가장 친절한 것 같은 친구(3명)
    st.markdown("**3. 우리 반에서 가장 친절한 것 같은 친구**")
    friends_kind = st.multiselect(
        "가장 친절한 친구를 선택해주세요:",
        options=STUDENT_NAMES,
        key="kind_friends",
        max_selections=3
    )
    friends_kind_etc = ""
    if "기타 직접 입력" in friends_kind:
        friends_kind_etc = st.text_input("직접 입력 (가장 친절한 친구):", key="kind_friends_etc")

    # 4. 우리 반에서 나의 비밀을 잘 지켜줄 것 같은 친구(3명)
    st.markdown("**4. 우리 반에서 나의 비밀을 잘 지켜줄 것 같은 친구**")
    friends_secret = st.multiselect(
        "비밀을 잘 지켜줄 것 같은 친구를 선택해주세요:",
        options=STUDENT_NAMES,
        key="secret_friends",
        max_selections=3
    )
    friends_secret_etc = ""
    if "기타 직접 입력" in friends_secret:
        friends_secret_etc = st.text_input("직접 입력 (비밀을 잘 지켜줄 것 같은 친구):", key="secret_friends_etc")

    # 5. 우리 반에서 졸업식 날 눈물을 흘릴 것 같은 친구(3명)
    st.markdown("**5. 우리 반에서 졸업식 날 눈물을 흘릴 것 같은 친구**")
    friends_cry = st.multiselect(
        "졸업식 날 눈물을 흘릴 것 같은 친구를 선택해주세요:",
        options=STUDENT_NAMES,
        key="cry_friends",
        max_selections=3
    )
    friends_cry_etc = ""
    if "기타 직접 입력" in friends_cry:
        friends_cry_etc = st.text_input("직접 입력 (졸업식 날 눈물을 흘릴 것 같은 친구):", key="cry_friends_etc")

    # 6. 우리 반에서 2학기에 더 가까워지고 싶은 친구(3명)
    st.markdown("**6. 2학기에 더 가까워지고 싶은 친구**")
    friends_closer = st.multiselect(
        "2학기에 더 가까워지고 싶은 친구를 선택해주세요:",
        options=STUDENT_NAMES,
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
    submitted = st.form_submit_button("설문 제출하기 ✅")

    if submitted:
        # 각 질문에 대한 답변을 딕셔너리로 저장
        response_data = {
            "제출 시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
        st.rerun() # 제출 후 페이지 새로고침 (폼 초기화)

st.markdown("---")
st.subheader("📊 선생님용: 설문 결과 다운로드")

# 현재까지 저장된 데이터를 불러와서 다운로드 버튼에 연결
current_data = get_survey_data()

if not current_data.empty:
    # DataFrame을 CSV 문자열로 변환 (한글 인코딩 포함)
    csv_string = current_data.to_csv(index=False, encoding='utf-8-sig')
    
    st.download_button(
        label="설문 결과 엑셀(CSV) 파일로 다운로드 📥",
        data=csv_string,
        file_name="우리반_설문조사_결과.csv", # 파일명에 한글 포함 (다운로드 시에도 깨지지 않음)
        mime="text/csv",
        help="클릭하면 현재까지 제출된 모든 설문 응답이 CSV 파일로 다운로드됩니다. 이 파일을 엑셀에서 열 수 있습니다."
    )
    st.info(f"설문 결과는 '{current_data.shape[0]}'개의 응답으로 구성되어 있으며, '우리반_설문조사_결과.csv' 파일로 다운로드됩니다.")
    st.warning("⚠️ **주의**: 이 앱을 온라인에 배포하는 경우, 서버가 재시작될 때 CSV 파일이 초기화될 수 있습니다. 지속적인 데이터 저장을 위해서는 Google Sheets와 같은 외부 데이터베이스 연결을 고려해주세요.")

    # (선택 사항) 설문 결과 미리보기 (선생님만 볼 수 있도록 비밀번호 등으로 보호할 수 있습니다.)
    # st.markdown("---")
    # st.subheader("전체 응답 미리보기")
    # if st.checkbox("미리보기 보기"): # 체크박스를 눌러야 미리보기 보이게
    #     st.dataframe(current_data, use_container_width=True)
else:
    st.info("아직 제출된 설문 응답이 없습니다. 첫 번째 설문 응답을 기다리고 있습니다! 😊")
