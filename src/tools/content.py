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
            'getSlideContentStats': 'object_management.applescript',
            
            # Theme-aware content functions (NEW) - using simple version to avoid modular issues
            'setSlideContent': 'slide_content_simple.applescript',
            'getSlideDefaultElements': 'slide_content_simple.applescript'
        }
    
    def get_tools(self) -> List[Tool]:
        """Get all content management tools"""
        return [
            Tool(
                name="add_text_box",
                description="📝 TEXT CONTENT ADDER: Add custom text content to any slide with precise positioning. This tool creates a new text box with your content and places it at the specified coordinates. Perfect for adding custom text that doesn't fit in standard layout placeholders.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "Target slide number (1-based indexing)",
                            "minimum": 1
                        },
                        "text": {
                            "type": "string",
                            "description": "Text content to add to the slide. Can include multiple lines and paragraphs.",
                            "examples": ["Key takeaways from this quarter", "Contact us: info@company.com", "Thank you for your attention"]
                        },
                        "x": {
                            "type": "number",
                            "description": "X coordinate in pixels from left edge (optional - will auto-position if not specified)"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate in pixels from top edge (optional - will auto-position if not specified)"
                        }
                    },
                    "required": ["slide_number", "text"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="add_image",
                description="🖼️ IMAGE INSERTER: Add photos, graphics, or visual content to slides with smart positioning. This tool inserts image files directly into your presentation and automatically handles sizing and positioning. Supports common formats: PNG, JPG, JPEG, GIF, TIFF.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "Target slide number to add the image to (1-based indexing)",
                            "minimum": 1
                        },
                        "image_path": {
                            "type": "string",
                            "description": "Full file path to the image file on your local system",
                            "examples": ["/Users/username/Pictures/chart.png", "/Users/username/Desktop/logo.jpg", "~/Documents/product-photo.png"]
                        },
                        "x": {
                            "type": "number",
                            "description": "X coordinate in pixels from left edge (optional - will center horizontally if not specified)"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y coordinate in pixels from top edge (optional - will center vertically if not specified)"
                        }
                    },
                    "required": ["slide_number", "image_path"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="set_slide_content",
                description="🎨 THEME-AWARE CONTENT SETTER: Set slide content using the presentation's theme-styled title and body elements. This tool automatically applies consistent formatting, fonts, and colors based on your chosen theme. RECOMMENDED for professional-looking presentations instead of manual text boxes.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "Target slide number to set content for (1-based indexing)",
                            "minimum": 1
                        },
                        "title": {
                            "type": "string",
                            "description": "Title text - will be styled according to the presentation theme (optional but recommended for most slides)",
                            "examples": ["Q4 Results Overview", "Next Steps", "Key Takeaways", "Thank You"]
                        },
                        "body": {
                            "type": "string", 
                            "description": "Body/content text - supports bullet points, paragraphs, and multiple lines with theme-appropriate formatting",
                            "examples": ["• Revenue increased by 15%\n• Customer satisfaction improved\n• New markets opened", "Our three-step process ensures quality delivery every time.", "Questions?\nContact: support@company.com"]
                        }
                    },
                    "required": ["slide_number"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="get_slide_default_elements",
                description="🔍 LAYOUT INSPECTOR: Analyze a slide's available content placeholders and layout structure. This tool shows you what theme-styled elements (title, body, image placeholders) are available on a specific slide, helping you understand how to best add content using the slide's intended design.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "Target slide number to analyze (1-based indexing)",
                            "minimum": 1
                        }
                    },
                    "required": ["slide_number"],
                    "additionalProperties": False
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
            result = self.runner.run_function(
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
            result = self.runner.run_function(
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
    
    async def set_slide_content(self, slide_number: int, title: Optional[str] = None, body: Optional[str] = None) -> List[TextContent]:
        """Set slide content using theme's default elements"""
        try:
            validate_slide_number(slide_number)
            
            if not title and not body:
                return [TextContent(
                    type="text",
                    text="❌ At least title or body text must be provided"
                )]
            
            # Use theme-aware function
            result = self.runner.run_function(
                script_file=self.script_files['setSlideContent'],
                function_name='setSlideContent',
                args=["", slide_number, title or "", body or ""]
            )
            
            content_set = []
            if title:
                content_set.append("title")
            if body:
                content_set.append("body")
            
            return [TextContent(
                type="text",
                text=f"✅ Set slide {slide_number} content using theme elements: {', '.join(content_set)}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to set slide content: {str(e)}"
            )]
    
    async def get_slide_default_elements(self, slide_number: int) -> List[TextContent]:
        """Get available default elements in slide"""
        try:
            validate_slide_number(slide_number)
            
            result = self.runner.run_function(
                script_file=self.script_files['getSlideDefaultElements'],
                function_name='getSlideDefaultElements',
                args=["", slide_number]
            )
            
            # Parse the result (should be a list of available elements)
            if result and result.strip():
                elements = result.replace("{", "").replace("}", "").split(", ")
                available = [elem.strip('"') for elem in elements if elem.strip()]
                
                if available:
                    return [TextContent(
                        type="text",
                        text=f"✅ Available default elements in slide {slide_number}: {', '.join(available)}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"ℹ️ No default elements available in slide {slide_number} (blank layout)"
                    )]
            else:
                return [TextContent(
                    type="text",
                    text=f"ℹ️ No default elements found in slide {slide_number}"
                )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get slide elements: {str(e)}"
            )]
