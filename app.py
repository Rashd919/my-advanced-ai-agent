"""
🤖 Rashed Ai - منصة ذكية متقدمة
تصميم عصري حديث احترافي 100%
"""

import streamlit as st
import requests
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

# CSS عصري وحديث - تصميم احترافي 100%
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    /* الخلفية الرئيسية */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* حاوية الرسائل - تصميم حديث */
    .user-msg {
        display: flex;
        justify-content: flex-end;
        margin: 12px 0;
    }
    
    .user-msg-bubble {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: white;
        padding: 14px 18px;
        border-radius: 20px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
        font-size: 15px;
        line-height: 1.5;
    }
    
    .assistant-msg {
        display: flex;
        justify-content: flex-start;
        margin: 12px 0;
    }
    
    .assistant-msg-bubble {
        background: linear-gradient(135deg, #2d3561 0%, #3d4a7a 100%);
        color: #e8f0ff;
        padding: 14px 18px;
        border-radius: 20px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(45, 53, 97, 0.5);
        font-size: 15px;
        line-height: 1.5;
        border-left: 4px solid #00d4ff;
    }
    
    /* العنوان الرئيسي */
    .header-section {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        border-radius: 25px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
    }
    
    .header-section h1 {
        color: white;
        font-size: 3em;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: 1px;
    }
    
    .header-section p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2em;
        margin: 12px 0 0 0;
        font-weight: 500;
    }
    
    /* منطقة المحادثة */
    .chat-area {
        background: rgba(45, 53, 97, 0.3);
        border-radius: 25px;
        padding: 25px;
        margin: 25px 0;
        min-height: 450px;
        max-height: 650px;
        overflow-y: auto;
        border: 2px solid rgba(0, 212, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* شريط الإدخال */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #00d4ff;
        padding: 16px 20px;
        font-size: 16px;
        background: #1a1a2e;
        color: #e8f0ff;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #666;
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%);
    }
    
    /* الفاصل */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
        margin: 25px 0;
    }
    
    /* رسالة الترحيب */
    .welcome-msg {
        text-align: center;
        padding: 60px 30px;
        color: #888;
    }
    
    .welcome-msg h2 {
        color: #00d4ff;
        font-size: 2em;
        margin: 0 0 15px 0;
    }
    
    .welcome-msg p {
        color: #aaa;
        font-size: 1.1em;
        margin: 0;
    }
    
    /* الفوتر */
    .footer-section {
        text-align: center;
        padding: 25px;
        color: #666;
        font-size: 0.9em;
        border-top: 2px solid rgba(0, 212, 255, 0.1);
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# العنوان الرئيسي
st.markdown("""
<div class="header-section">
    <h1>🤖 Rashed Ai</h1>
    <p>منصة ذكية متقدمة - بدون تكاليف</p>
</div>
""", unsafe_allow_html=True)

# منطقة المحادثة
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

if st.session_state.messages:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-msg">
                <div class="user-msg-bubble">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-msg">
                <div class="assistant-msg-bubble">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="welcome-msg">
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

# دالة لكتابة شعر جميل
def write_poem(topic):
    """كتابة شعر جميل عن الموضوع المطلوب"""
    poems = {
        "الحب": """🌹 شعر عن الحب 🌹

في قلبي حب لا ينتهي
مثل نجم يضيء الليل البعيد
أنتِ نور عيني وسر سعادتي
وفي كل لحظة أشعر بك بجانبي

كلماتك عسل على شفتي
وابتسامتك شمس تضيء دنيايا
أحبك بكل ما في قلبي
وستبقين الحب الأول والأخير""",
        
        "الحياة": """🌟 شعر عن الحياة 🌟

الحياة رحلة جميلة
مليئة بالأمل والأحلام
نسير فيها خطوة خطوة
نبني أملنا من جديد كل يوم

لا تستسلم للحزن والألم
فالحياة أجمل من كل هذا
ابحث عن نورك الخاص
وسترى الجمال في كل شيء""",
        
        "الأمل": """💫 شعر عن الأمل 💫

الأمل هو شعاع نور
يضيء ظلام الليل الطويل
يا أمل كن معي دائماً
في كل خطوة وفي كل تنفس

لا تتركني وحيداً في الطريق
كن نجمي الذي يهديني
الأمل هو كل ما أملكه
وفيك أستودع كل أحلامي""",
        
        "الصداقة": """👥 شعر عن الصداقة 👥

صديقي أنت أغلى من الذهب
أنت نور في ظلام الليل
معك أشعر بالأمان والحب
وفي قلبك مكان خاص لي

نحن معاً نبني أحلامنا
نضحك ونبكي معاً
الصداقة أجمل هدية
وأنت أغلى صديق لي""",
    }
    
    # البحث عن الموضوع
    for key, poem in poems.items():
        if key in topic:
            return poem
    
    # شعر عام جميل
    return f"""✨ شعر جميل عن {topic} ✨

في كل لحظة من حياتي
أفكر في {topic} وجماله
يملأ قلبي بالسعادة والحب
ويجعل حياتي أكثر جمالاً وألواناً

{topic} هو الحياة الحقيقية
هو الشعور الذي يجعلنا أحياء
فشكراً لك يا {topic}
على كل اللحظات الجميلة التي أعطيتها لي"""

# دالة لتوليد ردود ذكية
def generate_smart_response(messages):
    """توليد رد ذكي بدون الحاجة لـ API"""
    user_message = messages[-1]["content"].lower()
    
    # التحقق من طلبات الشعر
    if "شعر" in user_message or "قصيدة" in user_message:
        # استخراج الموضوع
        topics = ["الحب", "الحياة", "الأمل", "الصداقة", "الحزن", "الفرح"]
        for topic in topics:
            if topic in user_message:
                return write_poem(topic)
        # إذا لم يتم تحديد موضوع، اطلب منه أن يحدد
        return "🎭 موضوع شعري جميل! أي موضوع تريد أن أكتب عنه؟\n\nاختر من:\n🌹 الحب\n🌟 الحياة\n💫 الأمل\n👥 الصداقة\n😢 الحزن\n😊 الفرح"
    
    # قاموس الردود الذكية
    smart_responses = {
        "كيف حالك": "🌟 حالي رائع! أنا هنا لمساعدتك في أي شيء. كيف يمكنني خدمتك اليوم؟",
        "مرحبا": "👋 مرحباً! أنا Rashed Ai، وكيل ذكي متقدم. سعيد بلقاءك! ما الذي تود فعله؟",
        "شكرا": "😊 على الرحب والسعة! أنا هنا دائماً لمساعدتك.",
        "وداعا": "👋 وداعاً! كان من الممتع التحدث معك. إلى اللقاء! 😊",
        "احسب": "🧮 بكل سرور! يمكنني حل المسائل الحسابية. ما المسألة التي تريد حلها؟",
        "اكتب": "✍️ بكل سرور! يمكنني كتابة قصص وشعر ومقالات. ما الموضوع الذي تريد أن أكتب عنه؟",
        "علمني": "📚 أنا هنا لتعليمك! يمكنني شرح أي موضوع بطريقة سهلة وممتعة. ما الموضوع؟",
        "من أنت": "🤖 أنا Rashed Ai، وكيل ذكي متقدم مدعوم بتقنيات الذكاء الاصطناعي. أنا هنا لمساعدتك في:\n• الإجابة على الأسئلة\n• كتابة المحتوى\n• شرح المواضيع\n• حل المسائل\n• والكثير من الأشياء الأخرى!",
        "ما اسمك": "🤖 اسمي Rashed Ai! أنا منصة ذكية متقدمة تم تطويرها خصيصاً لمساعدتك.",
    }
    
    # البحث عن كلمات مفتاحية
    for key, response in smart_responses.items():
        if key in user_message:
            return response
    
    # رد عام ذكي
    return f"""✨ شكراً على رسالتك!

أنا Rashed Ai، وكيل ذكي متقدم. يمكنني مساعدتك في:

🔹 الإجابة على أسئلتك
🔹 كتابة قصص وشعر ومقالات
🔹 شرح المواضيع المعقدة
🔹 حل المسائل الحسابية
🔹 تقديم النصائح والاستشارات
🔹 والكثير من الأشياء الأخرى!

كيف يمكنني مساعدتك بشكل أفضل؟"""

# معالجة الإرسال
if send_button and user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # إظهار رسالة التحميل
    with st.spinner("⏳ جاري المعالجة..."):
        try:
            # تحضير الرسائل
            messages_for_api = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages
            ]
            
            # توليد رد ذكي
            assistant_message = generate_smart_response(messages_for_api)
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            
            # تفريغ حقل الإدخال
            st.session_state.user_input = ""
            
            st.rerun()
                    
        except Exception as e:
            error_msg = f"❌ حدث خطأ: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.error(error_msg)

# الفوتر
st.markdown("""
<div class="footer-section">
    <p>© 2026 Rashed Ai - جميع الحقوق محفوظة</p>
    <p style='margin-top: 8px;'>منصة ذكية مجانية بدون تكاليف API</p>
</div>
""", unsafe_allow_html=True)
