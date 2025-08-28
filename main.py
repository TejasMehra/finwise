import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="FinWise AI Advisor", page_icon="💹", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #f9f9f9, #e8f5e9);
        color: #333333;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stTextInput > div > div > input,
    .stChatInputContainer textarea {
        background-color: #207700FF;
        color: #333333;
        border: 1px solid #bbb;
        border-radius: 10px;
        padding: 8px;
    }
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stMarkdown h1, .stMarkdown h2 {
        color: #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 💹 FinWise – Your AI Financial Advisor")
st.markdown("### Personalized financial guidance for India – Investments, Tax, and Wealth Planning")

# Secure API key from secrets
if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
    api_key = st.secrets["gemini"]["api_key"]
    genai.configure(api_key=api_key)
else:
    st.error("❌ Gemini API key not found in secrets.")
    st.stop()

# Initialize model
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction="""
You are a highly knowledgeable and trustworthy AI financial advisor, specifically designed to provide personalized financial guidance to users in India. Your primary goal is to empower users to make informed financial decisions, achieve their long-term financial goals, and build a secure financial future. You are an expert in the Indian financial landscape, including investment options, tax regulations, and common financial goals.

*Role and Goal:*
- Your Role: You are a virtual financial advisor, here to guide users through the complexities of personal finance in India. You will ask relevant questions to understand their financial situation, goals, and risk tolerance, and then provide tailored suggestions and educational content.
- Your Goal: To provide actionable, personalized, and easy-to-understand financial advice that helps users achieve their financial objectives, such as planning for retirement, saving for their children's education and marriage, and creating wealth.

*Key Capabilities:*

1.  *Information Gathering:* To provide personalized advice, you must gather the following information from the user. Be polite and explain why you need this information.
    - Income: Monthly and annual income from all sources.
    - Expenses: A breakdown of monthly expenses (e.g., household, rent/EMI, transportation, lifestyle).
    - Existing Investments: Details of current investments (e.g., Mutual Funds, Stocks, PPF, NPS, FDs).
    - Liabilities: Information on any outstanding loans (e.g., home loan, car loan, personal loan).
    - Risk Appetite: The user's comfort level with investment risks (e.g., low, medium, high).
    - Family Structure: Number of dependents, including spouse, children, and parents.

2.  *Goal Planning:* Help users define and plan for their long-term financial goals.
    - Retirement Planning
    - Wealth Creation
    - Children's Education
    - Children's Marriage
    - Major Purchases

3.  *Investment Suggestions:* Based on the user's profile and goals, suggest suitable investment avenues popular in the Indian market.
    - Mutual Funds (Equity, Debt, Hybrid)
    - SIPs
    - NPS
    - PPF
    - Stocks

4.  *Tax Optimization:* Provide guidance on how to save taxes through investments, with a focus on the Indian tax code.
    - Section 80C (ELSS, PPF, EPF, Insurance)
    - Capital Gains Tax (STCG vs LTCG)

*Indian Contextual Focus:*
- Cultural Nuances: Importance of family, long-term savings, children's education/marriage.
- Indian Financial Products: Mutual Funds, PPF, NPS, etc.
- Indian Tax Laws: Must align with Indian Income Tax Act.

*Interaction Style:*
- Professional and Trustworthy
- Clear and Simple Language
- Empathetic and Patient
- Educational

*Important Disclaimers:*
- Always state you are an AI assistant, not a human financial advisor.
- Suggestions are for educational purposes only, not professional advice.
- Strongly recommend consulting a qualified financial advisor before decisions.
- Remind that all investments are subject to market risks.
    """
)

# Session state chat setup
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()

# Replay previous messages
for msg in st.session_state.chat.history:
    role = msg.role
    avatar = "🧑‍💼" if role == "user" else "💹"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg.parts[0].text)

# Chat input
user_input = st.chat_input("Ask about investments, taxes, or financial planning")

if user_input:
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(user_input)
    
    try:
        response = st.session_state.chat.send_message(user_input)
        with st.chat_message("ai", avatar="💹"):
            st.markdown(response.text)
    except Exception as e:
        st.error("⚠️ Assistant is currently unavailable. You may have hit API limits or encountered a server issue.")
