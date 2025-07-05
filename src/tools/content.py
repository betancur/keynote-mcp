"""
Content management tools - Simplified version
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number, validate_coordinates, validate_file_path


class ContentTools:
    """Content management tools class"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """Get all content management tools"""
        return [
            Tool(
                name="add_text_box",
                description="Add a text box to slide",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "Slide number"
                        },
                        "text": {
                            "type": "string",
                            "description": "Text content"
                        },
                        "x": {
                            "type": "number",
                            "description": "X coordinate (pixels, optional)"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate (pixels, optional)"
                        }
                    },
                    "required": ["slide_number", "text"]
                }
            ),
            Tool(
                name="add_image",
                description="Add an image to slide",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "Slide number"
                        },
                        "image_path": {
                            "type": "string",
                            "description": "Image file path"
                        },
                        "x": {
                            "type": "number",
                            "description": "X coordinate (pixels, optional)"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate (pixels, optional)"
                        }
                    },
                    "required": ["slide_number", "image_path"]
                }
            )
        ]
    
    async def add_text_box(self, slide_number: int, text: str, x: Optional[float] = None, y: Optional[float] = None) -> List[TextContent]:
        """Add text box to slide"""
        try:
            validate_slide_number(slide_number)
            x, y = validate_coordinates(x, y)
            
            if not text or not text.strip():
                return [TextContent(
                    type="text",
                    text="❌ Text content cannot be empty"
                )]
            
            # Escape special characters in text
            escaped_text = text.replace('"', '\\"').replace('\n', '\\n')
            
            # Use default coordinates if not specified
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
                text=f"✅ Added text box to slide {slide_number} at position ({x}, {y})"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to add text box: {str(e)}"
            )]
    
    async def add_image(self, slide_number: int, image_path: str, x: Optional[float] = None, y: Optional[float] = None) -> List[TextContent]:
        """Add image to slide"""
        try:
            validate_slide_number(slide_number)
            validate_file_path(image_path)
            x, y = validate_coordinates(x, y)
            
            # Use default coordinates if not specified
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
                text=f"✅ Added image to slide {slide_number} at position ({x}, {y}): {image_path}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to add image: {str(e)}"
            )]
