"""
نظام الأدوات المتقدمة للوكيل الذكي
يتضمن أدوات لتصفح الويب وتنفيذ الكود وتحليل البيانات
"""

import subprocess
import sys
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod


class Tool(ABC):
    """فئة أساسية للأدوات"""

    def __init__(self, name: str, description: str):
        """
        Args:
            name: اسم الأداة
            description: وصف الأداة
        """
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """تنفيذ الأداة"""
        pass


class PythonCodeExecutor(Tool):
    """أداة لتنفيذ كود Python"""

    def __init__(self):
        super().__init__(
            name="Python Code Executor",
            description="تنفيذ كود Python مباشرة"
        )

    def execute(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        تنفيذ كود Python
        
        Args:
            code: الكود المراد تنفيذه
            timeout: المدة القصوى للتنفيذ بالثواني
            
        Returns:
            نتائج التنفيذ
        """
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"انتهت مهلة التنفيذ ({timeout}s)",
                "return_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "return_code": -1
            }

    def safe_execute(self, code: str) -> Dict[str, Any]:
        """تنفيذ آمن للكود مع قيود"""
        # قائمة الكلمات المحظورة
        forbidden_keywords = [
            "exec", "eval", "compile", "__import__",
            "open", "input", "raw_input", "file"
        ]
        
        # التحقق من الكلمات المحظورة
        for keyword in forbidden_keywords:
            if keyword in code:
                return {
                    "success": False,
                    "output": "",
                    "error": f"الكلمة المحظورة '{keyword}' موجودة في الكود",
                    "return_code": -1
                }
        
        return self.execute(code)


class WebScraper(Tool):
    """أداة لتصفح الويب"""

    def __init__(self):
        super().__init__(
            name="Web Scraper",
            description="تصفح وجمع البيانات من المواقع"
        )

    def execute(self, url: str, **kwargs) -> Dict[str, Any]:
        """
        تصفح موقع ويب
        
        Args:
            url: رابط الموقع
            
        Returns:
            محتوى الموقع
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # استخراج المعلومات الأساسية
            title = soup.title.string if soup.title else "بدون عنوان"
            text = soup.get_text(strip=True)[:1000]  # أول 1000 حرف
            links = [a.get('href') for a in soup.find_all('a', href=True)][:10]
            
            return {
                "success": True,
                "url": url,
                "title": title,
                "text": text,
                "links": links,
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e),
                "status_code": None
            }

    def search_and_summarize(self, query: str, num_results: int = 3) -> Dict[str, Any]:
        """البحث عن موضوع وتلخيص النتائج"""
        try:
            import requests
            
            # محاكاة البحث (في التطبيق الحقيقي يمكن استخدام Google Search API)
            search_url = f"https://www.google.com/search?q={query}"
            
            return {
                "success": True,
                "query": query,
                "results": [
                    {
                        "title": "نتيجة 1",
                        "url": "https://example.com/1",
                        "snippet": "ملخص النتيجة الأولى"
                    }
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e)
            }


class DataAnalyzer(Tool):
    """أداة لتحليل البيانات"""

    def __init__(self):
        super().__init__(
            name="Data Analyzer",
            description="تحليل البيانات والملفات"
        )

    def execute(self, filepath: str, **kwargs) -> Dict[str, Any]:
        """
        تحليل ملف بيانات
        
        Args:
            filepath: مسار الملف
            
        Returns:
            نتائج التحليل
        """
        try:
            import pandas as pd
            
            # قراءة الملف
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filepath)
            else:
                return {
                    "success": False,
                    "error": "صيغة الملف غير مدعومة"
                }
            
            # تحليل البيانات
            analysis = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "statistics": df.describe().to_dict()
            }
            
            return {
                "success": True,
                "filepath": filepath,
                "analysis": analysis,
                "preview": df.head(5).to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "filepath": filepath,
                "error": str(e)
            }


class FileManager(Tool):
    """أداة لإدارة الملفات"""

    def __init__(self):
        super().__init__(
            name="File Manager",
            description="إدارة وقراءة الملفات"
        )

    def execute(self, action: str, filepath: str, **kwargs) -> Dict[str, Any]:
        """
        تنفيذ عملية على ملف
        
        Args:
            action: العملية (read, write, list, delete)
            filepath: مسار الملف
            
        Returns:
            نتائج العملية
        """
        import os
        
        try:
            if action == "read":
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "success": True,
                    "action": action,
                    "filepath": filepath,
                    "content": content[:5000]  # أول 5000 حرف
                }
            
            elif action == "write":
                content = kwargs.get("content", "")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {
                    "success": True,
                    "action": action,
                    "filepath": filepath,
                    "message": "تم كتابة الملف بنجاح"
                }
            
            elif action == "list":
                directory = filepath
                files = os.listdir(directory)
                return {
                    "success": True,
                    "action": action,
                    "directory": directory,
                    "files": files[:20]  # أول 20 ملف
                }
            
            elif action == "delete":
                os.remove(filepath)
                return {
                    "success": True,
                    "action": action,
                    "filepath": filepath,
                    "message": "تم حذف الملف بنجاح"
                }
            
            else:
                return {
                    "success": False,
                    "error": f"العملية '{action}' غير معروفة"
                }
        except Exception as e:
            return {
                "success": False,
                "action": action,
                "filepath": filepath,
                "error": str(e)
            }


class ToolBox:
    """صندوق الأدوات - يدير جميع الأدوات المتاحة"""

    def __init__(self):
        """تهيئة صندوق الأدوات"""
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """تسجيل الأدوات الافتراضية"""
        self.register_tool(PythonCodeExecutor())
        self.register_tool(WebScraper())
        self.register_tool(DataAnalyzer())
        self.register_tool(FileManager())

    def register_tool(self, tool: Tool) -> None:
        """تسجيل أداة جديدة"""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[Tool]:
        """الحصول على أداة"""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict[str, str]]:
        """قائمة الأدوات المتاحة"""
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """تنفيذ أداة"""
        tool = self.get_tool(tool_name)
        if not tool:
            return {
                "success": False,
                "error": f"الأداة '{tool_name}' غير موجودة"
            }
        
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
