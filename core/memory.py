"""
نظام الذاكرة المستمرة للوكيل الذكي
يستخدم ChromaDB لتخزين التفاعلات والدروس المستفادة
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import chromadb



class Memory:
    """نظام الذاكرة المستمرة"""

    def __init__(self, db_path: str = "./data/chroma_db"):
        """
        تهيئة نظام الذاكرة
        
        Args:
            db_path: مسار قاعدة بيانات ChromaDB
        """
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        
        # إعداد ChromaDB
        self.client = chromadb.EphemeralClient()
        
        # إنشاء مجموعات الذاكرة
        self.interactions_collection = self.client.get_or_create_collection(
            name="interactions",
            metadata={"description": "سجل التفاعلات والمحادثات"}
        )
        
        self.lessons_collection = self.client.get_or_create_collection(
            name="lessons",
            metadata={"description": "الدروس المستفادة والخبرات"}
        )
        
        self.memory_file = os.path.join(db_path, "memory.json")
        self._load_memory()

    def _load_memory(self):
        """تحميل الذاكرة من الملف"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory_data = json.load(f)
            except Exception as e:
                print(f"خطأ في تحميل الذاكرة: {e}")
                self.memory_data = {"interactions": [], "lessons": []}
        else:
            self.memory_data = {"interactions": [], "lessons": []}

    def _save_memory(self):
        """حفظ الذاكرة إلى الملف"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ الذاكرة: {e}")

    def add_interaction(self, user_input: str, agent_response: str, 
                       metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        إضافة تفاعل جديد إلى الذاكرة
        
        Args:
            user_input: مدخل المستخدم
            agent_response: رد الوكيل
            metadata: معلومات إضافية
            
        Returns:
            معرف التفاعل
        """
        interaction_id = f"interaction_{len(self.memory_data['interactions']) + 1}"
        timestamp = datetime.now().isoformat()
        
        interaction = {
            "id": interaction_id,
            "timestamp": timestamp,
            "user_input": user_input,
            "agent_response": agent_response,
            "metadata": metadata or {}
        }
        
        self.memory_data["interactions"].append(interaction)
        
        # إضافة إلى ChromaDB
        self.interactions_collection.add(
            ids=[interaction_id],
            documents=[f"{user_input} {agent_response}"],
            metadatas=[{
                "timestamp": timestamp,
                "user_input": user_input[:500],  # تقليص الطول
                "type": "interaction"
            }]
        )
        
        self._save_memory()
        return interaction_id

    def add_lesson(self, lesson: str, category: str, 
                   importance: int = 5) -> str:
        """
        إضافة درس مستفاد إلى الذاكرة
        
        Args:
            lesson: نص الدرس
            category: فئة الدرس
            importance: مستوى الأهمية (1-10)
            
        Returns:
            معرف الدرس
        """
        lesson_id = f"lesson_{len(self.memory_data['lessons']) + 1}"
        timestamp = datetime.now().isoformat()
        
        lesson_entry = {
            "id": lesson_id,
            "timestamp": timestamp,
            "lesson": lesson,
            "category": category,
            "importance": importance
        }
        
        self.memory_data["lessons"].append(lesson_entry)
        
        # إضافة إلى ChromaDB
        self.lessons_collection.add(
            ids=[lesson_id],
            documents=[lesson],
            metadatas=[{
                "timestamp": timestamp,
                "category": category,
                "importance": importance,
                "type": "lesson"
            }]
        )
        
        self._save_memory()
        return lesson_id

    def search_interactions(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        البحث عن التفاعلات السابقة
        
        Args:
            query: نص البحث
            n_results: عدد النتائج المطلوبة
            
        Returns:
            قائمة التفاعلات المطابقة
        """
        try:
            results = self.interactions_collection.query(
                query_texts=[query],
                n_results=min(n_results, 10)
            )
            
            interactions = []
            for i, doc in enumerate(results['documents'][0]):
                interactions.append({
                    "id": results['ids'][0][i],
                    "document": doc,
                    "metadata": results['metadatas'][0][i]
                })
            
            return interactions
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return []

    def search_lessons(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        البحث عن الدروس المستفادة
        
        Args:
            query: نص البحث
            n_results: عدد النتائج المطلوبة
            
        Returns:
            قائمة الدروس المطابقة
        """
        try:
            results = self.lessons_collection.query(
                query_texts=[query],
                n_results=min(n_results, 10)
            )
            
            lessons = []
            for i, doc in enumerate(results['documents'][0]):
                lessons.append({
                    "id": results['ids'][0][i],
                    "lesson": doc,
                    "metadata": results['metadatas'][0][i]
                })
            
            return lessons
        except Exception as e:
            print(f"خطأ في البحث: {e}")
            return []

    def get_recent_interactions(self, n: int = 10) -> List[Dict]:
        """الحصول على آخر التفاعلات"""
        return self.memory_data["interactions"][-n:]

    def get_important_lessons(self, min_importance: int = 7) -> List[Dict]:
        """الحصول على الدروس المهمة"""
        return [
            lesson for lesson in self.memory_data["lessons"]
            if lesson.get("importance", 0) >= min_importance
        ]

    def get_lessons_by_category(self, category: str) -> List[Dict]:
        """الحصول على الدروس حسب الفئة"""
        return [
            lesson for lesson in self.memory_data["lessons"]
            if lesson.get("category") == category
        ]

    def get_memory_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الذاكرة"""
        return {
            "total_interactions": len(self.memory_data["interactions"]),
            "total_lessons": len(self.memory_data["lessons"]),
            "categories": list(set(
                lesson.get("category", "unknown") 
                for lesson in self.memory_data["lessons"]
            )),
            "memory_file_size": os.path.getsize(self.memory_file) if os.path.exists(self.memory_file) else 0
        }

    def clear_old_interactions(self, days: int = 30):
        """مسح التفاعلات القديمة"""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        
        self.memory_data["interactions"] = [
            interaction for interaction in self.memory_data["interactions"]
            if datetime.fromisoformat(interaction["timestamp"]) > cutoff_date
        ]
        
        self._save_memory()

    def export_memory(self, filepath: str):
        """تصدير الذاكرة إلى ملف"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, ensure_ascii=False, indent=2)
            print(f"تم تصدير الذاكرة إلى {filepath}")
        except Exception as e:
            print(f"خطأ في التصدير: {e}")

    def import_memory(self, filepath: str):
        """استيراد الذاكرة من ملف"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.memory_data = json.load(f)
            self._save_memory()
            print(f"تم استيراد الذاكرة من {filepath}")
        except Exception as e:
            print(f"خطأ في الاستيراد: {e}")
