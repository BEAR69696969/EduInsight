from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import random
from sklearn.linear_model import LinearRegression

# 題目資料庫
QUESTIONS = {
    "Reading": [
        {
            "question": "Read the following passage and answer the question.\n\n'The company announced that it would expand its operations to three new countries next year. The CEO stated that this expansion would create over 500 new jobs.'\n\nWhat did the CEO say about the expansion?",
            "options": ["A. It would reduce the number of employees", "B. It would create more than 500 jobs", "C. It would close some existing offices", "D. It would happen in five years"],
            "answer": "B",
            "explanation": "文章中提到 CEO 說擴張將創造超過 500 個新工作機會（create over 500 new jobs）。"
        },
        {
            "question": "Read the notice below.\n\n'The office will be closed on Monday, December 25th for the holiday. Regular business hours will resume on Tuesday, December 26th.'\n\nWhen will the office reopen?",
            "options": ["A. December 24th", "B. December 25th", "C. December 26th", "D. December 27th"],
            "answer": "C",
            "explanation": "通知中說 12 月 26 日（Tuesday, December 26th）恢復正常營業時間。"
        },
        {
            "question": "Read the email subject line.\n\n'Reminder: Annual Performance Review Scheduled for Next Friday'\n\nWhat is the email about?",
            "options": ["A. A job application", "B. A company picnic", "C. A yearly employee review", "D. A product launch"],
            "answer": "C",
            "explanation": "Annual Performance Review 指的是年度績效評估，即每年一次的員工考核。"
        },
        {
            "question": "Read the advertisement.\n\n'Wanted: Experienced software engineer with at least 3 years of experience. Must be proficient in Python and Java. Competitive salary offered.'\n\nWhat is required for this position?",
            "options": ["A. Experience in marketing", "B. Knowledge of Python and Java", "C. A degree in business", "D. Sales experience"],
            "answer": "B",
            "explanation": "廣告中要求應徵者必須精通 Python 和 Java（Must be proficient in Python and Java）。"
        },
        {
            "question": "Read the memo.\n\n'All employees are required to complete the online safety training by March 31st. Failure to do so may result in restricted access to company systems.'\n\nWhat will happen if employees do not complete the training?",
            "options": ["A. They will receive a bonus", "B. They will be promoted", "C. Their system access may be limited", "D. They will get extra vacation days"],
            "answer": "C",
            "explanation": "備忘錄中提到未完成訓練可能導致對公司系統的存取受限（restricted access to company systems）。"
        },
        {
            "question": "Read the following passage.\n\n'Our store will be undergoing renovations from June 1st to June 15th. During this time, we will remain open but some sections may be temporarily unavailable.'\n\nWhat is true about the store during renovations?",
            "options": ["A. It will be completely closed", "B. It will move to a new location", "C. It will still be open to customers", "D. It will offer special discounts"],
            "answer": "C",
            "explanation": "文章說明店舖在裝修期間仍會營業（we will remain open）。"
        },
        {
            "question": "Read the letter.\n\n'Thank you for your order. Your package has been shipped and is expected to arrive within 3-5 business days. You can track your order using the tracking number provided.'\n\nHow can the customer monitor their delivery?",
            "options": ["A. By calling the store", "B. By visiting the warehouse", "C. By using a tracking number", "D. By sending an email"],
            "answer": "C",
            "explanation": "信件中提到可以使用提供的追蹤號碼追蹤訂單（track your order using the tracking number provided）。"
        },
        {
            "question": "Read the announcement.\n\n'The quarterly meeting has been rescheduled from Thursday to Wednesday due to a scheduling conflict. The time and location remain the same.'\n\nWhat changed about the meeting?",
            "options": ["A. The location", "B. The time", "C. The day", "D. The agenda"],
            "answer": "C",
            "explanation": "公告中說會議從週四改到週三（rescheduled from Thursday to Wednesday），只有日期改變。"
        }
    ],
    "Vocabulary": [
        {
            "question": "Choose the word that best completes the sentence.\n\nThe manager asked the team to ______ the project deadline by two weeks.",
            "options": ["A. extend", "B. reduce", "C. ignore", "D. replace"],
            "answer": "A",
            "explanation": "extend 表示延長，符合句意「將截止日期延長兩週」。"
        },
        {
            "question": "Choose the word closest in meaning to 'collaborate'.",
            "options": ["A. compete", "B. cooperate", "C. complain", "D. calculate"],
            "answer": "B",
            "explanation": "collaborate 意思是合作，與 cooperate（合作）意思最接近。"
        },
        {
            "question": "Choose the word that best completes the sentence.\n\nPlease ______ your attendance at the meeting by Friday.",
            "options": ["A. confirm", "B. cancel", "C. confuse", "D. collect"],
            "answer": "A",
            "explanation": "confirm your attendance 是「確認出席」的固定用法，符合句意。"
        },
        {
            "question": "Choose the word that best completes the sentence.\n\nThe new policy will ______ starting from next month.",
            "options": ["A. take effect", "B. take place", "C. take over", "D. take back"],
            "answer": "A",
            "explanation": "take effect 表示「生效」，是描述政策或規定開始實施的固定用法。"
        },
        {
            "question": "Choose the word closest in meaning to 'mandatory'.",
            "options": ["A. optional", "B. suggested", "C. required", "D. helpful"],
            "answer": "C",
            "explanation": "mandatory 意思是強制性的、必須的，與 required（必要的）意思最接近。"
        },
        {
            "question": "Choose the word that best completes the sentence.\n\nThe company decided to ______ its partnership with the supplier.",
            "options": ["A. terminate", "B. celebrate", "C. donate", "D. estimate"],
            "answer": "A",
            "explanation": "terminate 表示終止，符合句意「終止與供應商的合作關係」。"
        },
        {
            "question": "Choose the word closest in meaning to 'compensate'.",
            "options": ["A. punish", "B. reimburse", "C. ignore", "D. delay"],
            "answer": "B",
            "explanation": "compensate 意思是補償，與 reimburse（償還、補償）意思最接近。"
        },
        {
            "question": "Choose the word that best completes the sentence.\n\nThe sales team exceeded their ______ for the third quarter.",
            "options": ["A. quota", "B. quality", "C. quantity", "D. question"],
            "answer": "A",
            "explanation": "quota 表示配額或業績目標，exceeded their quota 意思是「超過了他們的目標」。"
        }
    ],
    "Grammar": [
        {
            "question": "Choose the correct form to complete the sentence.\n\nThe report ______ by the team before the deadline.",
            "options": ["A. submit", "B. submitted", "C. was submitted", "D. submitting"],
            "answer": "C",
            "explanation": "這句是被動語態，主詞 The report 是被提交的，所以要用 was submitted（過去被動式）。"
        },
        {
            "question": "Choose the correct word to complete the sentence.\n\nShe has been working at this company ______ five years.",
            "options": ["A. since", "B. for", "C. during", "D. while"],
            "answer": "B",
            "explanation": "for 用於表示一段時間長度（five years），since 用於表示起點（a specific time）。"
        },
        {
            "question": "Choose the grammatically correct sentence.",
            "options": ["A. He don't know the answer.", "B. She have finished her work.", "C. They are waiting for the bus.", "D. We was happy about the news."],
            "answer": "C",
            "explanation": "They are waiting for the bus. 是正確的現在進行式句型。其他選項都有主詞動詞不一致的錯誤。"
        },
        {
            "question": "Choose the correct form to complete the sentence.\n\nBy the time the manager arrived, the team ______ the presentation.",
            "options": ["A. finish", "B. finished", "C. had finished", "D. will finish"],
            "answer": "C",
            "explanation": "By the time 引導的句子要用過去完成式（had finished），表示在某個過去時間點之前已完成的動作。"
        },
        {
            "question": "Choose the correct word to complete the sentence.\n\nNeither the manager ______ the employees were informed about the change.",
            "options": ["A. or", "B. nor", "C. but", "D. and"],
            "answer": "B",
            "explanation": "Neither...nor... 是固定搭配，表示「兩者都不」。"
        },
        {
            "question": "Choose the correct form to complete the sentence.\n\nIf we ______ more time, we could have completed the project.",
            "options": ["A. have", "B. had", "C. will have", "D. having"],
            "answer": "B",
            "explanation": "這是假設語氣（If + had + 過去分詞），表示與過去事實相反的假設。"
        },
        {
            "question": "Choose the correct word to complete the sentence.\n\nThe new employee, ______ started last Monday, has already impressed the team.",
            "options": ["A. who", "B. which", "C. whom", "D. whose"],
            "answer": "A",
            "explanation": "關係代名詞 who 用於指人，且在子句中作主詞，符合句意。"
        },
        {
            "question": "Choose the grammatically correct sentence.",
            "options": ["A. The meeting will reschedule tomorrow.", "B. The meeting will be rescheduled tomorrow.", "C. The meeting will be reschedule tomorrow.", "D. The meeting will rescheduling tomorrow."],
            "answer": "B",
            "explanation": "被動語態的正確結構是 will be + 過去分詞，所以應該是 will be rescheduled。"
        }
    ]
}

