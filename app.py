"""
تطبيق Streamlit الرئيسي للوكيل الذكي المتقدم
واجهة تفاعلية وأنيقة بدعم كامل للغة العربية
"""

import streamlit as st
import asyncio
import os
from datetime import datetime
from pathlib import Path

# إضافة مسار المشروع
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import SmartAgent
from core.reasoning import ThoughtType


# إعدادات الصفحة
st.set_page_config(
    page_title="الوكيل الذكي المتقدم",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "وكيل ذكي Python متقدم مع ذاكرة مستمرة وقدرات تنفيذ غير مقيدة"
    }
)

# تحميل CSS مخصص
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    .main {
        padding: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: bold;
    }
    
    .thought-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-right: 4px solid #1f77b4;
    }
    
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-right: 4px solid #28a745;
    }
    
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-right: 4px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)


def initialize_agent():
    """تهيئة الوكيل الذكي"""
    if "agent" not in st.session_state:
        try:
            st.session_state.agent = SmartAgent(
                agent_name="الوكيل الذكي المتقدم",
                language="ar",
                debug=True
            )
            st.session_state.conversation = []
        except ValueError as e:
            st.error(f"❌ خطأ: {str(e)}")
            st.info("تأكد من تعيين OPENAI_API_KEY في ملف .env")
            return False
    return True


def display_thought_process(thoughts: list):
    """عرض مسار التفكير"""
    st.subheader("🧠 مسار التفكير")
    
    for i, thought in enumerate(thoughts, 1):
        thought_type = thought.get("type", "unknown")
        content = thought.get("content", "")
        reasoning = thought.get("reasoning", "")
        confidence = thought.get("confidence", 0.5)
        
        # اختيار الأيقونة بناءً على نوع الفكرة
        icons = {
            "تحليل": "🔍",
            "تخطيط": "📋",
            "تنفيذ": "⚙️",
            "تقييم": "✅",
            "تعلم": "📚"
        }
        
        icon = icons.get(thought_type, "💭")
        
        with st.expander(f"{icon} {thought_type} - {content[:50]}..."):
            st.write(f"**المحتوى:** {content}")
            st.write(f"**التبرير:** {reasoning}")
            st.progress(confidence, text=f"درجة الثقة: {confidence*100:.0f}%")


def display_memory_stats():
    """عرض إحصائيات الذاكرة"""
    if "agent" not in st.session_state:
        return
    
    stats = st.session_state.agent.get_memory_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 إجمالي التفاعلات",
            stats.get("total_interactions", 0)
        )
    
    with col2:
        st.metric(
            "📚 الدروس المستفادة",
            stats.get("total_lessons", 0)
        )
    
    with col3:
        categories = stats.get("categories", [])
        st.metric(
            "🏷️ الفئات",
            len(categories)
        )
    
    with col4:
        size_kb = stats.get("memory_file_size", 0) / 1024
        st.metric(
            "💾 حجم الذاكرة",
            f"{size_kb:.1f} KB"
        )


