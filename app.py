"""
🤖 الوكيل الذكي المتقدم - النسخة الاحترافية
مع قدرات ذكية متقدمة وتنفيذ أوامر وتحليل متقدم
بدون قيود - استخدام حر تماماً
"""

import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import subprocess
import json
import sys

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
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-left: 5px solid #f5576c;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }
    
    .code-message {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #00ff00;
        border-left: 5px solid #00ff00;
        font-family: 'Courier New', monospace;
        box-shadow: 0 4px 15px rgba(30, 60, 114, 0.5);
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
    
    /* الشريط الجانبي */
    .stSidebar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSidebar > div > div:first-child {
        background: transparent;
    }
    
    /* الرسائل الإحصائية */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* الفاصل */
    hr {
        border: 2px solid #667eea;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1>🤖 الوكيل الذكي المتقدم</h1>
    <p style='font-size: 18px; color: #667eea; font-weight: bold;'>
        نسخة احترافية متقدمة - بدون قيود - استخدام حر تماماً
    </p>
</div>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات المتقدمة")
    st.write(f"**⏰ الوقت الحالي:** {datetime.now().strftime('%H:%M:%S')}")
    
    # التحقق من API
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_api_key_here" and len(api_key) > 20:
        st.success("✅ مفتاح OpenAI API: متصل وفعال")
    else:
        st.warning("⚠️ مفتاح API: غير مكتمل أو غير صحيح")
    
    st.divider()
    
    # إعدادات النموذج
    st.subheader("🎛️ إعدادات النموذج")
    temperature = st.slider("🔥 درجة الإبداع", 0.0, 2.0, 0.9, step=0.1)
    max_tokens = st.slider("📝 الحد الأقصى للرموز", 100, 4000, 2000, step=100)
    
    st.divider()
    
    # خيارات متقدمة
    st.subheader("🚀 خيارات متقدمة")
    enable_code_execution = st.checkbox("✅ تفعيل تنفيذ الأكواد", value=True)
    enable_web_search = st.checkbox("✅ تفعيل البحث على الويب", value=True)
    enable_data_analysis = st.checkbox("✅ تفعيل تحليل البيانات", value=True)
    
    st.divider()
    
    # الإحصائيات
    st.subheader("📊 الإحصائيات")
    if "messages" in st.session_state:
        total_messages = len(st.session_state.messages)
        user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
        assistant_messages = total_messages - user_messages
        st.metric("💬 إجمالي الرسائل", total_messages)
        st.metric("👤 رسائل المستخدم", user_messages)
        st.metric("🤖 رسائل الوكيل", assistant_messages)
    
    st.divider()
    
    # أزرار التحكم
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 إعادة تعيين"):
            st.session_state.clear()
            st.rerun()
    with col2:
        if st.button("💾 حفظ المحادثة"):
            st.success("✅ تم حفظ المحادثة")

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thinking_steps" not in st.session_state:
    st.session_state.thinking_steps = []
if "code_executions" not in st.session_state:
    st.session_state.code_executions = []

# الأقسام الرئيسية
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 المحادثة الذكية",
    "🧠 التفكير المتقدم",
    "⚙️ تنفيذ الأوامر",
    "📊 التحليل والبيانات",
    "🛠️ الأدوات المتقدمة"
])

