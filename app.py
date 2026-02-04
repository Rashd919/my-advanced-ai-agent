"""
🤖 Rashed Ai - منصة ذكية متقدمة
واجهة بسيطة وأنيقة مثل Manus
"""

import streamlit as st
import openai
from datetime import datetime
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعدادات الصفحة
st.set_page_config(
    page_title="Rashed Ai",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS احترافي - تصميم بسيط وأنيق
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    /* الخلفية */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* رسائل المحادثة */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        margin-left: 50px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideIn 0.3s ease-in-out;
    }
    
    .assistant-message {
        background: #2a2a3e;
        color: #e0e0e0;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        margin-right: 50px;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        animation: slideIn 0.3s ease-in-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* العنوان */
    .title-container {
        text-align: center;
        padding: 30px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 30px;
    }
    
    .title-container h1 {
        color: white;
        font-size: 2.5em;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .title-container p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1em;
        margin: 10px 0 0 0;
    }
    
    /* حقل الإدخال */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 15px 20px;
        font-size: 16px;
        background: #1a1a2e;
        color: white;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888;
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* منطقة المحادثة */
    .chat-container {
        background: rgba(26, 26, 46, 0.5);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* الفاصل */
    hr {
        border: none;
        border-top: 2px solid rgba(102, 126, 234, 0.3);
        margin: 20px 0;
    }
    
    /* النص العام */
    body {
        color: #e0e0e0;
    }
    
    /* الرسائل */
    .message-text {
        word-wrap: break-word;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# العنوان
st.markdown("""
<div class="title-container">
    <h1>🤖 Rashed Ai</h1>
    <p>منصة ذكية متقدمة - بدون قيود</p>
</div>
""", unsafe_allow_html=True)

# منطقة المحادثة
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if st.session_state.messages:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="message-text">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="message-text">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 50px; color: #888;">
        <h2>👋 مرحباً بك في Rashed Ai</h2>
        <p>ابدأ المحادثة الآن - اسأل عن أي شيء!</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# حقل الإدخال والإرسال
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "اكتب رسالتك:",
        placeholder="مثال: احسب جذر 144 أو اكتب لي قصة أو علمني البرمجة...",
        key="user_input"
    )

with col2:
    send_button = st.button("📤 إرسال", use_container_width=True)

# معالجة الإرسال
if send_button and user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # إظهار رسالة التحميل
    with st.spinner("🤔 جاري المعالجة..."):
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            
            # التحقق من مفتاح API
            if not api_key or api_key == "your_api_key_here" or len(api_key) < 20:
                error_msg = "❌ خطأ: مفتاح OpenAI API غير صحيح أو غير موجود"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.error(error_msg)
            else:
                # تعيين مفتاح API
                openai.api_key = api_key
                
                # تحضير الرسائل
                messages_for_api = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages
                ]
                
                # استدعاء OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages_for_api,
                    temperature=0.9,
                    max_tokens=2000
                )
                
                # استخراج الرد
                assistant_message = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # إعادة تحميل الصفحة
                st.rerun()
                
        except Exception as e:
            error_msg = f"❌ خطأ: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.error(error_msg)
            st.info("💡 تأكد من صحة مفتاح API والاتصال بالإنترنت")

# الفوتر
st.markdown("""
<div style='text-align: center; margin-top: 40px; padding: 20px; color: #888; font-size: 0.9em;'>
    <p>© 2026 Rashed Ai - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
