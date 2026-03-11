import streamlit as st
from openai import OpenAI


def build_prompt_mode(mode_name: str) -> tuple[str, str, int]:
    if mode_name == "Low-token":
        return (
            "You are a concise creator strategy consultant.",
            "Use compact bullet points, zero fluff, no repetition, and deterministic formatting.",
            700,
        )
    if mode_name == "SKIPE":
        return (
            "You are a UX-grade structured output engine and creator strategy consultant.",
            (
                "Classify user intent first, then produce a shippable deliverable using: "
                "Intent Lock -> Information Architecture -> Structured Blocks -> Self-check. "
                "Rules: no repetition, no generic fluff, strict format fidelity, high signal density."
            ),
            1200,
        )
    return (
        "You are a top-tier creator strategy consultant.",
        "Return practical, no-fluff plans that can be executed immediately.",
        1400,
    )


def build_required_markers(preferred_language: str) -> list[str]:
    if preferred_language == "English":
        return ["IG Bio", "MVP", "short", "Bio Link", "risk", "conclusion"]
    if preferred_language == "한국어":
        return ["IG", "MVP", "숏폼", "Bio Link", "리스크", "결론"]
    return ["IG Bio", "MVP", "短片", "Bio Link", "風險", "結論"]


def run_self_check(result_text: str, preferred_language: str) -> dict[str, str]:
    lines = [line.strip() for line in result_text.splitlines() if line.strip()]
    unique_lines = set(lines)

    no_repetition = "pass" if len(lines) == len(unique_lines) else "warn"

    normalized_text = result_text.lower()
    required_markers = build_required_markers(preferred_language)
    format_fidelity = "pass" if all(marker.lower() in normalized_text for marker in required_markers) else "warn"

    avg_line_len = sum(len(line) for line in lines) / len(lines) if lines else 0
    signal_density = "pass" if 10 <= avg_line_len <= 120 else "warn"

    excessive_blank_lines = result_text.count("\n\n\n")
    low_noise = "pass" if excessive_blank_lines == 0 else "warn"

    return {
        "No Repetition": no_repetition,
        "Format Fidelity": format_fidelity,
        "Signal Density": signal_density,
        "Reduced Noise": low_noise,
    }


def build_user_prompt(
    creator_identity: str,
    core_topics: str,
    target_audience: str,
    revenue_goal: str,
    content_style: str,
    preferred_language: str,
    constraints: str,
    output_mode: str,
    system_rules: str,
    reference_urls: str,
    reference_notes: str,
) -> str:
    base_prompt = f"""
請依照以下資訊，產出一份可直接執行的策略稿：

[輸入資料]
- Creator identity: {creator_identity}
- Core topics: {core_topics}
- Target audience: {target_audience}
- Revenue goal: {revenue_goal}
- Content style: {content_style}
- Preferred language: {preferred_language}
- Constraints: {constraints}

[外部參考 URL（需先閱讀）]
{reference_urls or "(無)"}

[URL 重點摘錄（由使用者提供）]
{reference_notes or "(無)"}

[輸出格式要求]
1) 最終 IG Bio（3 個版本：平衡版 / 強勢版 / 極簡版）
2) 思維轉向（Before → After，最多 6 點）
3) MVP 計畫（4 週）
   - 每週目標
   - 每週內容主題與短片數量
   - 每週唯一 CTA
4) 10 支短片題目（依「最先測爆款」排序）
5) Bio Link 文案（最小可行：標題、主 CTA、私訊關鍵字）
6) 風險與修正（常見 5 個跑偏點 + 修正方法）
7) 一句話結論（讓創作者不再搖擺）

模式要求：{output_mode}
{system_rules}

請務必：
- 避免空泛鼓勵
- 用可執行、可驗證的語言
- 若資訊不足，做合理假設並標註
- 若有提供 URL 但無摘錄內容，先用「待確認事項」列出，不可把 URL 內容當已讀事實
"""

    if output_mode == "SKIPE":
        base_prompt += """

[SKIPE Output Blocks]
A) Intent Lock (1-2 lines)
B) Information Architecture (compact bullets)
C) Shippable Deliverable Blocks (ready-to-paste)
D) Self-check Summary (pass/warn with one-line reason)
E) URL Confirmation Block（已確認 / 待確認）
"""

    return base_prompt


st.set_page_config(page_title="創作者策略助手", page_icon="💡", layout="wide")

