import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="공공 AI 문서함 템플릿 표준화 솔루션",
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
st.markdown('<p class="main-header">🏛️ 공공기관 문서함 5대 업무 AI 표준 템플릿 솔루션</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">기관별 자율성을 보장하는 표준 템플릿 기반으로 AI가 메타데이터를 매칭하고, 담당자가 직접 검토·수정하여 공식 등록합니다.</p>', unsafe_allow_html=True)

# 4. 사이드바 - 설정 및 기관별 템플릿 가이드
with st.sidebar:
    st.header("⚙️ 기관 설정 및 템플릿 규칙")
    org_name = st.text_input("소속 기관명", value="○○부/○○청")
    
    category = st.selectbox(
        "핵심 업무 카테고리 선택",
        ["업무분장", "인사발령", "휴직복직", "예산", "인수인계"]
    )
    
    st.markdown("---")
    st.markdown("### 📋 기관별 표준 템플릿 구조")
    if category == "업무분장":
        st.info("`[업무분장] {연도}년 {시기} 주무관별 담당 사무 지정 ({부서명})`")
    elif category == "인사발령":
        st.info("`[인사발령] {연도}년 {시기} 정기인사 {직급} 전보 ({부서명})`")
    elif category == "휴직복직":
        st.info("`[휴직복직] {사유} 신청 및 후임자 업무 대행 지정 ({부서명} {성명})`")
    elif category == "예산":
        st.info("`[예산] {연도}년도 {회차} {내용} 요구서 제출 ({부서명})`")
    else:
        st.info("`[인수인계] {연도}년도 {업무명} 인수인계서 ({부서명} {성명})`")
        
    st.markdown("---")
    st.markdown("### 🎯 Human-in-the-Loop")
    st.write("AI가 매칭한 초안 템플릿을 담당 주무관이 기관 실정에 맞게 **직접 수정**한 후 최종 승인합니다.")

# 5. 메인 입력 영역
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 원문 제목(또는 작성 중인 내용) 입력")
    raw_input = st.text_area(
        "자유롭게 작성된 기존 문서 제목이나 내용을 입력하세요",
        value="[초안] 2026년 상반기 주무관별 담당사무 지정해둔거 기획예산담당관실에서 올립니다 최종최종",
        height=130
    )
    
    department = st.text_input("작성 부서명", value="기획예산담당관")
    officer_name = st.text_input("담당자 성명 및 직급", value="김주무관")
    
    # AI 초안 매칭 버튼
    transform_btn = st.button("✨ AI 표준 템플릿 초안 매칭", type="primary", use_container_width=True)

with col2:
    st.subheader("📤 표준 템플릿 편집 및 승인 (PoC)")
    
    if transform_btn:
        with st.spinner("AI가 기관 표준 템플릿에 맞춰 키워드를 분석 및 매칭 중입니다..."):
            time.sleep(1) # 시연용 딜레이
            
            # 카테고리별 스마트 템플릿 매칭 초안 로직
            if category == "업무분장":
                default_draft = f"[업무분장] 2026년 상반기 주무관별 담당 사무 지정 ({department})"
            elif category == "인사발령":
                default_draft = f"[인사발령] 2026년 상반기 정기인사 5급 이하 전보 ({department})"
            elif category == "휴직복직":
                default_draft = f"[휴직복직] 육아휴직 신청 및 후임자 업무 대행 지정 ({department} {officer_name})"
            elif category == "예산":
                default_draft = f"[예산] 2026년도 제1회 추가경정예산 편성 요구서 제출 ({department})"
            else:
                default_draft = f"[인수인계] 2026년도 예산관리 업무 인수인계서 ({department} {officer_name})"
                
            st.session_state['editable_title'] = default_draft
            st.session_state['is_approved'] = False

    if 'editable_title' in st.session_state:
        st.markdown("##### ✏️ AI 제안 초안 (기관 맞춤형 수정 가능)")
        # 사용자가 직접 내용을 고칠 수 있는 텍스트 입력창 제공 (Human-in-the-Loop 핵심)
        user_modified_title = st.text_input(
            "필요시 아래에서 제목을 기관 실정에 맞게 수정하세요:",
            value=st.session_state['editable_title']
        )
        
        st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ 최종 승인 및 문서함 등록", use_container_width=True):
                st.session_state['final_registered_title'] = user_modified_title
                st.session_state['is_approved'] = True
        with col_b:
            if st.button("🔄 초안 다시 생성하기", use_container_width=True):
                st.rerun()
                
        if st.session_state.get('is_approved', False):
            st.success(f"[승인 완료] [{org_name}] 표준 문서함에 아래 제목으로 공식 등록되었습니다!")
            st.code(st.session_state['final_registered_title'])
    else:
        st.info("왼쪽에서 원문을 입력하고 'AI 표준 템플릿 초안 매칭' 버튼을 눌러주세요.")

# 6. 하단 푸터
st.markdown("---")
st.markdown(f"2026 공공 AI 대전환 챌린지 출품작 시제품 (PoC) | 소속 기관: {org_name} | Powered by Streamlit", unsafe_allow_html=True)
