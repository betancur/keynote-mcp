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
    
    async def add_slide(self, doc_name: str = "", position: int = 0, layout: str = "", clear_default_content: bool = True, content_type: str = "", content_description: str = "") -> List[TextContent]:
        """Add new slide"""
        try:
            # If content_type is provided and no layout specified, use smart layout
            if content_type and layout == "":
                try:
                    # Try to use smart layout based on content type
                    from ...tools.smart_layout import SmartLayoutTools
                    smart_layout = SmartLayoutTools()
                    suggestion_result = smart_layout.runner.run_function(
                        script_file='smart_layout.applescript',
                        function_name='suggestLayoutForContent',
                        args=[doc_name, content_type, ""]
                    )
                    
                    if suggestion_result and suggestion_result.strip():
                        layout = suggestion_result.strip()
                    else:
                        layout = "2"  # Fallback to Title & Content
                except Exception:
                    layout = "2"  # Fallback to Title & Content if smart layout fails
            elif layout == "":
                layout = "2"  # Layout 2 is typically Title & Content
            
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
                            -- Try to use layout by number first (more reliable)
                            if "{layout}" is "1" or "{layout}" is "2" or "{layout}" is "3" or "{layout}" is "4" or "{layout}" is "5" then
                                set layoutNumber to {layout} as integer
                                set masterSlides to slide layouts of targetDoc
                                if layoutNumber ≤ (count of masterSlides) then
                                    set base slide of newSlide to item layoutNumber of masterSlides
                                else
                                    -- Fallback to layout 2 (Title & Content)
                                    set base slide of newSlide to item 2 of masterSlides
                                end if
                            else
                                -- Try to use layout by name
                                set base slide of newSlide to master slide "{layout}" of targetDoc
                            end if
                        on error
                            -- Fallback to layout 2 (Title & Content)
                            try
                                set masterSlides to slide layouts of targetDoc
                                if (count of masterSlides) ≥ 2 then
                                    set base slide of newSlide to item 2 of masterSlides
                                    log "Using default Title & Content layout"
                                end if
                            on error
                                log "Could not set any layout, using document default"
                            end try
                        end try
                    end if
                    
                    return slide number of newSlide
                end tell
            ''')
            
            # Set presenter notes for image/photo content types when using smart layout
            if content_type in ["image", "photo", "gallery", "multiple_images"] and content_description:
                try:
                    # Escape quotes in content description
                    escaped_description = content_description.replace('"', '\\"')
                    self.runner.run_inline_script(f'''
                        tell application "Keynote"
                            if "{doc_name}" is "" then
                                set targetDoc to front document
                            else
                                set targetDoc to document "{doc_name}"
                            end if
                            
                            set targetSlide to slide {result} of targetDoc
                            set presenter notes of targetSlide to "Image suggestion: {escaped_description}"
                        end tell
                    ''')
                except Exception:
                    # Ignore errors setting presenter notes
                    pass
            
            # Prepare layout and notes info
            notes_info = ""
            if content_type in ["image", "photo", "gallery", "multiple_images"] and content_description:
                notes_info = " + presenter notes with image suggestion"
            
            if content_type and layout != "2":
                layout_info = f" (Smart Layout: {layout} - optimized for {content_type})"
            elif layout == "2":
                layout_info = " (Layout: Title & Content - Default)"
            elif layout:
                layout_info = f" (Layout: {layout})"
            else:
                layout_info = " (Layout: Default)"
            
            return [TextContent(
                type="text",
                text=f"✅ Successfully added slide {result}{layout_info}{notes_info}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to add slide: {str(e)}"
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
                text=f"✅ Successfully deleted slide {slide_number}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to delete slide: {str(e)}"
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
                text=f"✅ Successfully duplicated slide, new number: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to duplicate slide: {str(e)}"
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
                text=f"✅ Successfully moved slide from position {from_position} to position {to_position}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to move slide: {str(e)}"
            )]