st.title("💡 創作者策略助手")
st.write(
    "快速產出 IG Bio 與 4 週 MVP 內容規劃。"
    "可使用 **快速規劃**（結構化輸出）、**SKIPE**（固定區塊）或 **對話模式**（自由提問）。"
)

openai_api_key = st.text_input("OpenAI API 金鑰", type="password")

if not openai_api_key:
    st.info("請先輸入 OpenAI API 金鑰。", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)
mode = st.radio("模式", ["Quick Planner", "Chat"], horizontal=True)

if "last_result" not in st.session_state:
    st.session_state.last_result = ""
if "last_language" not in st.session_state:
    st.session_state.last_language = "繁體中文"

if mode == "Quick Planner":
    st.subheader("IG Bio + MVP 規劃")
    st.caption("只填你目前確定的資訊即可，未知欄位可留空。")

    output_mode = st.selectbox(
        "輸出模式",
        ["Standard", "Low-token", "SKIPE"],
        help="Standard：完整細節；Low-token：精簡高密度；SKIPE：固定結構區塊。",
    )

    with st.form("planner_form"):
        col1, col2 = st.columns(2)
        with col1:
            creator_identity = st.text_input(
                "創作者定位",
                placeholder="e.g. 台灣人視角｜在韓8年｜延世大碩士畢｜韓國在職中",
            )
            core_topics = st.text_area(
                "核心主題",
                placeholder="e.g. 韓國簽證、語學堂、研究所、求職、韓文學習、職場文化差異",
                height=120,
            )
            target_audience = st.text_input(
                "目標受眾",
                placeholder="e.g. 想來韓國留學/求職的華語圈用戶",
            )

        with col2:
            revenue_goal = st.text_input(
                "營收目標",
                value="4個月內達成 2,000萬韓幣",
            )
            content_style = st.text_input(
                "內容風格",
                value="觀點是主角，臉只是載體；可用 AI 圖 + 文字 + 音樂",
            )
            preferred_language = st.selectbox(
                "輸出語言",
                ["繁體中文", "한국어", "English"],
                index=0,
            )

        constraints = st.text_area(
            "限制 / 避免事項",
            placeholder="e.g. 先不做 YouTube 長片；只做短影片；避免過度雞湯",
            height=90,
        )

        reference_urls = st.text_area(
            "參考 URL（每行一個）",
            placeholder="https://example.com/page1\nhttps://example.com/page2",
            height=90,
        )
        reference_notes = st.text_area(
            "URL 重點摘錄（可貼下一個分頁讀到的重點）",
            placeholder="請貼上你已確認的重點，模型才會當成已讀事實。",
            height=90,
        )

        submitted = st.form_submit_button("產生 Bio + MVP")

    if submitted:
        if not core_topics.strip():
            st.warning("請至少填寫「核心主題」，輸出才會更精準。")
        else:
            if reference_urls.strip() and not reference_notes.strip():
                st.info("你有提供 URL 但未提供摘錄；輸出將改以「待確認事項」標註，避免臆測內容。")
            system_role, system_rules, max_tokens = build_prompt_mode(output_mode)
            user_prompt = build_user_prompt(
                creator_identity=creator_identity,
                core_topics=core_topics,
                target_audience=target_audience,
                revenue_goal=revenue_goal,
                content_style=content_style,
                preferred_language=preferred_language,
                constraints=constraints,
                output_mode=output_mode,
                system_rules=system_rules,
                reference_urls=reference_urls,
                reference_notes=reference_notes,
            )

            try:
                with st.spinner("Generating your strategy..."):
                    stream = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_role},
                            {"role": "user", "content": user_prompt},
                        ],
                        max_tokens=max_tokens,
                        stream=True,
                    )
                    result = st.write_stream(stream)
                    st.session_state.last_result = result
                    st.session_state.last_language = preferred_language
            except Exception as error:
                st.error(f"產生失敗：{error}")

    if st.session_state.last_result:
        st.download_button(
            "下載結果（.md）",
            data=st.session_state.last_result,
            file_name="ig_bio_mvp_plan.md",
            mime="text/markdown",
        )

        st.markdown("### 自我檢查")
        check_results = run_self_check(st.session_state.last_result, st.session_state.last_language)
        for rule_name, status in check_results.items():
            icon = "✅" if status == "pass" else "⚠️"
            st.write(f"{icon} {rule_name}: {status}")

else:
    st.subheader("自由對話")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("可詢問 IG Bio、短影音策略或內容規劃…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a practical creator growth strategist."},
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
