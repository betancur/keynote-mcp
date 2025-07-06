"""
Layout Guidance Tools - Help Claude Desktop make better layout decisions
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner


class LayoutGuidanceTools:
    """Tools to help Claude Desktop choose appropriate layouts intelligently"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
        self.script_file = 'layout_guidance.applescript'
    
    def get_tools(self) -> List[Tool]:
        """Get all layout guidance tools"""
        return [
            Tool(
                name="get_detailed_layout_info",
                description="Get comprehensive information about all available layouts with use cases and recommendations",
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
                name="get_contextual_layout_suggestions",
                description="Get layout suggestions based on slide position, content type, and presentation context",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_position": {
                            "type": "integer",
                            "description": "Position of the slide in the presentation (1-based)"
                        },
                        "content_type": {
                            "type": "string",
                            "description": "Type of content: 'title', 'image', 'text', 'quote', 'comparison', 'gallery', etc."
                        },
                        "content_description": {
                            "type": "string",
                            "description": "Brief description of the slide content"
                        },
                        "presentation_theme": {
                            "type": "string",
                            "description": "Overall theme or topic of the presentation (optional)"
                        },
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, uses front document if empty)"
                        }
                    },
                    "required": ["slide_position", "content_type"]
                }
            ),
            Tool(
                name="get_recent_layout_usage",
                description="Check which layouts were used in recent slides to help avoid repetition",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "last_n_slides": {
                            "type": "integer",
                            "description": "Number of recent slides to check (default: 5)"
                        },
                        "doc_name": {
                            "type": "string",
                            "description": "Document name (optional, uses front document if empty)"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="get_layout_variety_suggestions",
                description="Get suggestions for creating varied and engaging presentations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "presentation_length": {
                            "type": "integer",
                            "description": "Total number of slides planned"
                        },
                        "presentation_type": {
                            "type": "string",
                            "description": "Type of presentation: 'business', 'educational', 'creative', 'technical'"
                        }
                    },
                    "required": ["presentation_length"]
                }
            )
        ]
    
    async def get_detailed_layout_info(self, doc_name: str = "") -> List[TextContent]:
        """Get detailed information about all available layouts"""
        try:
            result = self.runner.run_function(
                script_file='simple_layout_info.applescript',
                function_name='getSimpleLayoutInfo',
                args=[doc_name]
            )
            
            if result and result.strip():
                info_text = "📐 **Available Layouts with Use Cases:**\n\n"
                info_text += result
                info_text += "\n\n💡 **Tips for Better Presentations:**\n"
                info_text += "• Avoid using the same layout more than 2 times in a row\n"
                info_text += "• Mix text-heavy and visual layouts for better flow\n"
                info_text += "• Use photo layouts for impact and engagement\n"
                info_text += "• Section breaks help organize long presentations\n"
                info_text += "• End with a powerful statement or quote layout"
                
                return [TextContent(
                    type="text",
                    text=info_text
                )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ Could not get layout information"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get layout info: {str(e)}"
            )]
    
    async def get_contextual_layout_suggestions(self, slide_position: int, content_type: str, content_description: str = "", presentation_theme: str = "", doc_name: str = "") -> List[TextContent]:
        """Get contextual layout suggestions"""
        try:
            result = self.runner.run_function(
                script_file=self.script_file,
                function_name='getContextualLayoutSuggestions',
                args=[doc_name, slide_position, content_type, content_description, presentation_theme]
            )
            
            if result and result.strip():
                suggestions = result.split("|")
                
                suggestion_text = f"🎯 **Layout Suggestions for Slide {slide_position}** ({content_type} content):\n\n"
                
                for i, suggestion in enumerate(suggestions, 1):
                    if suggestion.strip():
                        suggestion_text += f"{i}. {suggestion.strip()}\n"
                
                return [TextContent(
                    type="text",
                    text=suggestion_text
                )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ Could not get contextual suggestions"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get suggestions: {str(e)}"
            )]
    
    async def get_recent_layout_usage(self, last_n_slides: int = 5, doc_name: str = "") -> List[TextContent]:
        """Get recent layout usage to avoid repetition"""
        try:
            result = self.runner.run_function(
                script_file='simple_recent_layouts.applescript',
                function_name='getSimpleRecentLayouts',
                args=[doc_name, last_n_slides]
            )
            
            if result and result.strip():
                usage_text = f"📊 **Recent Layout Usage** (last {last_n_slides} slides):\n\n"
                usage_text += result
                
                # Analyze for patterns
                lines = result.split('\n')
                layout_names = []
                for line in lines:
                    if ':' in line:
                        layout_name = line.split(':')[1].strip()
                        layout_names.append(layout_name)
                
                # Check for repetition
                unique_layouts = set(layout_names)
                if len(unique_layouts) == 1 and len(layout_names) > 2:
                    usage_text += f"\n⚠️ **Warning**: Same layout used {len(layout_names)} times in a row!"
                    usage_text += "\n💡 **Suggestion**: Consider using a different layout for visual variety"
                elif len(unique_layouts) < len(layout_names) / 2:
                    usage_text += f"\n🔄 **Notice**: Limited layout variety detected"
                    usage_text += "\n💡 **Suggestion**: Try mixing different layout types"
                else:
                    usage_text += f"\n✅ **Good**: Nice layout variety in recent slides"
                
                return [TextContent(
                    type="text",
                    text=usage_text
                )]
            else:
                return [TextContent(
                    type="text",
                    text="❌ Could not get recent layout usage"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get layout usage: {str(e)}"
            )]
    
    async def get_layout_variety_suggestions(self, presentation_length: int, presentation_type: str = "business") -> List[TextContent]:
        """Get suggestions for creating varied presentations"""
        try:
            suggestions_text = f"🎨 **Layout Variety Guide** for {presentation_length}-slide {presentation_type} presentation:\n\n"
            
            # General guidelines based on presentation length
            if presentation_length <= 5:
                suggestions_text += "**Short Presentation (≤5 slides):**\n"
                suggestions_text += "• Slide 1: Title layout for strong opening\n"
                suggestions_text += "• Slides 2-4: Alternate between content and visual layouts\n"
                suggestions_text += "• Last slide: Statement or Quote layout for impact\n\n"
                
            elif presentation_length <= 10:
                suggestions_text += "**Medium Presentation (6-10 slides):**\n"
                suggestions_text += "• Slide 1: Title layout\n"
                suggestions_text += "• Slides 2-3: Content layouts (Title & Bullets)\n"
                suggestions_text += "• Slide 4: Visual break (Photo layout)\n"
                suggestions_text += "• Slides 5-7: Mix content and visual layouts\n"
                suggestions_text += "• Slide 8: Section break or Quote\n"
                suggestions_text += "• Slides 9-10: Strong closing layouts\n\n"
                
            else:
                suggestions_text += "**Long Presentation (>10 slides):**\n"
                suggestions_text += "• Every 3-4 slides: Change layout type\n"
                suggestions_text += "• Every 5-6 slides: Add visual break (Photo/Gallery)\n"
                suggestions_text += "• Use Section layouts to divide topics\n"
                suggestions_text += "• Alternate text-heavy and visual layouts\n\n"
            
            # Type-specific suggestions
            if presentation_type == "business":
                suggestions_text += "**Business Presentation Tips:**\n"
                suggestions_text += "• Use Title & Bullets for key points\n"
                suggestions_text += "• Photo layouts for product showcases\n"
                suggestions_text += "• Statement layouts for key statistics\n"
                suggestions_text += "• Quote layouts for testimonials\n\n"
                
            elif presentation_type == "educational":
                suggestions_text += "**Educational Presentation Tips:**\n"
                suggestions_text += "• Section layouts for chapter breaks\n"
                suggestions_text += "• Gallery layouts for examples\n"
                suggestions_text += "• Title & Bullets for structured learning\n"
                suggestions_text += "• Blank layouts for interactive content\n\n"
                
            elif presentation_type == "creative":
                suggestions_text += "**Creative Presentation Tips:**\n"
                suggestions_text += "• Mix unconventional layouts\n"
                suggestions_text += "• Use Photo layouts for inspiration\n"
                suggestions_text += "• Blank layouts for custom designs\n"
                suggestions_text += "• Quote layouts for artistic statements\n\n"
            
            suggestions_text += "🎯 **Golden Rules:**\n"
            suggestions_text += "1. Never use the same layout more than 2 times in a row\n"
            suggestions_text += "2. Balance text-heavy and visual slides\n"
            suggestions_text += "3. Use transition slides (Section/Quote) to break up content\n"
            suggestions_text += "4. End with impact (Statement/Quote layout)\n"
            
            return [TextContent(
                type="text",
                text=suggestions_text
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to generate suggestions: {str(e)}"
            )]