import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Creator Strategy Assistant", page_icon="💡", layout="wide")

st.title("💡 Creator Strategy Assistant")
st.write(
    "Build an IG bio and a focused 4-month MVP content plan for Korea-study/work creators. "
    "Use **Quick Planner** for a structured output, or **Chat** for free-form conversations."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)
mode = st.radio("Mode", ["Quick Planner", "Chat"], horizontal=True)

if mode == "Quick Planner":
    st.subheader("IG Bio + MVP Planner")
    st.caption("Fill only what you know. Leave unknown fields blank.")

    with st.form("planner_form"):
        col1, col2 = st.columns(2)
        with col1:
            creator_identity = st.text_input(
                "Creator identity",
                placeholder="e.g. 台灣人視角｜在韓8年｜延世大碩士畢｜韓國在職中",
            )
            core_topics = st.text_area(
                "Core topics",
                placeholder="e.g. 韓國簽證、語學堂、研究所、求職、韓文學習、職場文化差異",
                height=120,
            )
            target_audience = st.text_input(
                "Target audience",
                placeholder="e.g. 想來韓國留學/求職的華語圈用戶",
            )

        with col2:
            revenue_goal = st.text_input(
                "Revenue goal",
                value="4個月內達成 2,000萬韓幣",
            )
            content_style = st.text_input(
                "Content style",
                value="觀點是主角，臉只是載體；可用 AI 圖 + 文字 + 音樂",
            )
            preferred_language = st.selectbox(
                "Output language",
                ["繁體中文", "한국어", "English"],
                index=0,
            )

        constraints = st.text_area(
            "Constraints / things to avoid",
            placeholder="e.g. 先不做 YouTube 長片；只做短影片；避免過度雞湯",
            height=90,
        )

        submitted = st.form_submit_button("Generate Bio + MVP")

    if submitted:
        system_prompt = (
            "You are a top-tier creator strategy consultant. "
            "Return practical, no-fluff plans that can be executed immediately."
        )

        user_prompt = f"""
請依照以下資訊，產出一份可直接執行的策略稿：

[輸入資料]
- Creator identity: {creator_identity}
- Core topics: {core_topics}
- Target audience: {target_audience}
- Revenue goal: {revenue_goal}
- Content style: {content_style}
- Preferred language: {preferred_language}
- Constraints: {constraints}

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

請務必：
- 避免空泛鼓勵
- 用可執行、可驗證的語言
- 若資訊不足，做合理假設並標註
"""

        with st.spinner("Generating your strategy..."):
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )
            result = st.write_stream(stream)

        st.download_button(
            "Download result (.md)",
            data=result,
            file_name="ig_bio_mvp_plan.md",
            mime="text/markdown",
        )

else:
    st.subheader("Free-form Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about IG bio, short-video strategy, or planning..."):
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
