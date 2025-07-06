"""
Smart Layout Tools - Content-aware slide layout selection
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number


class SmartLayoutTools:
    """Smart layout selection tools for content-aware slide creation"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
        self.script_file = 'smart_layout.applescript'
    
    def get_tools(self) -> List[Tool]:
        """Get all smart layout tools"""
        return [
            Tool(
                name="get_available_master_slides",
                description="Get list of available master slide layouts in the presentation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, uses front document if empty)"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="suggest_layout_for_content",
                description="Get recommended slide layout based on content type",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content_type": {
                            "type": "string",
                            "description": "Type of content: 'image', 'photo', 'text', 'content', 'title', 'quote', 'comparison', 'split', 'gallery', 'multiple_images', 'blank'"
                        },
                        "content_description": {
                            "type": "string",
                            "description": "Brief description of the content to be added"
                        },
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, uses front document if empty)"
                        }
                    },
                    "required": ["content_type"]
                }
            ),
            Tool(
                name="add_slide_with_smart_layout",
                description="Add a new slide with automatically selected layout based on content type",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content_type": {
                            "type": "string",
                            "description": "Type of content: 'image', 'photo', 'text', 'content', 'title', 'quote', 'comparison', 'split', 'gallery', 'multiple_images', 'blank'"
                        },
                        "content_description": {
                            "type": "string",
                            "description": "Brief description of the content to be added"
                        },
                        "position": {
                            "type": "integer",
                            "description": "Position to insert slide (0 for end)"
                        },
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, uses front document if empty)"
                        }
                    },
                    "required": ["content_type"]
                }
            ),
            Tool(
                name="get_layout_recommendations",
                description="Get top 3 layout recommendations for specific content",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content_type": {
                            "type": "string",
                            "description": "Type of content: 'image', 'photo', 'text', 'content', 'title', 'quote', 'comparison', 'split', 'gallery', 'multiple_images', 'blank'"
                        },
                        "content_description": {
                            "type": "string",
                            "description": "Brief description of the content to be added"
                        },
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, uses front document if empty)"
                        }
                    },
                    "required": ["content_type"]
                }
            )
        ]
    
    async def get_available_master_slides(self, doc_name: str = "") -> List[TextContent]:
        """Get available master slide layouts"""
        try:
            result = self.runner.run_function(
                script_file=self.script_file,
                function_name='getAvailableMasterSlides',
                args=[doc_name]
            )
            
            # Parse the JSON-like result
            if result and result.strip():
                # Remove brackets and quotes, split by comma
                clean_result = result.strip('[]"')
                layouts = [layout.strip('"') for layout in clean_result.split('", "')]
                
                layout_list = "\n".join([f"• {layout}" for layout in layouts])
                
                return [TextContent(
                    type="text",
                    text=f"📋 Available master slide layouts:\n{layout_list}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ No master slides found"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get master slides: {str(e)}"
            )]
    
    async def suggest_layout_for_content(self, content_type: str, content_description: str = "", doc_name: str = "") -> List[TextContent]:
        """Suggest best layout for content type"""
        try:
            result = self.runner.run_function(
                script_file=self.script_file,
                function_name='suggestLayoutForContent',
                args=[doc_name, content_type, content_description]
            )
            
            if result and result.strip():
                return [TextContent(
                    type="text",
                    text=f"💡 Recommended layout for '{content_type}' content: {result.strip()}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ Could not determine appropriate layout"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to suggest layout: {str(e)}"
            )]
    
    async def add_slide_with_smart_layout(self, content_type: str, content_description: str = "", position: int = 0, doc_name: str = "") -> List[TextContent]:
        """Add slide with automatically selected layout"""
        try:
            result = self.runner.run_function(
                script_file=self.script_file,
                function_name='addSlideWithSmartLayout',
                args=[doc_name, position, content_type, content_description]
            )
            
            if result and "|" in result:
                slide_number, layout = result.split("|", 1)
                
                # Check if presenter notes were added
                notes_info = ""
                if content_type in ["image", "photo", "gallery", "multiple_images"] and content_description:
                    notes_info = " + presenter notes with image suggestion"
                
                if layout == "default":
                    return [TextContent(
                        type="text",
                        text=f"✅ Added slide {slide_number} with default layout (suggested layout not available){notes_info}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"✅ Added slide {slide_number} with smart layout: '{layout}' (optimized for {content_type} content){notes_info}"
                    )]
            else:
                return [TextContent(
                    type="text",
                    text=f"✅ Added slide with smart layout for {content_type} content"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to add slide with smart layout: {str(e)}"
            )]
    
    async def get_layout_recommendations(self, content_type: str, content_description: str = "", doc_name: str = "") -> List[TextContent]:
        """Get top 3 layout recommendations"""
        try:
            result = self.runner.run_function(
                script_file=self.script_file,
                function_name='getLayoutRecommendations',
                args=[doc_name, content_type, content_description]
            )
            
            if result and result.strip():
                recommendations = result.split("|")
                
                if len(recommendations) >= 1 and recommendations[0]:
                    rec_text = f"🎯 Top layout recommendations for '{content_type}' content:\n"
                    rec_text += f"1. {recommendations[0]} (Best match)\n"
                    
                    if len(recommendations) >= 2 and recommendations[1]:
                        rec_text += f"2. {recommendations[1]}\n"
                    
                    if len(recommendations) >= 3 and recommendations[2]:
                        rec_text += f"3. {recommendations[2]}\n"
                    
                    return [TextContent(
                        type="text",
                        text=rec_text.strip()
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="❌ No layout recommendations available"
                    )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ Could not get layout recommendations"
                )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get layout recommendations: {str(e)}"
            )]