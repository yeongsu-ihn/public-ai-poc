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
st.markdown('<p class="sub-text">표준 템플릿 기반으로 제목을 편집한 뒤, 미리보기 검증 과정을 거쳐 안전하게 문서함에 최종 등록합니다.</p>', unsafe_allow_html=True)

# 4. 사이드바 - 기관 설정 및 카테고리 선택
with st.sidebar:
    st.header("⚙️ 기관 및 메타데이터 설정")
    org_name = st.text_input("소속 기관명", value="○○부/○○청")
    department = st.text_input("작성 부서명", value="기획예산담당관")
    
    st.markdown("---")
    category = st.selectbox(
        "핵심 업무 카테고리 선택",
        ["업무분장", "인사발령", "휴직복직", "예산", "인수인계"]
    )
    
    st.markdown("---")
    st.markdown("### 🎯 2단계 검증 프로세스")
    st.write("1. 템플릿 내용 수정 후 **[적용 (미리보기)]** 클릭\n2. 변환 결과 확인 후 **[최종 등록 (실행)]**")

# 5. 카테고리별 핵심 내용 템플릿 정의 (부서/카테고리 중복 제거 깔끔한 포맷)
if category == "업무분장":
    default_content = "2026년 상반기 주무관별 담당 사무 지정"
elif category == "인사발령":
    default_content = "2026년 하반기 정기인사 3급 이하 전보"
elif category == "휴직복직":
    default_content = "육아휴직 신청 및 후임자 업무 대행 지정 (김주무관)"
elif category == "예산":
    default_content = "2026년도 제1회 추가경정예산 편성 요구서 제출"
else:
    default_content = "2026년도 핵심 업무 및 미결 현안 인수인계서 (김주무관)"

# 6. 메인 편집 영역
st.subheader(f"📝 [{category}] 표준 문서 제목 편집기")
st.markdown("템플릿의 핵심 내용을 기관 실정에 맞게 수정해주세요. (카테고리 및 부서명은 자동 조합됩니다)")

# 사용자가 핵심 내용만 자유롭게 수정
edited_content = st.text_input(
    "핵심 내용 및 목적 편집",
    value=default_content,
    key=f"content_{category}"
)

# 최종 조합될 완성본 실시간 계산
final_preview_title = f"[{category}] {edited_content} ({department})"

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    preview_btn = st.button("🔍 적용 (결과 미리보기)", use_container_width=True)

if preview_btn:
    st.session_state['preview_ready'] = True
    st.session_state['preview_title'] = final_preview_title
    st.session_state['is_approved'] = False # 새로 적용하면 승인 초기화

# 미리보기 상태일 때 하단에 검증 영역 표시
if st.session_state.get('preview_ready', False):
    st.markdown("---")
    st.markdown("#### 🔎 표준화 결과 미리보기 (Human-in-the-Loop 검증)")
    st.info("아래 생성된 최종 메타데이터 형식을 확인하신 후 문제가 없다면 **[최종 등록 (실행)]** 버튼을 눌러주세요.")
    
    st.code(st.session_state['preview_title'], language="text")
    
    if st.button("🚀 최종 등록 (실행)", type="primary", use_container_width=True):
        st.session_state['is_approved'] = True

if st.session_state.get('is_approved', False):
    st.success(f"🎉 [{org_name}] 표준 문서함에 성공적으로 등록되었습니다!")
    st.markdown(f"**등록된 공식 메타데이터:** `{st.session_state.get('preview_title')}`")

# 7. 하단 푸터
st.markdown("---")
st.markdown(f"2026 공공 AI 대전환 챌린지 출품작 시제품 (PoC) | 소속 기관: {org_name} | Powered by Streamlit", unsafe_allow_html=True)
