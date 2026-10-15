import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="공공 AI 문서함 표준화 솔루션",
    page_icon="🏛️",
    layout="wide"
)

# 2. 스타일링 (공공기관 느낌의 깔끔한 디자인)
st.markdown("""
    <style>
    .main-header { font-size: 24px; font-weight: bold; color: #1f77b4; }
    .sub-text { font-size: 14px; color: #555555; }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더 영역
st.markdown('<p class="main-header">🏛️ 공공기관 문서함 5대 업무 AI 표준화 솔루션</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">비정형 문서 제목과 인수인계 포맷을 단 1초 만에 공공 표준 포맷으로 변환하고, 담당자 승인(Human-in-the-Loop)을 거쳐 등록합니다.</p>', unsafe_allow_html=True)

# 4. 사이드바 - 설정 및 가이드
with st.sidebar:
    st.header("⚙️ 시스템 설정")
    category = st.selectbox(
        "핵심 업무 카테고리 선택",
        ["업무분장", "인사발령", "휴직복직", "예산", "인수인계"]
    )
    
    st.markdown("---")
    st.markdown("### 💡 표준 포맷 규칙")
    st.info("`[업무분류] 핵심 내용 및 목적 (대상/성명/부서) [연도 또는 상태]`")
    
    st.markdown("---")
    st.markdown("### 🎯 Human-in-the-Loop")
    st.write("AI가 제안한 표준 제목을 담당 주무관이 최종 검토 후 [승인]해야 문서함에 공식 등록됩니다.")

# 5. 메인 입력 영역
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 원문 제목(또는 작성 중인 내용) 입력")
    raw_input = st.text_area(
        "자유롭게 작성된 기존 문서 제목을 입력하세요",
        value="[초안] 2026년 상반기 주무관별 담당사무 지정해둔거 기획예산담당관실에서 올립니다 최종최종",
        height=130
    )
    
    department = st.text_input("작성 부서명", value="기획예산담당관")
    
    # AI 변환 버튼
    transform_btn = st.button("✨ AI 표준 제목 자동 생성", type="primary", use_container_width=True)

with col2:
    st.subheader("📤 AI 변환 결과 및 승인 (PoC)")
    
    if transform_btn:
        with st.spinner("AI가 표준 포맷을 분석 및 생성 중입니다... (1초 소요)"):
            time.sleep(1) # 시연용 딜레이
            
            # 카테고리별 스마트 매칭 예시 로직
            if category == "업무분장":
                suggested_title = f"[업무분장] 2026년 상반기 주무관별 담당 사무 지정 ({department})"
            elif category == "인사발령":
                suggested_title = f"[인사발령] 2026년 상반기 정기인사 5급 이하 전보 ({department})"
            elif category == "휴직복직":
                suggested_title = f"[휴직복직] 육아휴직 신청 및 후임자 업무 대행 지정 ({department} 김주무관)"
            elif category == "예산":
                suggested_title = f"[예산] 2026년도 제1회 추가경정예산 편성 요구서 제출 ({department})"
            else:
                suggested_title = f"[인수인계] 2026년도 핵심 업무 및 미결 현안 인수인계서 ({department} 김주무관)"
                
            st.session_state['suggested_title'] = suggested_title
            st.session_state['is_approved'] = False

    if 'suggested_title' in st.session_state:
        st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                <b>제안된 표준 제목:</b><br><br>
                <code style="font-size: 16px; color: #d63384;">{st.session_state['suggested_title']}</code>
            </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ 최종 승인 및 문서함 등록", use_container_width=True):
                st.session_state['is_approved'] = True
        with col_b:
            if st.button("🔄 다시 생성하기", use_container_width=True):
                st.rerun()
                
        if st.session_state.get('is_approved', False):
            st.success("[승인 완료] 표준 문서함에 성공적으로 등록되었으며, 전 부처 검색 표준 메타데이터로 저장되었습니다!")
    else:
        st.info("왼쪽에서 내용을 입력하고 'AI 표준 제목 자동 생성' 버튼을 눌러주세요.")

# 6. 하단 푸터
st.markdown("---")
st.markdown("2026 공공 AI 대전환 챌린지 출품작 시제품 (PoC) | Powered by Streamlit", unsafe_allow_html=True)
