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
        """Set the layout of a slide"""
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
                        -- Find the target layout
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
                        
                        -- Set slide layout (using correct syntax: base slide)
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
                    text=f"✅ Successfully set layout of slide {slide_number} to: {layout}"
                )]
            elif result == "layout_not_found":
                return [TextContent(
                    type="text",
                    text=f"❌ Layout not found: {layout}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Failed to set layout: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to set slide layout: {str(e)}"
            )]
    
    async def get_available_layouts(self, doc_name: str = "") -> List[TextContent]:
        """Get the list of available layouts"""
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
                    
                    -- Use a special delimiter to avoid issues with commas in layout names
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
                    text=f"📐 Available layouts:\n{layout_list}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="📐 No available layouts found"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get layout list: {str(e)}"
            )]
