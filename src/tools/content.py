"""
Content management tools - Modular version
Using separated AppleScript files for better maintainability
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number, validate_coordinates, validate_file_path


class ContentTools:
    """Content management tools class - uses modular AppleScript files"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
        # Define which AppleScript file contains each function
        self.script_files = {
            # Text content functions
            'addTextBox': 'text_content.applescript',
            'addTitle': 'text_content.applescript', 
            'addSubtitle': 'text_content.applescript',
            'addBulletList': 'text_content.applescript',
            'addNumberedList': 'text_content.applescript',
            'addCodeBlock': 'text_content.applescript',
            'addQuote': 'text_content.applescript',
            'editTextBox': 'text_content.applescript',
            
            # Media content functions
            'addImage': 'media_content.applescript',
            
            # Shapes and tables functions
            'addShape': 'shapes_tables.applescript',
            'addTable': 'shapes_tables.applescript',
            'setTableCell': 'shapes_tables.applescript',
            
            # Formatting functions
            'setTextStyle': 'formatting.applescript',
            
            # Object management functions
            'positionObject': 'object_management.applescript',
            'resizeObject': 'object_management.applescript', 
            'deleteObject': 'object_management.applescript',
            'getSlideContentStats': 'object_management.applescript'
        }
    
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
            
            # Use default coordinates if not specified
            if x == 0.0 and y == 0.0:
                x, y = 100.0, 200.0
            
            # Use modular AppleScript function
            result = await self.runner.run_function(
                script_file=self.script_files['addTextBox'],
                function_name='addTextBox',
                args=["", slide_number, text, x, y, 0, 0]
            )
            
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
            
            # Use modular AppleScript function
            result = await self.runner.run_function(
                script_file=self.script_files['addImage'],
                function_name='addImage',
                args=["", slide_number, image_path, x, y, 0, 0]
            )
            
            return [TextContent(
                type="text",
                text=f"✅ Added image to slide {slide_number} at position ({x}, {y}): {image_path}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to add image: {str(e)}"
            )]
