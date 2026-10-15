import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="HRDK-AI 문서기안기",
    page_icon="🤖",
    layout="wide"
)

# 2. 고급 AI 테크 감성 스타일링 (Custom CSS & Glassmorphism)
st.markdown("""
    <style>
    /* 전체 배경 톤 및 폰트 감성 정돈 */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #121824 0%, #0b0f17 90%);
        color: #e2e8f0;
    }
    
    /* 사이드바 스타일링 */
    [data-testid="stSidebar"] {
        background-color: #0f141d;
        border-right: 1px solid rgba(56, 189, 248, 0.15);
    }

    /* 프로그램 창 / 글래스모피즘 카드 스타일 */
    .program-window {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37), inset 0 0 12px rgba(56, 189, 248, 0.05);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }
    .program-title {
        font-size: 22px;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .program-subtitle {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 6px;
        margin-bottom: 0;
        font-weight: 400;
    }

    /* 입력 필드 및 텍스트 영역 테두리 감성 부여 */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.25) !important;
    }

    /* 버튼 네온 그라데이션 스타일 */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
        transition: all 0.3s ease;
    }
    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6);
        transform: translateY(-1px);
    }
    
    /* 코드 박스 (미리보기) 사이버틱한 테두리 */
    pre {
        background-color: #090d16 !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 사이드바 - 기관 설정 및 카테고리 선택
with st.sidebar:
    st.markdown("### ⚙️ 시스템 환경 설정")
    org_name = st.text_input("소속 기관명", value="한국산업인력공단")
    department = st.text_input("작성 부서명 (비워두면 괄호 생략)", value="일학습출제부")
    
    st.markdown("---")
    category = st.selectbox(
        "✨ 핵심 업무 카테고리 선택",
        ["업무분장", "인사발령", "휴직복직", "예산", "인수인계"]
    )
    
    st.markdown("---")
    st.markdown("### 🧠 AI 워크플로우 (HITL)")
    st.caption("1. 다중 본문 항 동적 추가 및 편집\n2. 관련문서 및 붙임 포함 여부 선택\n3. 최종 버튼 클릭 시 공공 표준 서식 자동 조합")

# 이전 카테고리와 현재 카테고리가 다르면 세션 상태 초기화 (입력 칸 꼬임 방지)
if 'prev_category' not in st.session_state:
    st.session_state['prev_category'] = category

if st.session_state['prev_category'] != category:
    st.session_state['prev_category'] = category
    # 기존 입력 세션들 클리어
    keys_to_clear = [k for k in st.session_state.keys() if 'body_paragraphs_' in k or 'attach_list_' in k or 'related_list_' in k]
    for k in keys_to_clear:
        del st.session_state[k]
    st.rerun()

# 4. 카테고리별 초기 본문 및 기본 붙임 문서 매핑
if category == "업무분장":
    default_title_content = "2026년 상반기 주무관별 담당 사무 지정"
    initial_body_paragraphs = [
        f"부서 내 원활한 업무 추진과 책임 행정 구현을 위하여 다음과 같이 주무관별 담당 사무를 지정하여 운영하고자 합니다.\n\n  가. 대상 부서: {department if department else '해당 부서'}\n  나. 시행 일자: 2026. 3. 1. 기준\n  다. 주요 내용: 단위 과제별 주·보조 담당자 지정 및 상시 협업 체계 구축",
        "각 담당관 및 팀에서는 소관 사무에 차질이 없도록 조치하여 주시기 바랍니다."
    ]
    default_attach = "2026년도 상반기 주무관별 담당 사무 내역서 1부."
elif category == "인사발령":
    default_title_content = "2026년 하반기 정기인사 3급 이하 전보"
    initial_body_paragraphs = [
        "2026년 하반기 정기인사를 아래와 같이 단행하여 효율적인 조직 운영과 현장 대응 역량을 강화하고자 합니다.\n\n  가. 인사 발령 대상: 3급 이하 일반직 공무원\n  나. 부서별 배치 인원: 총 00명\n  다. 부임 일자: 2026. 7. 1. 자로",
        "보직 변경에 따른 업무 공백이 발생하지 않도록 인수인계 철저 및 보안 관리에 만전을 기해 주시기 바랍니다."
    ]
    default_attach = "2026년 하반기 인사발령 대상자 명단 1부."
elif category == "휴직복직":
    default_title_content = "육아휴직 신청 및 후임자 업무 대행 지정 (김주무관)"
    initial_body_paragraphs = [
        "소속 직원의 육아휴직 신청에 따른 업무 공백을 방지하고 원활한 행정 서비스 유지를 위해 후임자 업무 대행자를 아래와 같이 지정합니다.\n\n  가. 휴직자 성명/직급: 주무관 김○○ (행정사무관)\n  나. 휴직 기간: 2026. 8. 1. ~ 2027. 1. 31. (6개월간)\n  다. 업무 대행자: 주무관 이○○ (지정 완료)",
        "대행자는 휴직 기간 동안 해당 사무를 성실히 수행하여 업무 누수가 발생하지 않도록 조치바랍니다."
    ]
    default_attach = "육아휴직 신청서 및 증빙서류 각 1부."
elif category == "예산":
    default_title_content = "2026년도 제1회 추가경정예산 편성 요구서 제출"
    initial_body_paragraphs = [
        "주요 현안 사업 추진 및 시급한 재정 소요에 대응하기 위하여 2026년도 제1회 추가경정예산 편성 요구서를 다음과 같이 제출합니다.\n\n  가. 요구 금액: 금 ○○○백만원 (₩000,000,000)\n  나. 주요 사업명: 공공 AI 문서 관리 시스템 고도화 사업 외 1건\n  다. 산출 내역: [붙임 산출내역서 참고]",
        "원활한 예산 심의 및 확보가 이루어질 수 있도록 관련 부서의 협조를 당부드립니다."
    ]
    default_attach = "2026년도 제1회 추가경정예산 산출내역서 1부."
else:
    default_title_content = "2026년도 핵심 업무 및 미결 현안 인수인계서 (김주무관)"
    initial_body_paragraphs = [
        "담당자 보직 변경에 따른 업무 연속성 확보와 행정 지식 자산의 안정적 승계를 위해 2026년도 소관 주요 업무 및 미결 현안에 대한 인수인계 결과를 보고합니다.\n\n  가. 인계자: 주무관 김○○ / 인수자: 주무관 박○○\n  나. 주요 인계 내용: 핵심 사업 추진 현황, 예산 집행 내역, 미결 공문 목록",
        "세부 인수인계 내용 및 관련 파일은 별첨 시스템을 참고하시기 바랍니다."
    ]
    default_attach = "업무 인수인계서 및 서명부 1부."

# 5. 상단 프로그램 창 배너
st.markdown(f"""
<div class="program-window">
    <p class="program-title">⚡ HRDK-AI 문서기안기</p>
    <p class="program-subtitle">공공기관 표준 메타데이터 및 AI 지능형 기안 검토 시스템</p>
</div>
""", unsafe_allow_html=True)

# [1파트] 제목 편집 영역
st.markdown("#### 📝 1. 표준 제목 설정")
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    edited_content = st.text_input("핵심 내용 및 목적 편집", value=default_title_content, key=f"title_{category}")
with col_t2:
    use_dept = st.checkbox("부서명 포함", value=True, key=f"dept_chk_{category}")

clean_department = department.strip()
if use_dept and clean_department:
    final_title = f"[{category}] {edited_content} ({clean_department})"
else:
    final_title = f"[{category}] {edited_content}"

st.code(final_title, language="text")

st.markdown("---")

# [2파트] 본문 내용 작성 영역 (다중 본문 항 동적 추가 지원)
st.markdown("#### 💡 2. 본문 내용 작성 (다중 항 동적 관리)")
st.caption("필요에 따라 본문 항을 추가하여 3개, 4개 이상의 다중 편제로 확장할 수 있습니다.")

if f'body_paragraphs_{category}' not in st.session_state:
    st.session_state[f'body_paragraphs_{category}'] = initial_body_paragraphs

if st.button("➕ 본문 항 추가", key=f"add_para_{category}"):
    st.session_state[f'body_paragraphs_{category}'].append("")
    st.rerun()

updated_paragraphs = []
for p_idx, p_text in enumerate(st.session_state[f'body_paragraphs_{category}']):
    p_val = st.text_area(
        f"본문 항 [{p_idx + 1}] 내용",
        value=p_text,
        height=120,
        key=f"para_{category}_{p_idx}"
    )
    if p_val.strip():
        updated_paragraphs.append(p_val.strip())

st.markdown("---")

# [3파트] 관련 문서 및 붙임 문서 설정
st.markdown("#### 🔗 3. 관련 문서 및 붙임 문서 설정")

col_sec1, col_sec2 = st.columns(2)

# --- 관련 문서 설정 ---
with col_sec1:
    col_chk1, col_lbl1 = st.columns([1, 4])
    with col_chk1:
        use_related = st.checkbox("포함", value=False, key=f"use_rel_{category}")
    with col_lbl1:
        st.markdown("##### 📌 관련 문서 (단일/복수 자동 분기)")
        
    updated_related = []
    if use_related:
        if f'related_list_{category}' not in st.session_state:
            st.session_state[f'related_list_{category}'] = ["정부조직법 및 당 기관 사무위임 규정"]
        
        if st.button("➕ 관련 문서 추가", key=f"add_rel_btn_{category}"):
            st.session_state[f'related_list_{category}'].append("")
            st.rerun()
            
        hangul_chars = ["가", "나", "다", "라", "마", "바", "사"]
        for idx, item in enumerate(st.session_state[f'related_list_{category}']):
            if idx < len(hangul_chars):
                char_label = hangul_chars[idx]
            else:
                char_label = f"({idx+1})"
                
            val = st.text_input(f"관련 문서 [{char_label}]", value=item, key=f"rel_{category}_{idx}")
            if val.strip():
                updated_related.append((char_label, val))
    else:
        st.caption("체크 시 상단에 '관련:' 항목이 생성됩니다.")

# --- 붙임 문서 설정 ---
with col_sec2:
    col_chk2, col_lbl2 = st.columns([1, 4])
    with col_chk2:
        use_attach = st.checkbox("포함", value=True, key=f"use_att_{category}")
    with col_lbl2:
        st.markdown("##### 📎 붙임 문서 (공문서 규정 서식)")
        
    updated_attach = []
    if use_attach:
        if f'attach_list_{category}' not in st.session_state:
            st.session_state[f'attach_list_{category}'] = [default_attach]
            
        if st.button("➕ 붙임 문서 추가", key=f"add_att_btn_{category}"):
            st.session_state[f'attach_list_{category}'].append("")
            st.rerun()
            
        for idx, item in enumerate(st.session_state[f'attach_list_{category}']):
            val = st.text_input(f"붙임 내용 {idx + 1}", value=item, key=f"att_{category}_{idx}")
            if val.strip():
                updated_attach.append(val.strip())
    else:
        st.caption("체크 해제 시 붙임 항목이 생략됩니다.")

st.markdown("---")

# 6. 최종 미리보기 및 등록 버튼 (지능형 연쇄 채번 및 공공 표준 조립 로직)
if st.button("🚀 최종 기안서 AI 검증 및 미리보기", type="primary", use_container_width=True):
    st.session_state['preview_ready'] = True
    st.session_state['is_approved'] = False
    
    full_doc = ""
    
    has_rel = use_related and updated_related
    
    # [채번 1] 관련 문서 개수에 따른 동적 조립 (1개면 기호 생략, 2개 이상이면 가, 나, 다 부여)
    current_num = 1
    if has_rel:
        if len(updated_related) == 1:
            full_doc += f"{current_num}. 관련: {updated_related[0][1]}\n\n"
        else:
            full_doc += f"{current_num}. 관련:\n"
            for char_lbl, text_val in updated_related:
                full_doc += f"  {char_lbl}. {text_val}\n"
            full_doc += "\n"
        current_num += 1

    # [채번 2] 동적으로 추가된 본문 항들을 순차적 번호(1, 2, 3, 4...)로 연쇄 조립
    for p_content in updated_paragraphs:
        full_doc += f"{current_num}. {p_content}\n\n"
        current_num += 1
    
    # [채번 3] 붙임 문서 조립 및 끝. 마감 처리
    has_att = use_attach and updated_attach
    
    if has_att:
        if len(updated_attach) == 1:
            full_doc += f"붙임  {updated_attach[0]}  끝."
        else:
            full_doc += f"붙임  1. {updated_attach[0]}\n"
            for idx in range(1, len(updated_attach)):
                indent_space = "      "  # '붙임  ' 글자 폭에 맞춘 정렬 공백
                if idx == len(updated_attach) - 1:
                    full_doc += f"{indent_space}{idx + 1}. {updated_attach[idx]}  끝."
                else:
                    full_doc += f"{indent_space}{idx + 1}. {updated_attach[idx]}\n"
    else:
        # 붙임 문서가 없으면 본문 마지막 줄에 두 칸 띄우고 끝. 마감
        full_doc = full_doc.rstrip() + "  끝."
    
    st.session_state['final_doc_title'] = final_title
    st.session_state['final_doc_body'] = full_doc

# 미리보기 결과 출력
if st.session_state.get('preview_ready', False):
    st.markdown("---")
    st.markdown("#### ✨ 전자문서시스템 AI 검증 완료본 프리뷰")
    st.info("공공 서식 정합성 및 다중 편제 번호 체계 검증이 완료되었습니다. 내용을 검토하신 후 최종 결재 상신을 진행해 주세요.")
    
    doc_title = st.session_state.get('final_doc_title', '')
    doc_body = st.session_state.get('final_doc_body', '')
    
    st.markdown(f"**[공식 메타데이터 제목]**\n> `{doc_title}`")
    st.markdown("**[최종 본문 및 편제 구조]**")
    st.code(doc_body, language="text")
    
    st.markdown("")
    if st.button("🌐 전자결재 상신 및 표준 문서함 자동 등록", type="primary", use_container_width=True, key="approve_btn"):
        st.
