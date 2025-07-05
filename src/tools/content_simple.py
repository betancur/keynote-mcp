"""
内容管理工具 - 简化版
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number, validate_coordinates, validate_file_path


class ContentTools:
    """内容管理工具类"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """获取所有内容管理工具"""
        return [
            Tool(
                name="add_text_box",
                description="在幻灯片中添加文本框",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "text": {
                            "type": "string",
                            "description": "文本内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）"
                        }
                    },
                    "required": ["slide_number", "text"]
                }
            ),
            Tool(
                name="add_image",
                description="在幻灯片中添加图片",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "image_path": {
                            "type": "string",
                            "description": "图片文件路径"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）"
                        }
                    },
                    "required": ["slide_number", "image_path"]
                }
            )
        ]
    
    async def add_text_box(self, slide_number: int, text: str, x: Optional[float] = None, y: Optional[float] = None) -> List[TextContent]:
        """在幻灯片中添加文本框"""
        try:
            validate_slide_number(slide_number)
            x, y = validate_coordinates(x, y)
            
            if not text or not text.strip():
                return [TextContent(
                    type="text",
                    text="❌ 文本内容不能为空"
                )]
            
            # 转义文本中的特殊字符
            escaped_text = text.replace('"', '\\"').replace('\n', '\\n')
            
            # 如果未指定坐标，使用默认值
            if x == 0.0 and y == 0.0:
                x, y = 100.0, 200.0
            
            script = f'''
            tell application "Keynote"
                tell front document
                    tell slide {slide_number}
                        make new text item with properties {{position:{{{x}, {y}}}, object text:"{escaped_text}"}}
                    end tell
                end tell
            end tell
            '''
            
            result = self.runner.run_inline_script(script)
            
            return [TextContent(
                type="text",
                text=f"✅ 已在幻灯片 {slide_number} 的位置 ({x}, {y}) 添加文本框"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加文本框失败: {str(e)}"
            )]
    
    async def add_image(self, slide_number: int, image_path: str, x: Optional[float] = None, y: Optional[float] = None) -> List[TextContent]:
        """在幻灯片中添加图片"""
        try:
            validate_slide_number(slide_number)
            validate_file_path(image_path)
            x, y = validate_coordinates(x, y)
            
            # 如果未指定坐标，使用默认值
            if x == 0.0 and y == 0.0:
                x, y = 300.0, 200.0
            
            script = f'''
            tell application "Keynote"
                tell front document
                    tell slide {slide_number}
                        make new image with properties {{position:{{{x}, {y}}}, file:"{image_path}"}}
                    end tell
                end tell
            end tell
            '''
            
            result = self.runner.run_inline_script(script)
            
            return [TextContent(
                type="text",
                text=f"✅ 已在幻灯片 {slide_number} 的位置 ({x}, {y}) 添加图片: {image_path}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加图片失败: {str(e)}"
            )]