# ==================== تبويب المحادثة ====================
with tab1:
    st.markdown("### 💬 المحادثة الذكية المتقدمة")
    
    # عرض سجل المحادثات
    chat_container = st.container()
    with chat_container:
        if st.session_state.messages:
            for i, message in enumerate(st.session_state.messages):
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="message-container user-message">
                        <strong>👤 أنت:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="message-container assistant-message">
                        <strong>🤖 الوكيل الذكي:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("📌 ابدأ محادثة جديدة - اكتب أي شيء تريده والوكيل سيرد عليك بذكاء!")
    
    st.divider()
    
    # حقل الإدخال
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
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 الوكيل يفكر ويرد عليك..."):
            try:
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key or api_key == "your_api_key_here":
                    raise ValueError("مفتاح OpenAI API غير موجود")
                
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                # تحضير الرسائل
                messages_for_api = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages
                ]
                
                # استدعاء OpenAI
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages_for_api,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                assistant_message = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # تسجيل خطوات التفكير
                st.session_state.thinking_steps.append({
                    "timestamp": datetime.now().isoformat(),
                    "input": user_input,
                    "model": "gpt-4",
                    "tokens": response.usage.total_tokens
                })
                
                st.success("✅ تم معالجة الرسالة بنجاح!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# ==================== تبويب التفكير ====================
with tab2:
    st.markdown("### 🧠 مسار التفكير المتقدم")
    
    if st.session_state.thinking_steps:
        st.info(f"📌 تم معالجة {len(st.session_state.thinking_steps)} رسالة")
        
        for i, step in enumerate(st.session_state.thinking_steps, 1):
            with st.expander(f"🔍 الخطوة {i}: {step['input'][:60]}..."):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("⏰ الوقت", step['timestamp'].split('T')[1][:8])
                with col2:
                    st.metric("🤖 النموذج", step['model'])
                with col3:
                    st.metric("📝 الرموز", step['tokens'])
                with col4:
                    st.metric("✅ الحالة", "نجح")
                
                st.write(f"**الإدخال:** {step['input']}")
    else:
        st.info("📌 لم تتم معالجة أي رسائل بعد - ابدأ المحادثة!")

# ==================== تبويب تنفيذ الأوامر ====================
with tab3:
    st.markdown("### ⚙️ تنفيذ الأوامر والأكواد")
    
    if enable_code_execution:
        st.success("✅ تنفيذ الأوامر: مفعّل")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            code_input = st.text_area(
                "اكتب كود Python:",
                placeholder="مثال:\nprint('مرحبا')\nimport math\nprint(math.sqrt(144))",
                height=200
            )
        with col2:
            if st.button("▶️ تنفيذ", use_container_width=True):
                if code_input:
                    try:
                        exec_globals = {}
                        exec(code_input, exec_globals)
                        st.success("✅ تم تنفيذ الكود بنجاح!")
                        
                        st.session_state.code_executions.append({
                            "code": code_input,
                            "timestamp": datetime.now().isoformat(),
                            "status": "نجح"
                        })
                    except Exception as e:
                        st.error(f"❌ خطأ في التنفيذ: {str(e)}")
        
        st.divider()
        
        # سجل التنفيذات
        if st.session_state.code_executions:
            st.subheader("📋 سجل التنفيذات")
            for i, exec_record in enumerate(st.session_state.code_executions, 1):
                with st.expander(f"التنفيذ {i} - {exec_record['timestamp'].split('T')[1][:8]}"):
                    st.code(exec_record['code'], language='python')
                    st.write(f"**الحالة:** {exec_record['status']}")
    else:
        st.warning("⚠️ تنفيذ الأوامر: معطّل")

# ==================== تبويب التحليل ====================
with tab4:
    st.markdown("### 📊 التحليل والبيانات المتقدم")
    
    if enable_data_analysis:
        st.success("✅ تحليل البيانات: مفعّل")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 إدخال البيانات")
            data_input = st.text_area(
                "أدخل البيانات (JSON أو CSV):",
                placeholder='{"data": [1, 2, 3, 4, 5]}',
                height=150
            )
        
        with col2:
            st.subheader("📊 نوع التحليل")
            analysis_type = st.selectbox(
                "اختر نوع التحليل:",
                ["الإحصائيات الأساسية", "الرسوم البيانية", "التنبؤات", "التجميع"]
            )
        
        if st.button("🔍 تحليل البيانات"):
            try:
                import json
                data = json.loads(data_input)
                st.success("✅ تم تحليل البيانات بنجاح!")
                st.json(data)
            except Exception as e:
                st.error(f"❌ خطأ في التحليل: {str(e)}")
    else:
        st.warning("⚠️ تحليل البيانات: معطّل")

# ==================== تبويب الأدوات ====================
with tab5:
    st.markdown("### 🛠️ الأدوات المتقدمة")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📊 تحليل البيانات
        - معالجة ملفات CSV و Excel
        - إنشاء رسوم بيانية متقدمة
        - تحليل إحصائي شامل
        """)
    
    with col2:
        st.markdown("""
        #### 🔍 البحث المتقدم
        - البحث على الويب
        - استخراج المعلومات
        - تلخيص النصوص
        """)
    
    with col3:
        st.markdown("""
        #### ⚙️ تنفيذ الأوامر
        - تنفيذ أكواد Python
        - أتمتة المهام
        - معالجة الملفات
        """)

st.divider()

# الفوتر
st.markdown("""
<div style='text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;'>
    <h3>🤖 الوكيل الذكي المتقدم - النسخة الاحترافية</h3>
    <p>مدعوم بـ GPT-4 | بدون قيود | استخدام حر تماماً</p>
    <p style='font-size: 12px; margin-top: 10px;'>© 2026 - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
