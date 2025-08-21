import streamlit as st
import pandas as pd
import datetime

# --- 데이터 저장소 ---
# 건의 내용을 저장할 세션 상태 초기화
if 'public_suggestions' not in st.session_state:
    st.session_state.public_suggestions = pd.DataFrame(columns=['이름', '내용', '날짜', '댓글'])
if 'private_suggestions' not in st.session_state:
    st.session_state.private_suggestions = pd.DataFrame(columns=['이름', '내용', '날짜'])

# --- 제목 및 설명 ---
st.title("온라인 건의함 📝")
st.write("여러분의 소중한 의견을 남겨주세요.")

# --- 탭 구성: 건의하기와 공개 건의함 보기 ---
tab1, tab2 = st.tabs(["건의하기", "공개 건의함 보기"])

with tab1:
    st.header("새로운 의견 제출")
    
    # 건의함 종류 선택 (라디오 버튼)
    suggestion_type = st.radio(
        "어떤 건의함에 의견을 남기시겠습니까?",
        ("공개 건의함 (모두가 볼 수 있음)", "비공개 건의함 (나만 볼 수 있음)")
    )
    
    # 이름 입력 (선택 사항)
    is_anonymous_post = st.checkbox("익명으로 제출")
    if is_anonymous_post:
        name_input = "익명"
    else:
        name_input = st.text_input("이름", placeholder="이름을 입력해주세요")
    
    # 건의 내용 입력
    suggestion_text = st.text_area("건의 내용", placeholder="내용을 입력해주세요", height=150)
    
    # 제출 버튼
    if st.button("제출"):
        if not suggestion_text.strip():
            st.error("내용을 입력해 주세요.")
        else:
            new_suggestion = {
                '이름': name_input,
                '내용': suggestion_text,
                '날짜': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '댓글': []  # 새로운 댓글 리스트 추가
            }
            
            # 선택한 건의함에 따라 데이터 저장
            if suggestion_type == "공개 건의함 (모두가 볼 수 있음)":
                st.session_state.public_suggestions = pd.concat(
                    [st.session_state.public_suggestions, pd.DataFrame([new_suggestion])],
                    ignore_index=True
                )
                st.success("공개 건의함에 의견이 제출되었습니다. 다른 사람의 의견도 확인해 보세요!")
            else:
                st.session_state.private_suggestions = pd.concat(
                    [st.session_state.private_suggestions, pd.DataFrame([new_suggestion])],
                    ignore_index=True
                )
                st.success("비공개 건의함에 의견이 제출되었습니다. 내용은 안전하게 전달되었습니다.")
            
            # 입력 필드 초기화 (필요시)
            # st.experimental_rerun()

with tab2:
    st.header("공개 건의함")
    if not st.session_state.public_suggestions.empty:
        # 최신 글이 위로 오도록 정렬
        display_df = st.session_state.public_suggestions.sort_values(by='날짜', ascending=False)
        
        # 각 건의 내용에 대한 UI 생성
        for index, row in display_df.iterrows():
            st.subheader(f"🗣️ {row['이름']}")
            st.write(f"**날짜:** {row['날짜']}")
            st.write(f"**내용:** {row['내용']}")
            
            # 댓글 목록 및 댓글 작성 폼
            with st.expander(f"댓글 ({len(row['댓글'])}) 보기"):
                if row['댓글']:
                    for comment in row['댓글']:
                        st.markdown(f"**{comment['이름']}**: {comment['내용']}")
                else:
                    st.write("아직 댓글이 없습니다.")

            # 댓글 작성 폼
            with st.form(key=f"comment_form_{index}"):
                st.write("댓글 달기")
                comment_name = st.text_input("이름", key=f"name_{index}")
                is_anonymous_comment = st.checkbox("익명으로 댓글 달기", key=f"anonymous_{index}")
                if is_anonymous_comment:
                    comment_name = "익명"

                comment_text = st.text_area("댓글 내용", height=50, key=f"comment_{index}")
                submit_comment = st.form_submit_button("댓글 제출")

                if submit_comment:
                    if not comment_text.strip():
                        st.error("댓글 내용을 입력해 주세요.")
                    else:
                        new_comment = {
                            '이름': comment_name,
                            '내용': comment_text
                        }
                        
                        # 원본 DataFrame의 댓글 리스트에 새 댓글 추가
                        # 인덱스를 통해 해당 행의 '댓글' 리스트를 업데이트
                        st.session_state.public_suggestions.at[index, '댓글'].append(new_comment)
                        st.success("댓글이 성공적으로 제출되었습니다!")
                        st.rerun() # 댓글이 바로 화면에 반영되도록 페이지 새로고침
    else:
        st.info("아직 공개된 의견이 없습니다. 첫 번째 의견을 남겨보세요!")