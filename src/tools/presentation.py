"""
Presentation management tools
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_file_path, KeynoteError


class PresentationTools:
    """Presentation management tools class"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """Get all presentation management tools"""
        return [
            Tool(
                name="create_presentation",
                description="📂 PRESENTATION CREATOR: Create a new Keynote presentation with professional themes. This tool opens a new presentation document in Keynote with your specified title and theme. Use this before starting any slide creation workflow.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Main title for the presentation (will appear on the first slide)",
                            "examples": ["Q4 Sales Review 2024", "Machine Learning Workshop", "Product Launch Strategy"]
                        },
                        "theme": {
                            "type": "string",
                            "description": "Keynote theme name for professional styling (optional). Use get_available_themes to see options.",
                            "examples": ["White", "Black", "Gradient", "Modern Portfolio", "Bold"]
                        },
                        "template": {
                            "type": "string",
                            "description": "Path to custom Keynote template file (optional, advanced users only)"
                        }
                    },
                    "required": ["title"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="open_presentation",
                description="Open existing Keynote presentation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Presentation file path"
                        }
                    },
                    "required": ["file_path"]
                }
            ),
            Tool(
                name="save_presentation",
                description="Save presentation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, defaults to current document)"
                        }
                    }
                }
            ),
            Tool(
                name="close_presentation",
                description="Close presentation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, defaults to current document)"
                        },
                        "should_save": {
                            "type": "boolean",
                            "description": "Whether to save (default is true)"
                        }
                    }
                }
            ),
            Tool(
                name="list_presentations",
                description="List all open presentations",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="set_presentation_theme",
                description="Set presentation theme",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, defaults to current document)"
                        },
                        "theme_name": {
                            "type": "string",
                            "description": "Theme name"
                        }
                    },
                    "required": ["theme_name"]
                }
            ),
            Tool(
                name="get_presentation_info",
                description="Get presentation information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, defaults to current document)"
                        }
                    }
                }
            ),
            Tool(
                name="get_available_themes",
                description="🎨 THEME BROWSER: Get a complete list of available Keynote themes for professional presentation styling. Use this to discover theme options before creating a presentation or to switch themes on existing presentations. Each theme provides different color schemes, fonts, and layout styles.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False
                }
            ),
            Tool(
                name="get_presentation_resolution",
                description="Get presentation resolution information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, defaults to current document)"
                        }
                    }
                }
            ),
            Tool(
                name="get_slide_size",
                description="Get slide size and aspect ratio information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, defaults to current document)"
                        }
                    }
                }
            )
        ]
    
    async def create_presentation(self, title: str, theme: str = "", template: str = "") -> List[TextContent]:
        """Create new presentation"""
        try:
            # Ensure Keynote is running
            if not self.runner.check_keynote_running():
                self.runner.launch_keynote()
            
            # Use the simplified presentation script
            result = self.runner.run_function(
                script_file='presentation_simple.applescript',
                function_name='createNewPresentation',
                args=[title, theme]
            )
            
            # Now that presentation exists, get available layouts
            try:
                # Import here to avoid circular imports
                from .slide import SlideTools
                slide_tools = SlideTools()
                layouts_result = await slide_tools.get_available_layouts()
                layouts_text = layouts_result[0].text if layouts_result else ""
                
                response_text = f"✅ Successfully created presentation: {result}\n\n"
                response_text += "🎯 **Ready for guided workflow!** Use `start_presentation_planning` to get layout guidance.\n\n"
                response_text += layouts_text
                
                return [TextContent(
                    type="text",
                    text=response_text
                )]
            except:
                # Fallback if layouts can't be retrieved
                return [TextContent(
                    type="text",
                    text=f"✅ Successfully created presentation: {result}\n\n🎯 **Ready for guided workflow!** Use `start_presentation_planning` to get layout guidance."
                )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to create presentation: {str(e)}"
            )]
    
    async def open_presentation(self, file_path: str) -> List[TextContent]:
        """Open presentation"""
        try:
            validate_file_path(file_path)
            
            # Ensure Keynote is running
            if not self.runner.check_keynote_running():
                self.runner.launch_keynote()
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    set targetFile to POSIX file "{file_path}"
                    open targetFile
                    return name of front document
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ Successfully opened presentation: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to open presentation: {str(e)}"
            )]
    
    async def save_presentation(self, doc_name: str = "") -> List[TextContent]:
        """Save presentation"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        save front document
                        return name of front document
                    else
                        save document "{doc_name}"
                        return "{doc_name}"
                    end if
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ Successfully saved presentation: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to save presentation: {str(e)}"
            )]
    
    async def close_presentation(self, doc_name: str = "", should_save: bool = True) -> List[TextContent]:
        """Close presentation"""
        try:
            save_flag = "true" if should_save else "false"
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set docName to name of targetDoc
                    
                    if {save_flag} then
                        save targetDoc
                    end if
                    
                    close targetDoc
                    return docName
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ Successfully closed presentation: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to close presentation: {str(e)}"
            )]
    
    async def list_presentations(self) -> List[TextContent]:
        """List all open presentations"""
        try:
            result = self.runner.run_inline_script('''
                tell application "Keynote"
                    set docList to {}
                    repeat with doc in documents
                        set end of docList to name of doc
                    end repeat
                    return docList as string
                end tell
            ''')
            
            if result:
                presentations = result.replace("{", "").replace("}", "").split(", ")
                presentation_list = "\n".join([f"• {name}" for name in presentations])
                return [TextContent(
                    type="text",
                    text=f"📋 Open presentations:\n{presentation_list}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="📋 No presentations currently open"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get presentation list: {str(e)}"
            )]
    
    async def set_presentation_theme(self, theme_name: str, doc_name: str = "") -> List[TextContent]:
        """Set presentation theme"""
        try:
            # Use Keynote 14 compatible theme setting method
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    -- First check if theme exists
                    set themeExists to false
                    repeat with t in themes
                        if name of t is "{theme_name}" then
                            set themeExists to true
                            exit repeat
                        end if
                    end repeat
                    
                    if not themeExists then
                        return "theme_not_found"
                    end if
                    
                    -- Use document theme property to set theme
                    try
                        set document theme of targetDoc to theme "{theme_name}"
                        return "success"
                    on error errMsg
                        return "error: " & errMsg
                    end try
                end tell
            ''')
            
            if result == "success":
                return [TextContent(
                    type="text",
                    text=f"✅ Successfully set theme: {theme_name}"
                )]
            elif result == "theme_not_found":
                return [TextContent(
                    type="text",
                    text=f"❌ Theme not found: {theme_name}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ Failed to set theme: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to set theme: {str(e)}"
            )]
    
    async def get_presentation_info(self, doc_name: str = "") -> List[TextContent]:
        """Get presentation information"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set docInfo to {{}}
                    set end of docInfo to name of targetDoc
                    set end of docInfo to count of slides of targetDoc
                    
                    try
                        set end of docInfo to name of theme of targetDoc
                    on error
                        set end of docInfo to "Unknown Theme"
                    end try
                    
                    return docInfo as string
                end tell
            ''')
            
            info_parts = result.replace("{", "").replace("}", "").split(", ")
            if len(info_parts) >= 3:
                name, slide_count, theme = info_parts[0], info_parts[1], info_parts[2]
                return [TextContent(
                    type="text",
                    text=f"📊 Presentation Information:\n• Name: {name}\n• Slide Count: {slide_count}\n• Theme: {theme}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"📊 Presentation Information: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get presentation information: {str(e)}"
            )]
    
    async def get_available_themes(self) -> List[TextContent]:
        """Get available themes list"""
        try:
            # Use the simplified presentation script
            result = self.runner.run_function(
                script_file='presentation_simple.applescript',
                function_name='getAvailableThemes',
                args=[]
            )
            
            if result:
                # Parse the AppleScript list result
                themes = result.replace("{", "").replace("}", "").split(", ")
                themes = [theme.strip('"') for theme in themes if theme.strip()]
                
                if themes:
                    theme_list = "\n".join([f"• {theme}" for theme in themes])
                    return [TextContent(
                        type="text",
                        text=f"🎨 Available themes ({len(themes)}):\n{theme_list}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="🎨 No themes found"
                    )]
            else:
                return [TextContent(
                    type="text",
                    text="🎨 Could not retrieve themes"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get themes list: {str(e)}"
            )]
    
    async def get_presentation_resolution(self, doc_name: str = "") -> List[TextContent]:
        """Get presentation resolution"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    try
                        set docWidth to width of targetDoc
                        set docHeight to height of targetDoc
                        
                        set AppleScript's text item delimiters to ","
                        set resolution to {{docWidth, docHeight}} as string
                        set AppleScript's text item delimiters to ""
                        
                        return resolution
                    on error
                        -- Return standard 16:9 resolution
                        return "1920,1080"
                    end try
                end tell
            ''')
            
            # Parse result
            resolution_parts = result.split(",")
            if len(resolution_parts) >= 2:
                width, height = resolution_parts[0], resolution_parts[1]
                aspect_ratio = round(float(width) / float(height), 3)
                
                # Determine ratio type
                if 1.7 < aspect_ratio < 1.8:
                    ratio_type = "16:9"
                elif 1.3 < aspect_ratio < 1.4:
                    ratio_type = "4:3"
                else:
                    ratio_type = "Custom"
                
                return [TextContent(
                    type="text",
                    text=f"📐 Presentation Resolution:\n• Width: {width} pixels\n• Height: {height} pixels\n• Ratio: {aspect_ratio} ({ratio_type})"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"📐 Resolution Information: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get resolution: {str(e)}"
            )]
    
    async def get_slide_size(self, doc_name: str = "") -> List[TextContent]:
        """Get slide size and aspect ratio information"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    try
                        set slideWidth to width of targetDoc
                        set slideHeight to height of targetDoc
                        set aspectRatio to slideWidth / slideHeight
                        
                        -- Determine ratio type
                        set ratioType to ""
                        if aspectRatio > 1.7 and aspectRatio < 1.8 then
                            set ratioType to "16:9"
                        else if aspectRatio > 1.3 and aspectRatio < 1.4 then
                            set ratioType to "4:3"
                        else
                            set ratioType to "Custom"
                        end if
                        
                        set AppleScript's text item delimiters to ","
                        set sizeInfo to {{slideWidth, slideHeight, aspectRatio, ratioType}} as string
                        set AppleScript's text item delimiters to ""
                        
                        return sizeInfo
                    on error
                        -- Return default values
                        return "1920,1080,1.777,16:9"
                    end try
                end tell
            ''')
            
            # Parse result
            size_parts = result.split(",")
            if len(size_parts) >= 4:
                width, height, ratio, ratio_type = size_parts[0], size_parts[1], size_parts[2], size_parts[3]
                
                # Calculate useful layout information
                width_num = float(width)
                height_num = float(height)
                
                # Calculate safe area (leaving margins)
                safe_width = int(width_num * 0.9)
                safe_height = int(height_num * 0.9)
                margin_x = int((width_num - safe_width) / 2)
                margin_y = int((height_num - safe_height) / 2)
                
                # Calculate common positions
                center_x = int(width_num / 2)
                center_y = int(height_num / 2)
                
                layout_info = f"""📏 Slide Size Information:
• Size: {width} × {height} pixels
• Ratio: {float(ratio):.3f} ({ratio_type})
• Center Point: ({center_x}, {center_y})

📐 Layout Reference:
• Safe Area: {safe_width} × {safe_height} pixels
• Margins: {margin_x} × {margin_y} pixels
• Title Area Suggestion: y = {margin_y} - {margin_y + 100}
• Content Area Suggestion: y = {margin_y + 120} - {safe_height + margin_y}"""
                
                return [TextContent(
                    type="text",
                    text=layout_info
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"📏 Size Information: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get slide size: {str(e)}"
            )] 