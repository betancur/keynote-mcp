"""
Slide navigation and selection operations
"""

from typing import List
from mcp.types import TextContent
from ...utils import AppleScriptRunner, validate_slide_number


class SlideNavigationOperations:
    """Slide navigation and selection operations"""
    
    def __init__(self, runner: AppleScriptRunner):
        self.runner = runner
    
    async def get_slide_count(self, doc_name: str = "") -> List[TextContent]:
        """Get slide count"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    return count of slides of targetDoc
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"📊 幻灯片数量: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取幻灯片数量失败: {str(e)}"
            )]
    
    async def select_slide(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        """Select specified slide"""
        try:
            validate_slide_number(slide_number)
            
            self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set current slide of targetDoc to slide {slide_number} of targetDoc
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功选择幻灯片 {slide_number}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 选择幻灯片失败: {str(e)}"
            )]
    
    async def get_slide_info(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        """Get slide information"""
        try:
            validate_slide_number(slide_number)
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set targetSlide to slide {slide_number} of targetDoc
                    set slideInfo to {{}}
                    
                    set end of slideInfo to slide number of targetSlide
                    
                    try
                        set end of slideInfo to name of master slide of targetSlide
                    on error
                        set end of slideInfo to "Unknown Layout"
                    end try
                    
                    try
                        set end of slideInfo to count of text items of targetSlide
                    on error
                        set end of slideInfo to 0
                    end try
                    
                    return slideInfo as string
                end tell
            ''')
            
            info_parts = result.replace("{", "").replace("}", "").split(", ")
            if len(info_parts) >= 3:
                number, layout, text_count = info_parts[0], info_parts[1], info_parts[2]
                return [TextContent(
                    type="text",
                    text=f"📊 幻灯片 {slide_number} 信息:\n• 编号: {number}\n• 布局: {layout}\n• 文本框数量: {text_count}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"📊 幻灯片 {slide_number} 信息: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取幻灯片信息失败: {str(e)}"
            )]
