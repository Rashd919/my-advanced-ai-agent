"""
محرك الوكيل الذكي الرئيسي
يدمج الذاكرة والتفكير المنطقي والأدوات المتقدمة
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from openai import OpenAI

from .memory import Memory
from .reasoning import ReasoningEngine, ThoughtType
from .tools import ToolBox


class SmartAgent:
    """الوكيل الذكي المتقدم"""

    def __init__(self, agent_name: str = "الوكيل الذكي", 
                 language: str = "ar", debug: bool = False):
        """
        تهيئة الوكيل الذكي
        
        Args:
            agent_name: اسم الوكيل
            language: اللغة (ar, en)
            debug: تفعيل وضع التصحيح
        """
        self.agent_name = agent_name
        self.language = language
        self.debug = debug
        
        # تهيئة مفتاح API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY غير موجود في متغيرات البيئة")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
        
        # تهيئة الأنظمة الفرعية
        self.memory = Memory()
        self.reasoning_engine = ReasoningEngine()
        self.toolbox = ToolBox()
        
        # السجل
        self.conversation_history: List[Dict[str, str]] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # نظام التعليمات
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """بناء تعليمات النظام"""
        tools_list = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.toolbox.list_tools()
        ])
        
        return f"""أنت {self.agent_name}، وكيل ذكي متقدم يتمتع باستقلالية عالية.

اللغة: {'العربية' if self.language == 'ar' else 'الإنجليزية'}

المهام الرئيسية:
1. فهم طلبات المستخدم بشكل عميق
2. تقسيم المهام المعقدة إلى خطوات منطقية
3. استخدام الأدوات المتاحة لتنفيذ المهام
4. التعلم من التجارب السابقة
5. تقديم حلول عملية وفعالة

الأدوات المتاحة:
{tools_list}

التعليمات:
- فكر بشكل منطقي قبل اتخاذ أي إجراء
- اشرح خطواتك بوضوح
- استخدم الأدوات عند الحاجة
- تعلم من الأخطاء والنجاحات
- قدم ملخصاً نهائياً للنتائج

