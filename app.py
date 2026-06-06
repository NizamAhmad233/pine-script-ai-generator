import streamlit as st
from google import genai

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Pine Script AI Generator",
    layout="wide"
)

# Load API key from Streamlit secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🚀 Pine Script v6 AI Generator (Gemini)")

st.markdown("Describe your indicator or strategy below:")

# =========================
# USER INPUT
# =========================

prompt = st.text_area(
    "Your Prompt",
    height=250,
    placeholder="""
Example:
Create a Pine Script v6 indicator:
- RSI 14
- Buy when RSI crosses above 30
- Sell when RSI crosses below 70
- Plot arrows and alerts
"""
)

# =========================
# GENERATION FUNCTION
# =========================

def generate_pine(prompt_text):

    system_prompt = """
You are an expert Pine Script version 6 developer.

STRICT RULES:
- Output ONLY Pine Script code
- No explanations
- No markdown
- No backticks
- Must compile in TradingView
- Always start with //@version=6
- Add comments where needed
- Include alertcondition() when signals exist
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=system_prompt + "\n\nUSER REQUEST:\n" + prompt_text
    )

    return response.text

# =========================
# GENERATE BUTTON
# =========================

if st.button("🚀 Generate Pine Script"):

    if not prompt.strip():
        st.warning("Please enter a prompt first.")
        st.stop()

    with st.spinner("Generating Pine Script..."):

        try:
            code = generate_pine(prompt)

            st.subheader("📜 Generated Pine Script")

            st.code(code, language="javascript")

            st.download_button(
                label="📥 Download Pine Script",
                data=code,
                file_name="indicator.pine",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")