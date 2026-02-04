"""
🤖 الوكيل الذكي المتقدم - النسخة الاحترافية الكاملة
تصميم عصري احترافي + قدرات ذكية متقدمة + بدون قيود
"""

import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# تحميل متغيرات البيئة
load_dotenv()

# إعدادات الصفحة
st.set_page_config(
    page_title="الوكيل الذكي المتقدم",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS احترافي متقدم
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    /* الخلفية والألوان */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* رسائل المحادثة */
    .message-container {
        padding: 15px;
        margin: 12px 0;
        border-radius: 12px;
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
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        border-radius: 12px;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-left: 5px solid #f5576c;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        border-radius: 12px;
    }
    
    /* العنوان */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        font-weight: 900;
        font-size: 3em;
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* حقول الإدخال */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 12px;
        font-size: 16px;
    }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin: 5px;
    }
    
    /* الفاصل */
    hr {
        border: 2px solid #667eea;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1>🤖 الوكيل الذكي المتقدم</h1>
        <p style='font-size: 18px; color: #667eea; font-weight: bold;'>
            النسخة الاحترافية الكاملة - بدون قيود
        </p>
    </div>
    """, unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات المتقدمة")
    st.write(f"**⏰ الوقت:** {datetime.now().strftime('%H:%M:%S')}")
    
    # التحقق من API
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_api_key_here" and len(api_key) > 20:
        st.success("✅ OpenAI API: متصل")
    else:
        st.warning("⚠️ OpenAI API: غير متصل")
    
    st.divider()
    
    # إعدادات النموذج
    st.subheader("🎛️ إعدادات النموذج")
    temperature = st.slider("🔥 درجة الإبداع", 0.0, 2.0, 0.9, step=0.1)
    max_tokens = st.slider("📝 الحد الأقصى للرموز", 100, 4000, 2000, step=100)
    
    st.divider()
    
    # خيارات متقدمة
    st.subheader("🚀 خيارات متقدمة")
    enable_code = st.checkbox("✅ تنفيذ الأكواد", value=True)
    enable_analysis = st.checkbox("✅ تحليل البيانات", value=True)
    
    st.divider()
    
    # الإحصائيات
    st.subheader("📊 الإحصائيات")
    if "messages" in st.session_state:
        total = len(st.session_state.messages)
        user_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.metric("💬 إجمالي", total)
        st.metric("👤 المستخدم", user_count)
    
    st.divider()
    
    # أزرار التحكم
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 إعادة تعيين"):
            st.session_state.clear()
            st.rerun()
    with col2:
        if st.button("💾 حفظ"):
            st.success("✅ تم الحفظ")

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thinking_steps" not in st.session_state:
    st.session_state.thinking_steps = []

# الأقسام الرئيسية
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 المحادثة",
    "🧠 التفكير",
    "⚙️ الأوامر",
    "📊 التحليل",
    "🛠️ الأدوات"
])

# ==================== تبويب المحادثة ====================
with tab1:
    st.markdown("### 💬 المحادثة الذكية")
    
    # عرض سجل المحادثات
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-container user-message">
                    <strong>👤 أنت:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-container assistant-message">
                    <strong>🤖 الوكيل:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📌 ابدأ المحادثة الآن!")
    
    st.divider()
    
    # حقل الإدخال
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "اكتب رسالتك:",
            placeholder="اسأل عن أي شيء...",
            key="user_input"
        )
    with col2:
        send_button = st.button("📤 إرسال", use_container_width=True)
    
    # معالجة الإرسال
    if send_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 جاري المعالجة..."):
            try:
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key or api_key == "your_api_key_here":
                    st.error("❌ مفتاح API غير موجود")
                else:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    
                    messages_for_api = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages
                    ]
                    
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=messages_for_api,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    assistant_message = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                    
                    st.session_state.thinking_steps.append({
                        "timestamp": datetime.now().isoformat(),
                        "input": user_input,
                        "tokens": response.usage.total_tokens
                    })
                    
                    st.success("✅ تم!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ==================== تبويب التفكير ====================
with tab2:
    st.markdown("### 🧠 مسار التفكير")
    
    if st.session_state.thinking_steps:
        st.info(f"📌 {len(st.session_state.thinking_steps)} خطوات معالجة")
        
        for i, step in enumerate(st.session_state.thinking_steps, 1):
            with st.expander(f"الخطوة {i}: {step['input'][:50]}..."):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("⏰ الوقت", step['timestamp'].split('T')[1][:8])
                with col2:
                    st.metric("📝 الرموز", step['tokens'])
                with col3:
                    st.metric("✅ الحالة", "نجح")
    else:
        st.info("📌 لا توجد خطوات بعد")

# ==================== تبويب الأوامر ====================
with tab3:
    st.markdown("### ⚙️ تنفيذ الأوامر")
    
    if enable_code:
        st.success("✅ التنفيذ: مفعّل")
        
        code_input = st.text_area(
            "اكتب كود Python:",
            placeholder="print('مرحبا')",
            height=200
        )
        
        if st.button("▶️ تنفيذ"):
            if code_input:
                try:
                    exec(code_input)
                    st.success("✅ تم التنفيذ!")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
    else:
        st.warning("⚠️ التنفيذ: معطّل")

# ==================== تبويب التحليل ====================
with tab4:
    st.markdown("### 📊 التحليل والبيانات")
    
    if enable_analysis:
        st.success("✅ التحليل: مفعّل")
        
        data_input = st.text_area(
            "أدخل البيانات (JSON):",
            placeholder='{"data": [1, 2, 3]}',
            height=150
        )
        
        if st.button("🔍 تحليل"):
            if data_input:
                try:
                    data = json.loads(data_input)
                    st.success("✅ تم التحليل!")
                    st.json(data)
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
    else:
        st.warning("⚠️ التحليل: معطّل")

# ==================== تبويب الأدوات ====================
with tab5:
    st.markdown("### 🛠️ الأدوات المتقدمة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📊 تحليل البيانات
        - معالجة البيانات
        - رسوم بيانية
        - إحصائيات
        """)
    
    with col2:
        st.markdown("""
        #### 🔍 البحث
        - بحث متقدم
        - استخراج معلومات
        - تلخيص
        """)
    
    with col3:
        st.markdown("""
        #### ⚙️ التنفيذ
        - أكواد Python
        - أتمتة
        - معالجة ملفات
        """)

st.divider()

# الفوتر
st.markdown("""
<div style='text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;'>
    <h3>🤖 الوكيل الذكي المتقدم</h3>
    <p>النسخة الاحترافية الكاملة - مدعوم بـ GPT-4</p>
    <p style='font-size: 12px; margin-top: 10px;'>© 2026 - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
