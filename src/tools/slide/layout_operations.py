"""
Slide layout operations
"""

from typing import List
from mcp.types import TextContent
from ...utils import AppleScriptRunner, validate_slide_number


class SlideLayoutOperations:
    """Slide layout operations"""
    
    def __init__(self, runner: AppleScriptRunner):
        self.runner = runner
    
    async def set_slide_layout(self, slide_number: int, layout: str, doc_name: str = "") -> List[TextContent]:
        """Set slide layout"""
        try:
            validate_slide_number(slide_number)
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    try
                        -- 找到目标布局
                        set targetLayout to missing value
                        repeat with masterSlide in master slides of targetDoc
                            if name of masterSlide is "{layout}" then
                                set targetLayout to masterSlide
                                exit repeat
                            end if
                        end repeat
                        
                        if targetLayout is missing value then
                            return "layout_not_found"
                        end if
                        
                        -- 设置幻灯片布局（使用正确的语法：base slide）
                        set base slide of slide {slide_number} of targetDoc to targetLayout
                        return "success"
                    on error errMsg
                        return "error: " & errMsg
                    end try
                end tell
            ''')
            
            if result == "success":
                return [TextContent(
                    type="text",
                    text=f"✅ 成功设置幻灯片 {slide_number} 的布局为: {layout}"
                )]
            elif result == "layout_not_found":
                return [TextContent(
                    type="text",
                    text=f"❌ 布局不存在: {layout}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ 设置布局失败: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 设置幻灯片布局失败: {str(e)}"
            )]
    
    async def get_available_layouts(self, doc_name: str = "") -> List[TextContent]:
        """Get available layout list"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set layoutList to {{}}
                    repeat with masterSlide in master slides of targetDoc
                        set end of layoutList to name of masterSlide
                    end repeat
                    
                    -- 使用特殊分隔符来避免布局名称中的逗号问题
                    set AppleScript's text item delimiters to "|||"
                    set layoutString to layoutList as string
                    set AppleScript's text item delimiters to ""
                    
                    return layoutString
                end tell
            ''')
            
            if result:
                layouts = result.split("|||")
                layout_list = "\n".join([f"• {layout.strip()}" for layout in layouts if layout.strip()])
                return [TextContent(
                    type="text",
                    text=f"📐 可用布局:\n{layout_list}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="📐 没有找到可用布局"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取布局列表失败: {str(e)}"
            )]
