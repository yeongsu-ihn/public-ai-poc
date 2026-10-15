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
st.markdown('<p class="sub-text">카테고리를 선택하면 표준 템플릿이 입력창에 즉시 로드되며, 담당자가 직접 수정 및 검토(Human-in-the-Loop)하여 공식 등록합니다.</p>', unsafe_allow_html=True)

# 4. 사이드바 - 기관 설정 및 카테고리 선택
with st.sidebar:
    st.header("⚙️ 기관 설정")
    org_name = st.text_input("소속 기관명", value="○○부/○○청")
    department = st.text_input("작성 부서명", value="기획예산담당관")
    
    st.markdown("---")
    category = st.selectbox(
        "핵심 업무 카테고리 선택",
        ["업무분장", "인사발령", "휴직복직", "예산", "인수인계"]
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Human-in-the-Loop")
    st.write("입력창에 자동 로드된 표준 템플릿을 기관 실정에 맞게 수정하고 [최종 승인] 버튼을 누르면 표준 문서함에 등록됩니다.")

# 5. 카테고리별 기본 템플릿 정의 (실시간 연동)
if category == "업무분장":
    default_template = f"[업무분장] 2026년 상반기 주무관별 담당 사무 지정 ({department})"
elif category == "인사발령":
    default_template = f"[인사발령] 2026년 상반기 정기인사 5급 이하 전보 ({department})"
elif category == "휴직복직":
    default_template = f"[휴직복직] 육아휴직 신청 및 후임자 업무 대행 지정 ({department} 김주무관)"
elif category == "예산":
    default_template = f"[예산] 2026년도 제1회 추가경정예산 편성 요구서 제출 ({department})"
else:
    default_template = f"[인수인계] 2026년도 핵심 업무 및 미결 현안 인수인계서 ({department} 김주무관)"

# 6. 메인 입력 및 편집 영역 (단일 화면 직관적 구조)
st.subheader(f"📝 [{category}] 표준 문서 제목 작성 및 검토")
st.markdown("카테고리에 맞는 표준 템플릿이 아래 입력창에 자동으로 제공됩니다. 필요시 텍스트를 자유롭게 수정하세요.")

# 사용자가 입력창에서 직접 템플릿을 수정할 수 있도록 제공
edited_title = st.text_input(
    "표준 문서 제목 (직접 수정 가능)",
    value=default_template,
    key=f"input_{category}" # 카테고리 변경 시 입력창 초기화 연동
)

col_1, col_2 = st.columns([1, 4])
with col_1:
    approve_btn = st.button("✅ 최종 승인 및 등록", type="primary", use_container_width=True)

if approve_btn:
    st.session_state['is_approved'] = True
    st.session_state['registered_title'] = edited_title

if st.session_state.get('is_approved', False):
    st.success(f"[승인 완료] [{org_name}] 표준 문서함에 아래 제목으로 공식 등록되었으며, 전 부처 검색 표준 메타데이터로 저장되었습니다!")
    st.code(st.session_state.get('registered_title', edited_title))

# 7. 하단 푸터
st.markdown("---")
st.markdown(f"2026 공공 AI 대전환 챌린지 출품작 시제품 (PoC) | 소속 기관: {org_name} | Powered by Streamlit", unsafe_allow_html=True)