# 深色模式 session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# 深色模式配色
if st.session_state.dark_mode:
    bg_color = "linear-gradient(135deg, #1a1a2e, #16213e)"
    text_color = "#ffffff"
    card_bg = "rgba(255,255,255,0.05)"
    card_shadow = "0 4px 20px rgba(0,0,0,0.3)"
    metric_bg = "rgba(255,255,255,0.08)"
    plot_bgcolor = "rgba(30,30,50,0.8)"
    paper_bgcolor = "rgba(30,30,50,0.8)"
    font_color = "#ffffff"
else:
    bg_color = "linear-gradient(135deg, #f3e8ff, #ede8ff)"
    text_color = "#1a1a2e"
    card_bg = "white"
    card_shadow = "0 4px 20px rgba(0,0,0,0.08)"
    metric_bg = "white"
    plot_bgcolor = "rgba(255,255,255,0.8)"
    paper_bgcolor = "rgba(255,255,255,0.8)"
    font_color = "#1a1a2e"

# 自訂 CSS 樣式
st.markdown(f"""
<style>
    /* 載入 Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Poppins:wght@400;600;700;800&display=swap');

    /* 全域字體 */
    * {{
        font-family: 'Poppins', 'Noto Sans TC', sans-serif !important;
    }}

    /* 標題字體加粗 */
    h1, h2, h3 {{
        font-family: 'Poppins', 'Noto Sans TC', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }}

    /* 內文字體 */
    p, li, span, label {{
        font-family: 'Noto Sans TC', 'Poppins', sans-serif !important;
        font-weight: 400 !important;
        line-height: 1.7 !important;
    }}

    /* 按鈕字體 */
    .stButton > button {{
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }}
    
    /* 整體背景 */
    .stApp,
    [data-testid="stAppViewContainer"] {{
        background: {bg_color} !important;
    }}

    .main .block-container,
    [data-testid="stAppViewBlockContainer"] {{
        background: transparent !important;
    }}

    /* 側邊欄背景 */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1a1a2e, #16213e) !important;
    }}

    /* 側邊欄文字 */
    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
        opacity: 1 !important;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stSidebar"] .stAlert p {{
        color: #ffffff !important;
        opacity: 1 !important;
    }}

    [data-testid="stSidebar"] input {{
        color: #ffffff !important;
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        border-radius: 10px !important;
    }}

    [data-testid="stSidebar"] input::placeholder {{
        color: rgba(255,255,255,0.6) !important;
    }}

    [data-testid="stSidebar"] [data-testid="stInfo"],
    [data-testid="stSidebar"] [data-testid="stAlert"] {{
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}

    /* 主畫面文字 */
    .main * {{
        color: {text_color} !important;
    }}

    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {{
        color: {text_color} !important;
        opacity: 1 !important;
    }}

    .stRadio label,
    .stRadio span {{
        color: {text_color} !important;
        opacity: 1 !important;
    }}

    .stSlider label,
    .stSlider span {{
        color: {text_color} !important;
        opacity: 1 !important;
    }}

    /* 標題 */
    h1 {{
        color: {text_color} !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }}

    h2, h3 {{
        color: {text_color} !important;
        font-weight: 700 !important;
    }}

    /* 按鈕 */
    .stButton > button {{
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }}

    /* Link Button */
    .stLinkButton > a {{
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-decoration: none !important;
        display: block !important;
        text-align: center !important;
        width: 100% !important;
    }}

    .stLinkButton > a:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
        color: white !important;
    }}

    .stLinkButton > a p,
    .stLinkButton > a span {{
        color: white !important;
    }}

    /* Metric 卡片 */
    [data-testid="metric-container"] {{
        background: {metric_bg} !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: {card_shadow} !important;
        border-left: 4px solid #667eea !important;
    }}

    [data-testid="metric-container"] label,
    [data-testid="metric-container"] [data-testid="stMetricValue"],
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {{
        color: {text_color} !important;
    }}

    /* Tab */
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: {text_color} !important;
    }}

    .stTabs [aria-selected="true"] {{
        color: #667eea !important;
        border-bottom: 3px solid #667eea !important;
    }}

    /* 輸入框 */
    .stTextInput > div > div > input {{
        border-radius: 10px !important;
        border: 2px solid #667eea !important;
        color: {text_color} !important;
        background: {metric_bg} !important;
    }}

    /* 分隔線 */
    hr {{
        border-color: #667eea !important;
        opacity: 0.3 !important;
    }}
    
    /* sidebar 收合按鈕樣式 */
    [data-testid="stSidebarCollapseButton"] {{
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
        width: 40px !important;
        height: 40px !important;
    }}

    [data-testid="stSidebarCollapseButton"] svg {{
        fill: white !important;
        color: white !important;
    }}

    section[data-testid="stSidebarCollapsedControl"] button {{
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
        width: 40px !important;
        height: 40px !important;
    }}

    section[data-testid="stSidebarCollapsedControl"] svg {{
        fill: white !important;
        color: white !important;
    }}

    section[data-testid="stSidebarCollapsedControl"] {{
        display: none !important;
    }}

    .st-emotion-cache-ol6tze {{
        display: none !important;
    }}

    /* 隱藏所有 icon 文字 */
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    button[data-testid="baseButton-headerNoPadding"] {{
        display: none !important;
    }}

    /* 手機版 sidebar 按鈕 */
    .st-emotion-cache-1dp5vir {{
        display: none !important;
    }}

    header [data-testid="stToolbar"] button svg + span {{
        display: none !important;
    }}

    /* 只隱藏 icon 旁邊的文字，保留圖示 */
    .material-symbols-rounded {{
        font-size: 1.5rem !important;
        width: 1.5rem !important;
        height: 1.5rem !important;
        overflow: hidden !important;
    }}

    /* 隱藏 header 按鈕文字但保留功能 */
    header button span:not([data-testid]) {{
        display: none !important;
    }}

    /* 隱藏 chat_message icon 文字 */
    [data-testid="chatAvatarIcon-user"],
    [data-testid="chatAvatarIcon-assistant"] {{
        display: none !important;
    }}

    .stChatMessage {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}

    [data-testid="stChatMessageContent"] {{
        background: transparent !important;
    }}

    /* 對話輸入框 placeholder 顏色 */
    .stTextInput > div > div > input::placeholder {{
        color: #999999 !important;
        opacity: 1 !important;
    }}

    /* 隱藏按鈕內的文字但保留圖示 */
    [data-testid="stSidebarCollapseButton"] span,
    section[data-testid="stSidebarCollapsedControl"] span {{
        display: none !important;
    }}

</style>
""", unsafe_allow_html=True)

