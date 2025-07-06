"""
Basic slide CRUD operations
"""

from typing import List
from mcp.types import TextContent
from ...utils import AppleScriptRunner, validate_slide_number


class SlideBasicOperations:
    """Basic slide operations like add, delete, duplicate, move"""
    
    def __init__(self, runner: AppleScriptRunner):
        self.runner = runner
    
    async def add_slide(self, doc_name: str = "", position: int = 0, layout: str = "", clear_default_content: bool = True) -> List[TextContent]:
        """Add new slide"""
        try:
            # If clear default content is enabled and no layout is specified, use Blank layout
            if clear_default_content and layout == "":
                layout = "Blank"
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    if {position} is 0 then
                        set newSlide to make new slide at end of slides of targetDoc
                    else
                        set newSlide to make new slide at slide {position} of targetDoc
                    end if
                    
                    if "{layout}" is not "" then
                        try
                            set base slide of newSlide to master slide "{layout}" of targetDoc
                        on error
                            -- 如果布局不存在，尝试使用 Blank 布局
                            try
                                set base slide of newSlide to master slide "Blank" of targetDoc
                                log "Layout {layout} not found, using Blank layout"
                            on error
                                log "Neither {layout} nor Blank layout found, using default layout"
                            end try
                        end try
                    end if
                    
                    return slide number of newSlide
                end tell
            ''')
            
            layout_info = f" (布局: {layout})" if layout else " (默认布局)"
            return [TextContent(
                type="text",
                text=f"✅ 成功添加幻灯片，编号: {result}{layout_info}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加幻灯片失败: {str(e)}"
            )]
    
    async def delete_slide(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        """Delete slide"""
        try:
            validate_slide_number(slide_number)
            
            self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    delete slide {slide_number} of targetDoc
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功删除幻灯片 {slide_number}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 删除幻灯片失败: {str(e)}"
            )]
    
    async def duplicate_slide(self, slide_number: int, doc_name: str = "", new_position: int = 0) -> List[TextContent]:
        """Duplicate slide"""
        try:
            validate_slide_number(slide_number)
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set sourceSlide to slide {slide_number} of targetDoc
                    set newSlide to duplicate sourceSlide
                    
                    if {new_position} is not 0 then
                        move newSlide to slide {new_position} of targetDoc
                    end if
                    
                    return slide number of newSlide
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功复制幻灯片，新编号: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 复制幻灯片失败: {str(e)}"
            )]
    
    async def move_slide(self, from_position: int, to_position: int, doc_name: str = "") -> List[TextContent]:
        """Move slide position"""
        try:
            validate_slide_number(from_position)
            validate_slide_number(to_position)
            
            self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set sourceSlide to slide {from_position} of targetDoc
                    move sourceSlide to slide {to_position} of targetDoc
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功移动幻灯片从位置 {from_position} 到位置 {to_position}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 移动幻灯片失败: {str(e)}"
            )]