تذكر: أنت وكيل مستقل وذكي، لديك الحرية في اتخاذ القرارات والتصرف بناءً على الحكم والمنطق."""

    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        معالجة طلب المستخدم
        
        Args:
            user_input: طلب المستخدم
            
        Returns:
            النتيجة والمعلومات الإضافية
        """
        # بدء مهمة جديدة
        self.reasoning_engine.start_task(user_input)
        
        # إضافة إلى السجل
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # البحث عن التفاعلات السابقة المشابهة
        similar_interactions = self.memory.search_interactions(user_input, n_results=3)
        
        if similar_interactions:
            self.reasoning_engine.add_thought(
                content=f"وجدت {len(similar_interactions)} تفاعلات سابقة مشابهة",
                thought_type=ThoughtType.ANALYSIS,
                reasoning="البحث في الذاكرة عن تجارب سابقة"
            )
        
        # البحث عن الدروس المستفادة ذات الصلة
        relevant_lessons = self.memory.search_lessons(user_input, n_results=3)
        
        if relevant_lessons:
            self.reasoning_engine.add_thought(
                content=f"وجدت {len(relevant_lessons)} دروس مستفادة ذات صلة",
                thought_type=ThoughtType.ANALYSIS,
                reasoning="استخدام الخبرات السابقة"
            )
        
        # تخطيط الخطوات
        steps = self.reasoning_engine.plan_steps(user_input)
        
        # استدعاء OpenAI
        try:
            response = await self._call_openai(user_input, similar_interactions, relevant_lessons)
            
            # إضافة الرد إلى السجل
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            # حفظ التفاعل في الذاكرة
            self.memory.add_interaction(user_input, response)
            
            # تقييم النتيجة
            self.reasoning_engine.evaluate_result(response, quality=0.8)
            
            return {
                "success": True,
                "response": response,
                "thought_process": self.reasoning_engine.get_thought_process(),
                "summary": self.reasoning_engine.get_summary(),
                "steps": steps,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            error_msg = f"خطأ في معالجة الطلب: {str(e)}"
            self.reasoning_engine.add_thought(
                content=error_msg,
                thought_type=ThoughtType.EVALUATION,
                reasoning="حدث خطأ أثناء المعالجة",
                confidence=0.0
            )
            
            return {
                "success": False,
                "error": error_msg,
                "thought_process": self.reasoning_engine.get_thought_process(),
                "timestamp": datetime.now().isoformat()
            }

    async def _call_openai(self, user_input: str, 
                          similar_interactions: List[Dict],
                          relevant_lessons: List[Dict]) -> str:
        """استدعاء OpenAI API"""
        
        # بناء السياق من الذاكرة
        context = ""
        
        if similar_interactions:
            context += "\n### تفاعلات سابقة مشابهة:\n"
            for interaction in similar_interactions[:2]:
                context += f"- {interaction.get('document', '')[:200]}\n"
        
        if relevant_lessons:
            context += "\n### دروس مستفادة:\n"
            for lesson in relevant_lessons[:2]:
                context += f"- {lesson.get('lesson', '')[:200]}\n"
        
        # بناء الرسالة
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # إضافة السجل
        messages.extend(self.conversation_history[-10:])  # آخر 10 رسائل
        
        if context:
            messages.append({
                "role": "system",
                "content": f"السياق من الذاكرة:{context}"
            })
        
        # استدعاء API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content

    def use_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """استخدام أداة من الأدوات المتاحة"""
        self.reasoning_engine.add_thought(
            content=f"استخدام الأداة: {tool_name}",
            thought_type=ThoughtType.EXECUTION,
            reasoning=f"المعاملات: {kwargs}"
        )
        
        result = self.toolbox.execute_tool(tool_name, **kwargs)
        
        if result.get("success"):
            self.reasoning_engine.add_thought(
                content=f"نجح تنفيذ الأداة {tool_name}",
                thought_type=ThoughtType.EXECUTION,
                reasoning="تم الحصول على النتائج المطلوبة",
                confidence=0.9
            )
        else:
            self.reasoning_engine.add_thought(
                content=f"فشل تنفيذ الأداة {tool_name}",
                thought_type=ThoughtType.EXECUTION,
                reasoning=result.get("error", "خطأ غير معروف"),
                confidence=0.1
            )
        
        return result

    def learn_lesson(self, lesson: str, category: str = "general", 
                    importance: int = 5) -> str:
        """تسجيل درس مستفاد"""
        lesson_id = self.memory.add_lesson(lesson, category, importance)
        
        self.reasoning_engine.learn_from_experience(lesson, importance)
        
        return lesson_id

    def get_memory_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الذاكرة"""
        return self.memory.get_memory_stats()

    def get_session_summary(self) -> Dict[str, Any]:
        """الحصول على ملخص الجلسة"""
        return {
            "session_id": self.session_id,
            "agent_name": self.agent_name,
            "language": self.language,
            "conversation_turns": len(self.conversation_history) // 2,
            "reasoning_summary": self.reasoning_engine.get_summary(),
            "memory_stats": self.get_memory_stats(),
            "timestamp": datetime.now().isoformat()
        }

    def export_session(self, filepath: str) -> None:
        """تصدير الجلسة إلى ملف"""
        try:
            data = {
                "session": self.get_session_summary(),
                "conversation": self.conversation_history,
                "reasoning": self.reasoning_engine.get_thought_process()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            if self.debug:
                print(f"تم تصدير الجلسة إلى {filepath}")
        except Exception as e:
            print(f"خطأ في التصدير: {e}")

    def reset_session(self) -> None:
        """إعادة تعيين الجلسة"""
        self.conversation_history = []
        self.reasoning_engine.reset()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
