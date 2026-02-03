"""
محرك التفكير المنطقي (Reasoning Engine)
يقسم المهام المعقدة إلى خطوات منطقية ويتتبع مسار التفكير
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class ThoughtType(Enum):
    """أنواع الأفكار"""
    ANALYSIS = "تحليل"
    PLANNING = "تخطيط"
    EXECUTION = "تنفيذ"
    EVALUATION = "تقييم"
    LEARNING = "تعلم"


class Thought:
    """تمثيل فكرة واحدة في مسار التفكير"""

    def __init__(self, content: str, thought_type: ThoughtType, 
                 reasoning: str = "", confidence: float = 0.5):
        """
        Args:
            content: محتوى الفكرة
            thought_type: نوع الفكرة
            reasoning: التبرير المنطقي
            confidence: درجة الثقة (0-1)
        """
        self.content = content
        self.thought_type = thought_type
        self.reasoning = reasoning
        self.confidence = confidence
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """تحويل الفكرة إلى قاموس"""
        return {
            "content": self.content,
            "type": self.thought_type.value,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "timestamp": self.timestamp
        }


class ReasoningEngine:
    """محرك التفكير المنطقي"""

    def __init__(self):
        """تهيئة محرك التفكير"""
        self.thoughts: List[Thought] = []
        self.current_task: Optional[str] = None
        self.task_steps: List[str] = []

    def start_task(self, task: str) -> None:
        """
        بدء مهمة جديدة
        
        Args:
            task: وصف المهمة
        """
        self.current_task = task
        self.thoughts = []
        self.task_steps = []
        
        # إضافة فكرة البداية
        self.add_thought(
            content=f"بدء المهمة: {task}",
            thought_type=ThoughtType.ANALYSIS,
            reasoning="تحليل المهمة المطلوبة وتحديد الخطوات الأولية"
        )

    def add_thought(self, content: str, thought_type: ThoughtType,
                   reasoning: str = "", confidence: float = 0.5) -> Thought:
        """
        إضافة فكرة إلى مسار التفكير
        
        Args:
            content: محتوى الفكرة
            thought_type: نوع الفكرة
            reasoning: التبرير المنطقي
            confidence: درجة الثقة
            
        Returns:
            الفكرة المضافة
        """
        thought = Thought(content, thought_type, reasoning, confidence)
        self.thoughts.append(thought)
        return thought

    def plan_steps(self, task: str, num_steps: int = 5) -> List[str]:
        """
        تخطيط خطوات حل المهمة
        
        Args:
            task: وصف المهمة
            num_steps: العدد المقترح للخطوات
            
        Returns:
            قائمة الخطوات
        """
        self.add_thought(
            content=f"تخطيط {num_steps} خطوات لحل المهمة",
            thought_type=ThoughtType.PLANNING,
            reasoning="تقسيم المهمة المعقدة إلى خطوات بسيطة"
        )
        
        # هنا يمكن استخدام LLM لتوليد الخطوات
        # للآن نستخدم خطوات عامة
        steps = [
            "1. فهم المهمة بشكل كامل",
            "2. جمع المعلومات اللازمة",
            "3. تحليل البيانات والمعلومات",
            "4. تطوير الحل",
            "5. التحقق والتقييم"
        ]
        
        self.task_steps = steps
        return steps

    def execute_step(self, step_number: int, result: str, 
                    success: bool = True) -> None:
        """
        تسجيل تنفيذ خطوة
        
        Args:
            step_number: رقم الخطوة
            result: نتيجة الخطوة
            success: هل نجحت الخطوة
        """
        self.add_thought(
            content=f"تنفيذ الخطوة {step_number}: {result}",
            thought_type=ThoughtType.EXECUTION,
            reasoning=f"النتيجة: {'نجاح' if success else 'فشل'}",
            confidence=0.9 if success else 0.3
        )

    def evaluate_result(self, result: str, quality: float = 0.5) -> None:
        """
        تقييم النتيجة
        
        Args:
            result: وصف النتيجة
            quality: جودة النتيجة (0-1)
        """
        self.add_thought(
            content=f"تقييم النتيجة: {result}",
            thought_type=ThoughtType.EVALUATION,
            reasoning=f"جودة النتيجة: {quality * 100:.0f}%",
            confidence=quality
        )

    def learn_from_experience(self, lesson: str, importance: int = 5) -> None:
        """
        التعلم من التجربة
        
        Args:
            lesson: الدرس المستفاد
            importance: مستوى الأهمية (1-10)
        """
        self.add_thought(
            content=f"درس مستفاد: {lesson}",
            thought_type=ThoughtType.LEARNING,
            reasoning=f"أهمية الدرس: {importance}/10"
        )

    def get_thought_process(self) -> List[Dict[str, Any]]:
        """الحصول على مسار التفكير كاملاً"""
        return [thought.to_dict() for thought in self.thoughts]

    def get_summary(self) -> Dict[str, Any]:
        """الحصول على ملخص مسار التفكير"""
        if not self.thoughts:
            return {"summary": "لا توجد أفكار مسجلة"}
        
        thought_types = {}
        for thought in self.thoughts:
            type_name = thought.thought_type.value
            thought_types[type_name] = thought_types.get(type_name, 0) + 1
        
        avg_confidence = sum(t.confidence for t in self.thoughts) / len(self.thoughts)
        
        return {
            "current_task": self.current_task,
            "total_thoughts": len(self.thoughts),
            "thought_types": thought_types,
            "average_confidence": avg_confidence,
            "task_steps": self.task_steps,
            "first_thought": self.thoughts[0].to_dict() if self.thoughts else None,
            "last_thought": self.thoughts[-1].to_dict() if self.thoughts else None
        }

    def export_reasoning(self, filepath: str) -> None:
        """تصدير مسار التفكير إلى ملف"""
        import json
        try:
            data = {
                "task": self.current_task,
                "steps": self.task_steps,
                "thoughts": self.get_thought_process(),
                "summary": self.get_summary()
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في التصدير: {e}")

    def reset(self) -> None:
        """إعادة تعيين محرك التفكير"""
        self.thoughts = []
        self.current_task = None
        self.task_steps = []


class ReasoningChain:
    """سلسلة من خطوات التفكير المترابطة"""

    def __init__(self):
        """تهيئة سلسلة التفكير"""
        self.engines: Dict[str, ReasoningEngine] = {}
        self.execution_order: List[str] = []

    def add_engine(self, name: str, engine: ReasoningEngine) -> None:
        """إضافة محرك تفكير إلى السلسلة"""
        self.engines[name] = engine
        self.execution_order.append(name)

    def execute_chain(self) -> Dict[str, Any]:
        """تنفيذ سلسلة التفكير"""
        results = {}
        for engine_name in self.execution_order:
            engine = self.engines[engine_name]
            results[engine_name] = engine.get_summary()
        return results

    def get_chain_summary(self) -> Dict[str, Any]:
        """الحصول على ملخص السلسلة"""
        return {
            "total_engines": len(self.engines),
            "execution_order": self.execution_order,
            "engines_summary": {
                name: engine.get_summary()
                for name, engine in self.engines.items()
            }
        }