# 側邊欄
st.sidebar.markdown("""
<div style="
    text-align: center;
    padding: 20px 0;
">
    <div style="
        font-size: 3rem;
        margin-bottom: 10px;
    ">🌍</div>
    <h1 style="
        color: white !important;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    ">EduInsight</h1>
    <p style="
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.85rem;
        margin-top: 5px;
    ">AI 英文學習平台</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.info("""
AI 英文學習分析平台

功能：
- 弱點分析
- TOEIC 預測
- Machine Learning
- AI 讀書計畫
""")

st.sidebar.divider()

st.sidebar.subheader("👤 使用者登入")

username = st.sidebar.text_input("請輸入使用者名稱")

if username:
    st.sidebar.success(f"✅ 歡迎，{username}！")
else:
    st.sidebar.warning("⚠️ 請輸入使用者名稱後再儲存紀錄")
    
st.sidebar.divider()

if st.session_state.dark_mode:
    dark_label = "☀️ 切換淺色模式"
else:
    dark_label = "🌙 切換深色模式"

if st.sidebar.button(dark_label):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

    st.sidebar.divider()

st.sidebar.divider()

# 切換到 AI 對話模式
st.sidebar.subheader("💬 AI 對話助教")

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = False

if st.sidebar.button("💬 開啟 AI 對話"):
    st.session_state.chat_mode = not st.session_state.chat_mode
    st.rerun()

st.sidebar.subheader("📝 練習題")

if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = False

if st.sidebar.button("📝 開始練習題"):
    st.session_state.quiz_mode = not st.session_state.quiz_mode
    st.rerun()

st.sidebar.divider()

# 手機版 sidebar 提示
st.markdown(f"""
<div style="
    background: {card_bg};
    border-radius: 15px;
    padding: 12px 20px;
    margin-bottom: 15px;
    box-shadow: {card_shadow};
    display: flex;
    align-items: center;
    gap: 10px;
">
    <span style="font-size: 1.2rem;">☰</span>
    <p style="
        color: {text_color} !important;
        margin: 0;
        font-size: 0.9rem;
    ">點擊左上角 <b>☰</b> 開啟選單，可登入帳號與切換模式</p>
</div>
""", unsafe_allow_html=True)

# 模式選擇
analysis_ready = False
mode = st.radio(

    "選擇輸入方式",
    ["手動輸入", "CSV 上傳"]
)

# 歡迎頁面
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
">
    <h1 style="
        color: white !important;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 10px;
    ">🌍 EduInsight</h1>
    <p style="
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.2rem;
        margin-bottom: 20px;
    ">AI 英文學習弱點分析平台</p>
    <div style="
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    ">
        <div style="
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 10px 20px;
        ">
            <span style="color: white !important;">📊 弱點分析</span>
        </div>
        <div style="
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 10px 20px;
        ">
            <span style="color: white !important;">🤖 AI 建議</span>
        </div>
        <div style="
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 10px 20px;
        ">
            <span style="color: white !important;">🧠 Machine Learning</span>
        </div>
        <div style="
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 10px 20px;
        ">
            <span style="color: white !important;">📈 成長追蹤</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 手動輸入
if mode == "手動輸入":

    st.markdown(f"""
    <div style="
        background: {card_bg};
        border-radius: 20px;
        padding: 30px;
        box-shadow: {card_shadow};
        margin-bottom: 20px;
    ">
        <h3 style="color: #667eea !important; font-weight: 700; margin-bottom: 5px;">📝 請輸入英文能力</h3>
        <p style="color: {text_color} !important; font-size: 0.9rem;">請根據您的實際程度調整以下滑桿</p>
    </div>
    """, unsafe_allow_html=True)

    reading_score = st.slider("Reading（閱讀）", 0, 100, 50) / 100
    vocabulary_score = st.slider("Vocabulary（詞彙）", 0, 100, 50) / 100
    grammar_score = st.slider("Grammar（語法)", 0, 100, 50) / 100

    accuracy = pd.Series({
        "Reading": reading_score,
        "Vocabulary": vocabulary_score,
        "Grammar": grammar_score
    })

    analysis_ready = True

# CSV 上傳
if mode == "CSV 上傳":

    uploaded_file = st.file_uploader(
        "請上傳學生作答資料 CSV 檔案",
        type=["csv"]
    )

    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file)

        st.subheader("學生作答資料")
        st.write(data)

        accuracy = data.groupby("question_type")["correct"].mean()

        analysis_ready = True

        st.subheader("各題型正確率")
        st.write(accuracy)

        reading_score = accuracy.get("Reading", 0)
        vocabulary_score = accuracy.get("Vocabulary", 0)
        grammar_score = accuracy.get("Grammar", 0)

# 分析區塊
if analysis_ready:

    tab1, tab2, tab3 = st.tabs([
        "📊 分析結果",
        "🤖 AI 建議",
        "🧠 Machine Learning"
    ])

    with tab1:

        st.subheader("英文能力分析圖")

        # 長條圖
        fig_bar = px.bar(
            x=["Reading", "Vocabulary", "Grammar"],
            y=[reading_score * 100, vocabulary_score * 100, grammar_score * 100],
            labels={"x": "能力", "y": "分數（%）"},
            color=["Reading", "Vocabulary", "Grammar"],
            color_discrete_map={
                "Reading": "#667eea",
                "Vocabulary": "#764ba2",
                "Grammar": "#f093fb"
            },
            title="英文能力分析圖"
        )

        fig_bar.update_layout(
            plot_bgcolor=plot_bgcolor,
            paper_bgcolor=paper_bgcolor,
            font=dict(color=font_color, size=14),
            showlegend=False,
            yaxis=dict(
                range=[0, 100],
                tickfont=dict(color=font_color),
                title_font=dict(color=font_color)
            ),
            xaxis=dict(
                tickfont=dict(color=font_color),
                title_font=dict(color=font_color)
            ),
            bargap=0.3
        )

        fig_bar.update_traces(
            texttemplate="%{y:.0f}%",
            textposition="outside"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        # 雷達圖
        st.subheader("英文能力雷達圖")

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=[
                reading_score * 100,
                vocabulary_score * 100,
                grammar_score * 100,
                reading_score * 100
            ],
            theta=["Reading", "Vocabulary", "Grammar", "Reading"],
            fill="toself",
            fillcolor="rgba(102, 126, 234, 0.3)",
            line=dict(color="#667eea", width=2),
            name="能力分析"
        ))

        fig_radar.update_layout(
            polar=dict(
                bgcolor=plot_bgcolor,
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color=font_color),
                    gridcolor="rgba(255,255,255,0.2)" if st.session_state.dark_mode else "rgba(0,0,0,0.1)"
                ),
                angularaxis=dict(
                    tickfont=dict(color=font_color, size=14),
                    gridcolor="rgba(255,255,255,0.2)" if st.session_state.dark_mode else "rgba(0,0,0,0.1)"
                )
            ),
            plot_bgcolor=plot_bgcolor,
            paper_bgcolor=paper_bgcolor,
            font=dict(color=font_color, size=14),
            showlegend=False
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        st.divider()

        # 能力總覽
        st.subheader("英文能力總覽")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Reading", f"{int(reading_score * 100)}%")
        with col2:
            st.metric("Vocabulary", f"{int(vocabulary_score * 100)}%")
        with col3:
            st.metric("Grammar", f"{int(grammar_score * 100)}%")

    with tab2:

        # Groq AI 個人化建議
        st.subheader("🤖 AI 個人化建議")

        if st.button("產生 AI 建議", key="ai_suggest"):

            with st.spinner("AI 分析中，請稍候..."):

                try:
                    from groq import Groq

                    client = Groq(
                        api_key=os.getenv("GROQ_API_KEY")
                    )

                    prompt = f"""
你是一位專業的英文與 TOEIC 學習顧問。
以下是一位學生的英文能力分析結果：

- Reading（閱讀）正確率：{int(reading_score * 100)}%
- Vocabulary（詞彙）正確率：{int(vocabulary_score * 100)}%
- Grammar（語法）正確率：{int(grammar_score * 100)}%

請根據以上資料：
1. 分析學生目前的學習狀況
2. 針對每個能力給出具體的改善建議
3. 推薦適合的學習資源或練習方式
4. 給予鼓勵的話語

請用繁體中文回答，語氣親切、具體，條列式呈現建議。
"""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )

                    ai_response = response.choices[0].message.content
                    st.markdown(ai_response)

                except Exception as e:
                    st.error(f"AI 建議產生失敗：{e}")

    with tab3:

        # TOEIC 預測公式
        st.subheader("AI TOEIC 分數預測")

        predicted_toeic = (
            reading_score * 0.5
            + vocabulary_score * 0.3
            + grammar_score * 0.2
        ) * 990

        st.metric(
            label="AI 預測 TOEIC 分數",
            value=f"{int(predicted_toeic)} 分"
        )

        st.divider()

        # 讀書計畫
        st.subheader("AI 個人化讀書計畫")

        study_plan = []

        if reading_score < 0.5:
            study_plan.append("週一：TOEIC Part 7 閱讀練習")
            study_plan.append("週三：英文文章閱讀 20 分鐘")
            study_plan.append("週五：關鍵字定位訓練")

        if vocabulary_score < 0.5:
            study_plan.append("週二：背誦 30 個商業英文單字")
            study_plan.append("週四：多益同義字練習")

        if grammar_score < 0.5:
            study_plan.append("週六：文法時態練習")
            study_plan.append("週日：介系詞與句型訓練")

        if len(study_plan) == 0:
            st.success("目前能力穩定，建議持續保持練習！")
        else:
            for plan in study_plan:
                st.write(plan)

            st.divider()

            st.subheader("AI 推薦練習題目")

            recommend_questions = []

            if reading_score < 0.5:
                recommend_questions.append("📘 TOEIC Part 7 長篇閱讀練習")
                recommend_questions.append("📰 CNN 英文新聞閱讀")

            if vocabulary_score < 0.5:
                recommend_questions.append("📚 多益商業單字練習")

            if grammar_score < 0.5:
                recommend_questions.append("✏️ 英文時態練習")

            if len(recommend_questions) > 0:
                for question in recommend_questions:
                    st.write(question)

                st.divider()
                st.subheader("AI 推薦學習網站")

                if reading_score < 0.5:
                    st.link_button("🌐 CNN Learning English", "https://edition.cnn.com")
                    st.link_button("📰 BBC Learning English", "https://www.bbc.co.uk/learningenglish")

                if vocabulary_score < 0.5:
                    st.link_button("📚 TOEIC 單字練習", "https://www.vocabulary.com")

                if grammar_score < 0.5:
                    st.link_button("✏️ English Grammar", "https://learnenglish.britishcouncil.org/grammar")

            else:
                st.success("目前沒有特別需要加強的題目！")

        # 歷史資料
        save_file = f"users/{username}/results.csv"

        if os.path.exists(save_file):

            history_data = pd.read_csv(save_file)

            st.subheader("歷史分析紀錄")
            st.write(history_data)

            st.subheader("AI 學習成長趨勢")

            # 時間格式轉換
            history_data["time"] = pd.to_datetime(
                history_data["time"]
            )

            st.divider()
            
            # 建立折線圖
            st.subheader("AI 學習成長趨勢")

            fig_history = go.Figure()

            fig_history.add_trace(go.Scatter(
                x=history_data["time"],
                y=history_data["Reading"] * 100,
                mode="lines+markers",
                name="Reading",
                line=dict(color="#667eea", width=2),
                marker=dict(size=8)
            ))

            fig_history.add_trace(go.Scatter(
                x=history_data["time"],
                y=history_data["Vocabulary"] * 100,
                mode="lines+markers",
                name="Vocabulary",
                line=dict(color="#764ba2", width=2),
                marker=dict(size=8)
            ))

            fig_history.add_trace(go.Scatter(
                x=history_data["time"],
                y=history_data["Grammar"] * 100,
                mode="lines+markers",
                name="Grammar",
                line=dict(color="#f093fb", width=2),
                marker=dict(size=8)
            ))

            fig_history.add_trace(go.Scatter(
                x=history_data["time"],
                y=history_data["ML_TOEIC"] / 9.9,
                mode="lines+markers",
                name="TOEIC（%）",
                line=dict(color="#ff6b6b", width=2, dash="dash"),
                marker=dict(size=8)
            ))

            fig_history.update_layout(
                title="學習成長趨勢圖",
                xaxis_title="時間",
                yaxis_title="分數（%）",
                yaxis=dict(range=[0, 100]),
                plot_bgcolor=plot_bgcolor,
                paper_bgcolor=paper_bgcolor,
                font=dict(color=font_color, size=14),
                legend=dict(
                    bgcolor=plot_bgcolor,
                    bordercolor="#667eea",
                    borderwidth=1,
                    font=dict(color=font_color)
                ),
                hovermode="x unified"
            )

            st.plotly_chart(fig_history, use_container_width=True)

            # 成長分析
            if len(history_data) >= 2:

                st.subheader("📈 成長分析")

                col1, col2, col3 = st.columns(3)

                # 計算第一次與最後一次的差異
                reading_growth = int(
                    (history_data["Reading"].iloc[-1]
                    - history_data["Reading"].iloc[0]) * 100
                )

                vocabulary_growth = int(
                    (history_data["Vocabulary"].iloc[-1]
                    - history_data["Vocabulary"].iloc[0]) * 100
                )

                grammar_growth = int(
                    (history_data["Grammar"].iloc[-1]
                    - history_data["Grammar"].iloc[0]) * 100
                )

                with col1:
                    st.metric(
                        "Reading 成長",
                        f"{history_data['Reading'].iloc[-1] * 100:.0f}%",
                        delta=f"{reading_growth}%"
                    )

                with col2:
                    st.metric(
                        "Vocabulary 成長",
                        f"{history_data['Vocabulary'].iloc[-1] * 100:.0f}%",
                        delta=f"{vocabulary_growth}%"
                    )

                with col3:
                    st.metric(
                        "Grammar 成長",
                        f"{history_data['Grammar'].iloc[-1] * 100:.0f}%",
                        delta=f"{grammar_growth}%"
                    )

        else:
            st.info("目前還沒有歷史資料，請先儲存一次分析結果！")

        st.divider()

        # ✅ Machine Learning 預測（加上例外處理）
        st.subheader("Machine Learning TOEIC 預測")

        try:
            train_data = pd.read_csv("training_data.csv")

            X_train = train_data[["Reading", "Vocabulary", "Grammar"]]
            y_train = train_data["TOEIC"]

            model = LinearRegression()
            model.fit(X_train, y_train)

            student_data = [[reading_score, vocabulary_score, grammar_score]]
            ml_prediction = model.predict(student_data)

            st.success(f"Machine Learning 預測 TOEIC：約 {int(ml_prediction[0])} 分")

        except FileNotFoundError:
            st.error("找不到 training_data.csv，請確認檔案是否存在")
            ml_prediction = [predicted_toeic]

        except Exception as e:
            st.error(f"Machine Learning 發生錯誤：{e}")
            ml_prediction = [predicted_toeic]

        if username == "":
            st.warning("請先登入使用者名稱")

        # ✅ 儲存按鈕放在 analysis_ready 裡面
        if st.button("儲存分析結果", key="save_button"):

            save_data = pd.DataFrame([{
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Reading": reading_score,
                "Vocabulary": vocabulary_score,
                "Grammar": grammar_score,
                "Predicted_TOEIC": int(predicted_toeic),
                "ML_TOEIC": int(ml_prediction[0])
            }])

            os.makedirs("users", exist_ok=True)
            user_folder = f"users/{username}"
            os.makedirs(user_folder, exist_ok=True)

            save_file = f"{user_folder}/results.csv"

            if os.path.exists(save_file):
                old_data = pd.read_csv(save_file)
                new_data = pd.concat([old_data, save_data], ignore_index=True)
                new_data.to_csv(save_file, index=False)
            else:
                save_data.to_csv(save_file, index=False)

            st.success("分析結果已儲存")

            if predicted_toeic >= 750:
                st.success("AI 評估：高分潛力")
            elif predicted_toeic >= 550:
                st.warning("AI 評估：持續進步中")
            else:
                st.error("AI 評估：需加強基礎能力")

# 練習題功能
if st.session_state.quiz_mode:

    st.markdown(f"""
    <div style="
        background: {card_bg};
        border-radius: 20px;
        padding: 30px;
        box-shadow: {card_shadow};
        margin-top: 30px;
    ">
        <h3 style="color: #667eea !important; font-weight: 700;">
            📝 TOEIC 練習題
        </h3>
        <p style="color: {text_color} !important; font-size: 0.9rem;">
            選擇題型開始練習，完成後自動記錄答對率！
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 選擇題型
    quiz_type = st.selectbox(
        "選擇練習題型",
        ["Reading", "Vocabulary", "Grammar"],
        key="quiz_type"
    )

    # 初始化答題狀態
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False
    if "last_quiz_type" not in st.session_state:
        st.session_state.last_quiz_type = quiz_type

    # 題目數量選擇
    num_questions = st.slider(
        "選擇題目數量",
        min_value=3,
        max_value=8,
        value=5,
        key="num_questions"
    )

    # 如果換了題型或題目數量，重置狀態
    if (st.session_state.last_quiz_type != quiz_type or
        "quiz_questions" not in st.session_state):
        random.shuffle(QUESTIONS[quiz_type])
        st.session_state.quiz_questions = QUESTIONS[quiz_type][:num_questions]
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_finished = False
        st.session_state.last_quiz_type = quiz_type

    questions = st.session_state.quiz_questions
    total = len(questions)

    if not st.session_state.quiz_finished:

        current_q = questions[st.session_state.quiz_index]

        # 進度條
        progress = st.session_state.quiz_index / total
        st.progress(progress)
        st.write(f"第 {st.session_state.quiz_index + 1} 題 / 共 {total} 題")

        # 題目
        st.markdown(f"""
        <div style="
            background: {card_bg};
            border-radius: 15px;
            padding: 25px;
            box-shadow: {card_shadow};
            margin: 15px 0;
            border-left: 4px solid #667eea;
        ">
            <p style="color: {text_color} !important; font-size: 1rem; white-space: pre-line;">
                {current_q["question"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 選項
        selected = st.radio(
            "請選擇答案",
            current_q["options"],
            key=f"q_{st.session_state.quiz_index}",
            label_visibility="collapsed"
        )

        if not st.session_state.quiz_answered:
            if st.button("確認答案 ✓", key="confirm_answer"):
                st.session_state.quiz_answered = True
                selected_letter = selected[0]

                if selected_letter == current_q["answer"]:
                    st.session_state.quiz_score += 1
                    st.success("✅ 答對了！")
                else:
                    st.error(f"❌ 答錯了！正確答案是 {current_q['answer']}")

                st.info(f"📖 解析：{current_q['explanation']}")

        else:
            selected_letter = selected[0]
            if selected_letter == current_q["answer"]:
                st.success("✅ 答對了！")
            else:
                st.error(f"❌ 答錯了！正確答案是 {current_q['answer']}")

            st.info(f"📖 解析：{current_q['explanation']}")

            if st.session_state.quiz_index + 1 < total:
                if st.button("下一題 →", key="next_question"):
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_answered = False
                    st.rerun()
            else:
                if st.button("查看結果 🎯", key="show_result"):
                    st.session_state.quiz_finished = True
                    st.rerun()

    else:
        # 顯示結果
        score = st.session_state.quiz_score
        accuracy = score / total

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            margin: 20px 0;
        ">
            <h2 style="color: white !important; font-size: 2rem;">🎯 練習結果</h2>
            <p style="color: white !important; font-size: 1.5rem; font-weight: 700;">
                {score} / {total} 題答對
            </p>
            <p style="color: rgba(255,255,255,0.9) !important; font-size: 1.2rem;">
                答對率：{int(accuracy * 100)}%
            </p>
        </div>
        """, unsafe_allow_html=True)

        if accuracy >= 0.8:
            st.success("🌟 表現優秀！繼續保持！")
        elif accuracy >= 0.5:
            st.warning("📚 還不錯！多加練習可以更好！")
        else:
            st.error("💪 需要加強！建議多看解析後重新練習！")

        # 自動更新答對率
        if username:
            st.info(f"✅ 已自動將 {quiz_type} 答對率（{int(accuracy * 100)}%）更新到您的分析紀錄！")

            save_data = pd.DataFrame([{
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Reading": accuracy if quiz_type == "Reading" else 0.5,
                "Vocabulary": accuracy if quiz_type == "Vocabulary" else 0.5,
                "Grammar": accuracy if quiz_type == "Grammar" else 0.5,
                "Predicted_TOEIC": int((accuracy * 0.5 + 0.5 * 0.3 + 0.5 * 0.2) * 990),
                "ML_TOEIC": int((accuracy * 0.5 + 0.5 * 0.3 + 0.5 * 0.2) * 990)
            }])

            os.makedirs("users", exist_ok=True)
            user_folder = f"users/{username}"
            os.makedirs(user_folder, exist_ok=True)
            save_file = f"{user_folder}/results.csv"

            if os.path.exists(save_file):
                old_data = pd.read_csv(save_file)
                new_data = pd.concat([old_data, save_data], ignore_index=True)
                new_data.to_csv(save_file, index=False)
            else:
                save_data.to_csv(save_file, index=False)
        else:
            st.warning("⚠️ 請先登入使用者名稱才能儲存練習紀錄！")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 重新練習（換一組題目）", key="restart_quiz"):
                random.shuffle(QUESTIONS[quiz_type])
                st.session_state.quiz_questions = QUESTIONS[quiz_type][:num_questions]
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answered = False
                st.session_state.quiz_finished = False
                st.rerun()
        with col2:
            if st.button("📊 查看分析", key="go_analysis"):
                st.session_state.quiz_mode = False
                st.rerun()

# AI 對話功能
if st.session_state.chat_mode:

    st.markdown(f"""
    <div style="
        background: {card_bg};
        border-radius: 20px;
        padding: 30px;
        box-shadow: {card_shadow};
        margin-top: 30px;
    ">
        <h3 style="color: #667eea !important; font-weight: 700;">
            💬 AI 英文學習助教
        </h3>
        <p style="color: {text_color} !important; font-size: 0.9rem;">
            有任何英文或 TOEIC 相關問題都可以問我！
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 初始化對話紀錄
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div style="
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 15px 15px 0px 15px;
                padding: 15px 20px;
                margin: 10px 0;
                margin-left: 20%;
            ">
                <p style="color: white !important; margin: 0;">
                    👤 {message["content"]}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                background: {card_bg};
                border-radius: 15px 15px 15px 0px;
                padding: 15px 20px;
                margin: 10px 0;
                margin-right: 20%;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            ">
                <p style="color: {text_color} !important; margin: 0;">
                    🤖 {message["content"]}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # 輸入框
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_input(
            "請輸入問題",
            placeholder="例如：TOEIC Part 7 怎麼準備？",
            key="chat_input",
            label_visibility="collapsed"
        )

    with col2:
        send_button = st.button("送出 ➤", key="send_chat")

    if send_button and user_input:

        # 加入使用者訊息
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("AI 思考中..."):

            try:
                from groq import Groq

                client = Groq(
                    api_key=st.secrets["GROQ_API_KEY"]
                )

                chat_history = [
                    {
                        "role": "system",
                        "content": """你是一位專業的英文與 TOEIC 學習助教。
請用繁體中文回答，語氣親切、專業。
回答要具體、實用，盡量條列式呈現。
專注在英文學習、TOEIC 考試相關的問題。"""
                    }
                ]

                for msg in st.session_state.messages:
                    chat_history.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=chat_history
                )

                ai_reply = response.choices[0].message.content

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_reply
                })

                st.rerun()

            except Exception as e:
                st.error(f"AI 回覆失敗：{e}")

    # 清除對話按鈕
    if len(st.session_state.messages) > 0:
        if st.button("🗑️ 清除對話紀錄", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()

st.divider()

# 頁尾
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin-top: 50px;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
">
    <p style="
        color: white !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 5px;
    ">🌍 EduInsight</p>
    <p style="
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.85rem;
        margin: 0;
    ">AI 英文學習弱點分析平台 © 2025</p>
    <p style="
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.8rem;
        margin-top: 5px;
    ">Powered by Groq AI × Machine Learning</p>
</div>
""", unsafe_allow_html=True)