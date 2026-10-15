import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="HRDK-AI 문서기안기",
    page_icon="🏛️",
    layout="wide"
)

# 2. 스타일링 (한글/온나라 전자결재 프로그램 창 스타일 - 서브 텍스트 크기 조정)
st.markdown("""
    <style>
    .program-window {
        background-color: #2b2b2b;
        border: 1px solid #444;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 20px;
    }
    .program-title {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        margin: 0;
    }
    .program-subtitle {
        font-size: 13px;
        color: #8cd3ff;
        margin-top: 4px;
        margin-bottom: 6px;
        font-weight: 500;
    }
    .program-desc {
        font-size: 12px;
        color: #aaaaaa;
        margin-top: 0;
        margin-bottom: 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 사이드바 - 기관 설정 및 카테고리 선택
with st.sidebar:
    st.header("⚙️ 기관 및 메타데이터 설정")
    org_name = st.text_input("소속 기관명", value="한국산업인력공단")
    department = st.text_input("작성 부서명 (비워두면 괄호 생략)", value="일학습출제부")
    
    st.markdown("---")
    category = st.selectbox(
        "핵심 업무 카테고리 선택",
        ["업무분장", "인사발령", "휴직복직", "예산", "인수인계"]
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Human-in-the-Loop 프로세스")
    st.write("1. AI가 제안하는 **표준 제목 및 본문** 확인\n2. 필요시 텍스트 직접 수정\n3. 관련문서 및 붙임 선택 후 **[최종 등록]**")

# 4. 카테고리별 표준 제목 및 표준 본문 자동 생성 매핑
if category == "업무분장":
    default_title_content = "2026년 상반기 주무관별 담당 사무 지정"
    default_body = f"1. 관련 근거: 정부조직법 및 당 기관 사무위임 규정\n2. 2026년도 상반기 부서 내 원활한 업무 추진과 책임 행정 구현을 위하여 다음과 같이 주무관별 담당 사무를 지정하여 운영하고자 합니다.\n\n  가. 대상 부서: {department if department else '해당 부서'}\n  나. 시행 일자: 2026. 3. 1. 기준\n  다. 주요 내용: 단위 과제별 주·보조 담당자 지정 및 상시 협업 체계 구축\n\n3. 각 담당관 및 팀에서는 소관 사무에 차질이 없도록 조치하여 주시기 바랍니다."
elif category == "인사발령":
    default_title_content = "2026년 하반기 정기인사 3급 이하 전보"
    default_body = "1. 관련 근거: 국가공무원법 제28조 및 당 기관 인사운영지침\n2. 2026년 하반기 정기인사를 아래와 같이 단행하여 효율적인 조직 운영과 현장 대응 역량을 강화하고자 합니다.\n\n  가. 인사 발령 대상: 3급 이하 일반직 공무원\n  나. 부서별 배치 인원: 총 00명\n  다. 부임 일자: 2026. 7. 1. 자로\n\n3. 보직 변경에 따른 업무 공백이 발생하지 않도록 인수인계 철저 및 보안 관리에 만전을 기해 주시기 바랍니다."
elif category == "휴직복직":
    default_title_content = "육아휴직 신청 및 후임자 업무 대행 지정 (김주무관)"
    default_body = "1. 관련 근거: 국가공무원 복무규정 및 공무원 임용령\n2. 소속 직원의 육아휴직 신청에 따른 업무 공백을 방지하고 원활한 행정 서비스 유지를 위해 후임자 업무 대행자를 아래와 같이 지정합니다.\n\n  가. 휴직자 성명/직급: 주무관 김○○ (행정사무관)\n  나. 휴직 기간: 2026. 8. 1. ~ 2027. 1. 31. (6개월간)\n  다. 업무 대행자: 주무관 이○○ (지정 완료)\n\n3. 대행자는 휴직 기간 동안 해당 사무를 성실히 수행하여 업무 누수가 발생하지 않도록 조치바랍니다."
elif category == "예산":
    default_title_content = "2026년도 제1회 추가경정예산 편성 요구서 제출"
    default_body = "1. 관련 근거: 국가재정법 및 2026년도 예산편성 지침\n2. 주요 현안 사업 추진 및 시급한 재정 소요에 대응하기 위하여 2026년도 제1회 추가경정예산 편성 요구서를 다음과 같이 제출합니다.\n\n  가. 요구 금액: 금 ○○○백만원 (₩000,000,000)\n  나. 주요 사업명: 공공 AI 문서 관리 시스템 고도화 사업 외 1건\n  다. 산출 내역: [붙임 산출내역서 참고]\n\n3. 원활한 예산 심의 및 확보가 이루어질 수 있도록 관련 부서의 협조를 당부드립니다."
else:
    default_title_content = "2026년도 핵심 업무 및 미결 현안 인수인계서 (김주무관)"
    default_body = "1. 관련 근거: 보안업무규정 및 당 기관 문서관리 지침\n2. 담당자 보직 변경에 따른 업무 연속성 확보와 행정 지식 자산의 안정적 승계를 위해 2026년도 소관 주요 업무 및 미결 현안에 대한 인수인계 결과를 보고합니다.\n\n  가. 인계자: 주무관 김○○ / 인수자: 주무관 박○○\n  나. 주요 인계 내용: 핵심 사업 추진 현황, 예산 집행 내역, 미결 공문 목록\n\n3. 세부 인수인계 내용 및 관련 파일은 별첨 시스템을 참고하시기 바랍니다."

# 5. 프로그램 창 이름 스타일의 상단 배너 적용 (요청하신 계층 구조 반영)
st.markdown(f"""
<div class="program-window">
    <p class="program-title">🏛️ [HRDK-AI 문서기안기]</p>
    <p class="program-subtitle">표준 제목 설정 및 AI 기안 검토기 ({category})</p>
    <p class="program-desc">선택한 업무 유형에 맞는 표준 제목과 본문 초안이 자동으로 생성됩니다. 실정에 맞게 수정 후 검토를 진행하세요.</p>
</div>
""", unsafe_allow_html=True)

# [1파트] 제목 편집 영역
st.markdown("#### 1. 표준 제목 설정")
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    edited_content = st.text_input("핵심 내용 및 목적 편집", value=default_title_content, key=f"title_{category}")
with col_t2:
    use_dept = st.checkbox("부서명 포함", value=True)

# 부서명 유무에 따른 동적 제목 조합
clean_department = department.strip()
if use_dept and clean_department:
    final_title = f"[{category}] {edited_content} ({clean_department})"
else:
    final_title = f"[{category}] {edited_content}"

st.code(final_title, language="text")

st.markdown("---")

# [2파트] 본문 내용 작성 영역
st.markdown("#### 2. 표준 본문 내용 작성 (AI 초안)")
edited_body = st.text_area(
    "공공 표준 격식에 맞춘 본문 내용을 수정할 수 있습니다.",
    value=default_body,
    height=220,
    key=f"body_{category}"
)

st.markdown("---")

# [3파트] 관련문서 및 붙임문서 선택 영역
st.markdown("#### 3. 관련 문서 및 붙임 문서 설정")
col_a, col_b = st.columns(2)

with col_a:
    has_related_doc = st.checkbox("📌 관련 문서 있음", value=True)
    related_doc_text = ""
    if has_related_doc:
        related_doc_text = st.text_input("관련 문서 표시명 입력", value="일학습출제부-1234 (2026. 5. 10.)호 관련")

with col_b:
    has_attachment = st.checkbox("📎 붙임 문서 있음", value=True)
    attachment_text = ""
    if has_attachment:
        attachment_text = st.text_input("붙임 문서명 입력", value="[붙임] 2026년도 세부 추진 계획서 1부.")

st.markdown("---")

# 6. 최종 미리보기 및 등록 버튼 (Human-in-the-Loop)
if st.button("🔍 최종 기안서 미리보기 (검증)", type="primary", use_container_width=True):
    st.session_state['preview_ready'] = True
    st.session_state['is_approved'] = False
    
    # 최종 문서 포맷 조립 (관련문서 -> 본문 -> 붙임 -> 끝)
    full_doc = ""
    if has_related_doc and related_doc_text.strip():
        full_doc += f"산정 근거 및 관련: {related_doc_text}\n\n"
    
    full_doc += f"{edited_body}\n\n"
    
    if has_attachment and attachment_text.strip():
        full_doc += f"{attachment_text}\n\n"
        
    full_doc += "끝."
    
    st.session_state['final_doc_title'] = final_title
    st.session_state['final_doc_body'] = full_doc

# 미리보기 결과 출력
if st.session_state.get('preview_ready', False):
    st.markdown("---")
    st.markdown("#### 🔎 전자문서시스템 최종 기안본 미리보기 (Human-in-the-Loop)")
    st.info("아래의 최종 기안서 양식을 확인하신 후 결재 상신 및 문서함 등록을 진행해 주세요.")
    
    doc_title = st.session_state.get('final_doc_title', '')
    doc_body = st.session_state.get('final_doc_body', '')
    
    st.markdown(f"**[제목]** `{doc_title}`")
    st.markdown("**[본문 내용 및 편제]**")
    st.code(doc_body, language="text")
    
    st.markdown("")
    if st.button("🚀 결재 상신 및 표준 문서함 등록 (실행)", type="primary", use_container_width=True):
        st.session_state['is_approved'] = True

if st.session_state.get('is_approved', False):
    approved_title = st.session_state.get('final_doc_title', '')
    st.success(f"🎉 [{org_name}] 전자결재 상신이 완료되었으며, 표준 메타데이터 문서함에 성공적으로 등록되었습니다!")
    st.markdown(f"**공식 등록된 메타데이터 제목:** `{approved_title}`")

# 7. 하단 푸터
st.markdown("---")
st.markdown(f"2026 공공 AI 대전환 챌린지 출품작 시제품 (PoC) | 소속 기관: {org_name} | Powered by Streamlit", unsafe_allow_html=True)