def main():
    """الدالة الرئيسية"""
    
    # العنوان
    st.title("🤖 الوكيل الذكي المتقدم")
    st.markdown("وكيل ذكي Python مستقل مع ذاكرة مستمرة وقدرات تنفيذ غير مقيدة")
    
    # تهيئة الوكيل
    if not initialize_agent():
        st.stop()
    
    # الشريط الجانبي
    with st.sidebar:
        st.header("⚙️ الإعدادات")
        
        # معلومات الجلسة
        st.subheader("📋 معلومات الجلسة")
        session_summary = st.session_state.agent.get_session_summary()
        st.write(f"**معرف الجلسة:** {session_summary['session_id']}")
        st.write(f"**عدد الأدوار:** {session_summary['conversation_turns']}")
        
        # إحصائيات الذاكرة
        st.subheader("📊 إحصائيات الذاكرة")
        display_memory_stats()
        
        # الأدوات المتاحة
        st.subheader("🛠️ الأدوات المتاحة")
        tools = st.session_state.agent.toolbox.list_tools()
        for tool in tools:
            st.write(f"✓ {tool['name']}")
        
        # الإجراءات
        st.subheader("🎯 الإجراءات")
        
        if st.button("🔄 إعادة تعيين الجلسة"):
            st.session_state.agent.reset_session()
            st.session_state.conversation = []
            st.success("تم إعادة تعيين الجلسة")
            st.rerun()
        
        if st.button("💾 تصدير الجلسة"):
            export_path = f"session_{session_summary['session_id']}.json"
            st.session_state.agent.export_session(export_path)
            st.success(f"تم تصدير الجلسة إلى {export_path}")
    
    # الأقسام الرئيسية
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 المحادثة",
        "🧠 التفكير المنطقي",
        "🛠️ الأدوات",
        "📚 الذاكرة"
    ])
    
    # قسم المحادثة
    with tab1:
        st.subheader("💬 محادثة مع الوكيل الذكي")
        
        # عرض السجل
        if st.session_state.conversation:
            for message in st.session_state.conversation:
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant"):
                        st.write(message["content"])
        else:
            st.info("ابدأ محادثة جديدة بكتابة رسالتك أدناه")
        
        # إدخال المستخدم
        st.divider()
        user_input = st.text_area(
            "اكتب طلبك هنا:",
            placeholder="مثال: اكتب برنامج يحسب مجموع الأرقام من 1 إلى 100",
            height=100
        )
        
        if st.button("📤 إرسال", key="send_button"):
            if user_input.strip():
                with st.spinner("🔄 جاري معالجة طلبك..."):
                    try:
                        # معالجة الطلب
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        result = loop.run_until_complete(
                            st.session_state.agent.process_request(user_input)
                        )
                        
                        # إضافة إلى السجل
                        st.session_state.conversation.append({
                            "role": "user",
                            "content": user_input
                        })
                        
                        if result["success"]:
                            st.session_state.conversation.append({
                                "role": "assistant",
                                "content": result["response"]
                            })
                            
                            with st.chat_message("assistant"):
                                st.write(result["response"])
                            
                            st.success("✅ تم معالجة الطلب بنجاح")
                        else:
                            st.error(f"❌ خطأ: {result.get('error', 'خطأ غير معروف')}")
                    
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
    
    # قسم التفكير المنطقي
    with tab2:
        st.subheader("🧠 مسار التفكير المنطقي")
        
        if hasattr(st.session_state.agent.reasoning_engine, 'thoughts') and \
           st.session_state.agent.reasoning_engine.thoughts:
            
            thoughts = st.session_state.agent.reasoning_engine.get_thought_process()
            display_thought_process(thoughts)
            
            # ملخص التفكير
            st.divider()
            st.subheader("📊 ملخص التفكير")
            summary = st.session_state.agent.reasoning_engine.get_summary()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("عدد الأفكار", summary.get("total_thoughts", 0))
            
            with col2:
                st.metric("متوسط الثقة", f"{summary.get('average_confidence', 0)*100:.0f}%")
            
            with col3:
                st.metric("عدد الخطوات", len(summary.get("task_steps", [])))
            
            # الخطوات
            if summary.get("task_steps"):
                st.write("**الخطوات المخطط لها:**")
                for step in summary["task_steps"]:
                    st.write(f"- {step}")
        else:
            st.info("لا توجد أفكار مسجلة حتى الآن. ابدأ محادثة لرؤية مسار التفكير.")
    
    # قسم الأدوات
    with tab3:
        st.subheader("🛠️ الأدوات المتقدمة")
        
        tool_name = st.selectbox(
            "اختر أداة:",
            [tool["name"] for tool in st.session_state.agent.toolbox.list_tools()]
        )
        
        # تنفيذ الأداة
        if tool_name == "Python Code Executor":
            st.write("**تنفيذ كود Python**")
            code = st.text_area("اكتب الكود:", height=200)
            
            if st.button("▶️ تنفيذ الكود"):
                result = st.session_state.agent.use_tool(
                    "Python Code Executor",
                    code=code
                )
                
                if result.get("success"):
                    st.success("✅ تم التنفيذ بنجاح")
                    st.write("**الإخراج:**")
                    st.code(result.get("output", ""))
                else:
                    st.error(f"❌ خطأ: {result.get('error', '')}")
                    if result.get("error"):
                        st.code(result.get("error"))
        
        elif tool_name == "Web Scraper":
            st.write("**تصفح الويب**")
            url = st.text_input("أدخل رابط الموقع:")
            
            if st.button("🌐 تصفح الموقع"):
                result = st.session_state.agent.use_tool(
                    "Web Scraper",
                    url=url
                )
                
                if result.get("success"):
                    st.success("✅ تم التصفح بنجاح")
                    st.write(f"**العنوان:** {result.get('title', 'بدون عنوان')}")
                    st.write(f"**الحالة:** {result.get('status_code', 'N/A')}")
                    st.write("**المحتوى:**")
                    st.write(result.get("text", "")[:500])
                else:
                    st.error(f"❌ خطأ: {result.get('error', '')}")
        
        elif tool_name == "Data Analyzer":
            st.write("**تحليل البيانات**")
            filepath = st.text_input("مسار الملف (CSV, Excel):")
            
            if st.button("📊 تحليل البيانات"):
                result = st.session_state.agent.use_tool(
                    "Data Analyzer",
                    filepath=filepath
                )
                
                if result.get("success"):
                    st.success("✅ تم التحليل بنجاح")
                    analysis = result.get("analysis", {})
                    st.write(f"**الحجم:** {analysis.get('shape', 'N/A')}")
                    st.write(f"**الأعمدة:** {', '.join(analysis.get('columns', []))}")
                else:
                    st.error(f"❌ خطأ: {result.get('error', '')}")
    
    # قسم الذاكرة
    with tab4:
        st.subheader("📚 نظام الذاكرة")
        
        memory_tab1, memory_tab2 = st.tabs(["التفاعلات", "الدروس"])
        
        with memory_tab1:
            st.write("**التفاعلات الأخيرة:**")
            recent = st.session_state.agent.memory.get_recent_interactions(n=5)
            
            if recent:
                for interaction in recent:
                    with st.expander(f"🕐 {interaction.get('timestamp', '')[:10]}"):
                        st.write(f"**المدخل:** {interaction.get('user_input', '')[:200]}")
                        st.write(f"**الرد:** {interaction.get('agent_response', '')[:200]}")
            else:
                st.info("لا توجد تفاعلات مسجلة")
        
        with memory_tab2:
            st.write("**الدروس المستفادة:**")
            lessons = st.session_state.agent.memory.memory_data.get("lessons", [])
            
            if lessons:
                for lesson in lessons:
                    with st.expander(f"📚 {lesson.get('category', 'عام')} - أهمية: {lesson.get('importance', 0)}/10"):
                        st.write(lesson.get("lesson", ""))
            else:
                st.info("لا توجد دروس مسجلة")
            
            # إضافة درس جديد
            st.divider()
            st.write("**إضافة درس مستفاد:**")
            
            new_lesson = st.text_area("الدرس:")
            new_category = st.text_input("الفئة:", value="عام")
            new_importance = st.slider("الأهمية:", 1, 10, 5)
            
            if st.button("💾 حفظ الدرس"):
                if new_lesson.strip():
                    lesson_id = st.session_state.agent.learn_lesson(
                        new_lesson,
                        new_category,
                        new_importance
                    )
                    st.success(f"✅ تم حفظ الدرس (ID: {lesson_id})")
                    st.rerun()
                else:
                    st.warning("⚠️ الرجاء إدخال الدرس")


if __name__ == "__main__":
    main()
