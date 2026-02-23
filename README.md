# 💡 Creator Strategy Assistant

A Streamlit app powered by OpenAI for creator strategy workflows.

## Features

- **Quick Planner**: generate IG Bio + 4-week MVP content strategy.
- **Output modes**:
  - **Standard**: fuller structured strategy output.
  - **Low-token**: compact, high-signal output.
  - **SKIPE**: deterministic block-style output (intent → IA → deliverable).
- **Self-check panel**: quick output QA for repetition, format fidelity, and signal density.
- **Chat**: free-form creator strategy conversations.

## Run locally

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run app

```bash
streamlit run streamlit_app.py
```

3. Open the local URL shown in terminal and paste your OpenAI API key.
