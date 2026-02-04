"""
تطبيق Streamlit الرئيسي للوكيل الذكي المتقدم
نسخة محسّنة مع تكامل OpenAI الفعلي
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إعدادات الصفحة
st.set_page_config(
    page_title="الوكيل الذكي المتقدم",
    page_icon="🤖",
    layout="wide"
)

# CSS للعربية
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    .message-container {
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

# العنوان
st.title("🤖 الوكيل الذكي المتقدم")

# التحقق من API
api_key = os.getenv("OPENAI_API_KEY")

# الشريط الجانبي
with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.write(f"**الوقت**: {datetime.now().strftime('%H:%M:%S')}")
    
    # عرض حالة API
    if api_key and api_key != "your_api_key_here":
        st.success("✅ مفتاح API موجود وصحيح")
    else:
        st.warning("⚠️ مفتاح API غير موجود أو غير صحيح")
    
    # إعدادات النموذج
    st.subheader("إعدادات النموذج")
    temperature = st.slider("درجة الإبداع", 0.0, 1.0, 0.7)
    max_tokens = st.slider("الحد الأقصى للرموز", 100, 2000, 500)
    
    if st.button("🔄 إعادة تعيين"):
        st.session_state.clear()
        st.rerun()

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thinking_steps" not in st.session_state:
    st.session_state.thinking_steps = []
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 500

# تحديث الإعدادات من الشريط الجانبي
st.session_state.temperature = temperature
st.session_state.max_tokens = max_tokens

# الأقسام
tab1, tab2, tab3 = st.tabs(["💬 المحادثة", "🧠 التفكير", "🛠️ الأدوات"])

with tab1:
    st.header("💬 المحادثة")
    
    # عرض سجل المحادثات
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-container user-message">
                    <strong>👤 أنت:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-container assistant-message">
                    <strong>🤖 الوكيل:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📌 ابدأ محادثة جديدة بكتابة رسالة أدناه")
    
    # حقل الإدخال
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("اكتب رسالتك:", key="user_input")
    with col2:
        send_button = st.button("📤 إرسال")
    
    # معالجة الإرسال
    if send_button and user_input:
        # إضافة الرسالة للسجل
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # عرض رسالة التحميل
        with st.spinner("جاري معالجة الرسالة..."):
            try:
                # التحقق من وجود مفتاح API
                if not api_key or api_key == "your_api_key_here":
                    raise ValueError("مفتاح OpenAI API غير موجود أو غير صحيح")
                
                # استيراد OpenAI
                from openai import OpenAI
                
                # إنشاء عميل OpenAI
                client = OpenAI(api_key=api_key)
                
                # استدعاء OpenAI API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens
                )
                
                # استخراج الرد
                assistant_message = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # إضافة خطوات التفكير
                st.session_state.thinking_steps.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_input": user_input,
                    "model": "gpt-3.5-turbo",
                    "tokens_used": response.usage.total_tokens
                })
                
                st.success("✅ تم معالجة الرسالة بنجاح")
                st.rerun()
            except ValueError as e:
                st.error(f"❌ خطأ في الإعدادات: {str(e)}")
            except Exception as e:
                st.error(f"❌ خطأ في معالجة الرسالة: {str(e)}")

with tab2:
    st.header("🧠 مسار التفكير")
    if st.session_state.thinking_steps:
        st.info("📌 خطوات معالجة الرسائل:")
        for i, step in enumerate(st.session_state.thinking_steps, 1):
            with st.expander(f"الخطوة {i}: {step['user_input'][:50]}..."):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("الطابع الزمني", step['timestamp'].split('T')[1][:8])
                with col2:
                    st.metric("النموذج", step['model'])
                with col3:
                    st.metric("الرموز المستخدمة", step['tokens_used'])
                st.write(f"**الإدخال:** {step['user_input']}")
    else:
        st.info("📌 لم تتم معالجة أي رسائل بعد")

with tab3:
    st.header("🛠️ الأدوات")
    st.info("📌 الأدوات المتاحة:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 تحليل البيانات")
        st.write("تحليل وتصور البيانات الإحصائية")
    
    with col2:
        st.subheader("🔍 البحث على الويب")
        st.write("البحث والحصول على معلومات من الإنترنت")
    
    with col3:
        st.subheader("⚙️ تنفيذ الأكواد")
        st.write("تنفيذ أكواد Python بأمان")

st.divider()
st.markdown("<p style='text-align: center; color: #666;'>🤖 الوكيل الذكي - نسخة 2.0 | مدعوم بـ OpenAI</p>", unsafe_allow_html=True)
