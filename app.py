import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="공공 AI 문서함 다중 기안(복수안) 표준화 솔루션",
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
st.markdown('<p class="main-header">🏛️ 공공기관 문서함 5대 업무 복수안(1·2·3안) AI 표준 기안 솔루션</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">내부 결재 및 대외 발송 등 목적에 따라 복수의 안을 추가하고, 대상별 표준 제목을 개별 설정하여 안전하게 등록합니다.</p>', unsafe_allow_html=True)

# 4. 사이드바 - 기관 설정 및 카테고리 선택
with st.sidebar:
    st.header("⚙️ 기관 및 메타데이터 설정")
    org_name = st.text_input("소속 기관명", value="○○부/○○청")
    department = st.text_input("작성 부서명 (비워두면 괄호 생략)", value="기획예산담당관")
    
    st.markdown("---")
    category = st.selectbox(
        "핵심 업무 카테고리 선택",
        ["업무분장", "인사발령", "휴직복직", "예산", "인수인계"]
    )
    
    st.markdown("---")
    st.markdown("### 🎯 복수안 기안 가이드")
    st.write("• **1안**: 내부 결재 및 보고용\n• **2안**: 유관부서 또는 전체기관 발송용\n• **3안 이상**: 수기 작성 및 추가 대외 기관용")

# 5. 카테고리별 기본 템플릿 정의
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

# 6. 메인 다중 기안 영역 (세션 스테이트를 이용한 동적 안 추가 관리)
if 'draft_list' not in st.session_state or st.session_state.get('current_category') != category:
    st.session_state['current_category'] = category
    # 초기 세팅: 기본 2개 안 제공 (1안: 내부 결재, 2안: 대외 발송)
    st.session_state['draft_list'] = [
        {"id": 1, "target": "내부 결재용 (내부문서)", "content": default_content + " (내부 보고안)"},
        {"id": 2, "target": "전체 부서 / 유관기관 (대외발송)", "content": default_content + " (대외 협조안)"}
    ]

st.subheader(f"📝 [{category}] 복수안(1안, 2안...) 기안 및 표준 제목 편집기")
st.markdown("기안서 내에 포함될 안(Draft)을 추가하고, 발송 대상에 맞추어 제목을 각각 다르게 편집할 수 있습니다.")

# 안 추가 버튼
if st.button("➕ 새로운 안(Draft) 추가하기"):
    new_id = len(st.session_state['draft_list']) + 1
    st.session_state['draft_list'].append(
        {"id": new_id, "target": "수기 작성 / 기타 기관", "content": default_content + f" (제{new_id}안)"}
    )
    st.rerun()

# 각 안별 입력 폼 렌더링
updated_drafts = []
clean_department = department.strip()

for i, draft in enumerate(st.session_state['draft_list']):
    st.markdown(f"---")
    cols = st.columns([1, 3])
    with cols[0]:
        st.markdown(f"#### **제{draft['id']}안**")
        target_option = st.selectbox(
            f"제{draft['id']}안 대상 선택",
            ["내부 결재용 (내부문서)", "전체 부서 대상", "기타 부서 대상", "수기 작성 / 기타 기관", "직접 입력"],
            index=0 if draft['id'] == 1 else (1 if draft['id'] == 2 else 3),
            key=f"target_{draft['id']}_{category}"
        )
    with cols[1]:
        edited_content = st.text_input(
            f"제{draft['id']}안 핵심 내용 및 목적 편집",
            value=draft['content'],
            key=f"content_{draft['id']}_{category}"
        )
    
    # 대상이 '직접 입력'일 경우 추가 텍스트 입력창 제공
    final_target = target_option
    if target_option == "직접 입력":
        custom_target = st.text_input(f"제{draft['id']}안 발송 대상 직접 입력", value="지자체 및 유관기관", key=f"custom_{draft['id']}_{category}")
        final_target = custom_target

    # 최종 제목 조합 로직 ([카테고리] 핵심내용 [대상표기] (부서명))
    target_tag = f"[{final_target.split(' ')[0]}]" if "수기" not in final_target and "직접" not in final_target else f"[{final_target}]"
    
    if clean_department:
        combined_title = f"[{category}] {edited_content} - {target_tag} ({clean_department})"
    else:
        combined_title = f"[{category}] {edited_content} - {target_tag}"
        
    updated_drafts.append({"id": draft['id'], "target": final_target, "title": combined_title})

st.markdown("---")

# 7. 2단계 검증 및 최종 실행 영역
if st.button("🔍 전체 안(Draft) 적용 및 결과 미리보기", type="primary", use_container_width=True):
    st.session_state['preview_ready'] = True
    st.session_state['final_drafts'] = updated_drafts
    st.session_state['is_approved'] = False

if st.session_state.get('preview_ready', False):
    st.markdown("#### 🔎 복수안 표준화 결과 미리보기 (Human-in-the-Loop 검증)")
    st.info("각 안별로 조합된 최종 메타데이터 형식을 확인하신 후 문제가 없다면 **[최종 문서함 등록 (실행)]** 버튼을 눌러주세요.")
    
    for d in st.session_state['final_drafts']:
        st.markdown(f"**[제{d['id']}안 - 대상: {d['target']}]**")
        st.code(d['title'], language="text")
    
    if st.button("🚀 최종 문서함 등록 (실행)", type="primary", use_container_width=True):
        st.session_state['is_approved'] = True

if st.session_state.get('is_approved', False):
    st.success(f"🎉 [{org_name}] 표준 문서함에 복수안(총 {len(st.session_state['final_drafts'])}개 안)이 성공적으로 등록되었습니다!")
    for d in st.session_state.get('final_drafts', []):
        st.markdown(f"- 제{d['id']}안 등록 완료: `{d['title']}`")

# 8. 하단 푸터
st.markdown("---")
st.markdown(f"2026 공공 AI 대전환 챌린지 출품작 시제품 (PoC) | 소속 기관: {org_name} | Powered by Streamlit", unsafe_allow_html=True)
