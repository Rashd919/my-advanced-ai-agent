#!/usr/bin/env python3
"""
اختبار سريع للوكيل الذكي
"""

import asyncio
import os
from pathlib import Path

# إضافة مسار المشروع
import sys
sys.path.insert(0, str(Path(__file__).parent))

from core.agent import SmartAgent
from core.memory import Memory
from core.reasoning import ReasoningEngine, ThoughtType
from core.tools import ToolBox


def test_memory():
    """اختبار نظام الذاكرة"""
    print("\n🧪 اختبار نظام الذاكرة...")
    
    memory = Memory()
    
    # إضافة تفاعل
    interaction_id = memory.add_interaction(
        "مرحبا",
        "مرحبا بك في الوكيل الذكي"
    )
    print(f"✅ تم إضافة تفاعل: {interaction_id}")
    
    # إضافة درس
    lesson_id = memory.add_lesson(
        "التعامل مع المستخدمين بلطف مهم",
        "سلوك",
        importance=8
    )
    print(f"✅ تم إضافة درس: {lesson_id}")
    
    # البحث
    results = memory.search_interactions("مرحبا")
    print(f"✅ نتائج البحث: {len(results)} نتيجة")
    
    # الإحصائيات
    stats = memory.get_memory_stats()
    print(f"✅ إحصائيات الذاكرة: {stats}")


def test_reasoning():
    """اختبار محرك التفكير"""
    print("\n🧪 اختبار محرك التفكير المنطقي...")
    
    engine = ReasoningEngine()
    
    # بدء مهمة
    engine.start_task("حل مسألة رياضية")
    print("✅ تم بدء المهمة")
    
    # تخطيط الخطوات
    steps = engine.plan_steps("حل مسألة رياضية", num_steps=3)
    print(f"✅ تم تخطيط {len(steps)} خطوات")
    
    # تنفيذ خطوة
    engine.execute_step(1, "فهم المسألة", success=True)
    print("✅ تم تنفيذ الخطوة الأولى")
    
    # التقييم
    engine.evaluate_result("النتيجة صحيحة", quality=0.95)
    print("✅ تم تقييم النتيجة")
    
    # الملخص
    summary = engine.get_summary()
    print(f"✅ ملخص التفكير: {summary['total_thoughts']} أفكار")


def test_tools():
    """اختبار الأدوات"""
    print("\n🧪 اختبار الأدوات...")
    
    toolbox = ToolBox()
    
    # قائمة الأدوات
    tools = toolbox.list_tools()
    print(f"✅ عدد الأدوات: {len(tools)}")
    
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    # اختبار مفسر الكود
    print("\n  اختبار مفسر الكود Python:")
    result = toolbox.execute_tool(
        "Python Code Executor",
        code="print('مرحبا بك في الوكيل الذكي')"
    )
    
    if result.get("success"):
        print(f"  ✅ النتيجة: {result.get('output').strip()}")
    else:
        print(f"  ❌ خطأ: {result.get('error')}")


async def test_agent():
    """اختبار الوكيل الذكي"""
    print("\n🧪 اختبار الوكيل الذكي...")
    
    try:
        agent = SmartAgent(
            agent_name="وكيل الاختبار",
            language="ar",
            debug=True
        )
        print("✅ تم تهيئة الوكيل")
        
        # اختبار طلب بسيط
        print("\n  معالجة طلب بسيط...")
        result = await agent.process_request("مرحبا، من أنت؟")
        
        if result.get("success"):
            print(f"✅ الرد: {result.get('response')[:100]}...")
            print(f"✅ عدد الأفكار: {len(result.get('thought_process', []))}")
        else:
            print(f"❌ خطأ: {result.get('error')}")
        
        # الملخص
        session_summary = agent.get_session_summary()
        print(f"\n✅ ملخص الجلسة:")
        print(f"  - معرف الجلسة: {session_summary['session_id']}")
        print(f"  - عدد الأدوار: {session_summary['conversation_turns']}")
        
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")


def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🤖 اختبار الوكيل الذكي المتقدم")
    print("=" * 60)
    
    # اختبار الذاكرة
    test_memory()
    
    # اختبار التفكير
    test_reasoning()
    
    # اختبار الأدوات
    test_tools()
    
    # اختبار الوكيل
    asyncio.run(test_agent())
    
    print("\n" + "=" * 60)
    print("✅ انتهت الاختبارات بنجاح!")
    print("=" * 60)


if __name__ == "__main__":
    main()
