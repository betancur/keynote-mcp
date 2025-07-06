"""
Guided Presentation Tools - Forces Claude Desktop to use analysis tools first
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner
import time


class GuidedPresentationTools:
    """Tools that guide Claude Desktop through a proper presentation creation workflow"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
        # Session state to track what Claude has done
        self.session_state = {
            'has_seen_layouts': False,
            'has_planned_variety': False,
            'last_layout_check': 0,
            'slides_created_without_planning': 0,
            'presentation_name': None
        }
    
    def get_tools(self) -> List[Tool]:
        """Get guided presentation workflow tools"""
        return [
            Tool(
                name="start_presentation_planning",
                description="🎯 PLANNING TOOL: Initialize presentation planning with smart layout strategy. This tool provides Claude Desktop with design guidelines and variety recommendations tailored to your presentation type and length. Can be used before or after creating the presentation document. Essential for professional, varied presentations.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "presentation_title": {
                            "type": "string",
                            "description": "The main title/topic of your presentation (e.g., 'Q4 Sales Review', 'Machine Learning Basics')"
                        },
                        "presentation_length": {
                            "type": "integer", 
                            "description": "Total number of slides planned for this presentation (recommended: 5-20 slides)",
                            "minimum": 1,
                            "maximum": 50
                        },
                        "presentation_type": {
                            "type": "string",
                            "description": "Presentation category for tailored layout recommendations",
                            "enum": ["business", "educational", "creative", "technical"],
                            "default": "business"
                        }
                    },
                    "required": ["presentation_title", "presentation_length"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="create_guided_slide",
                description="📝 MAIN SLIDE CREATION TOOL: Create a professionally designed slide with AI-powered layout selection. This tool automatically chooses the optimal Keynote layout based on your content type, slide position, and presentation flow. Requires start_presentation_planning to be called first for best results.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "The position/order of this slide in the presentation (1 = first slide, 2 = second slide, etc.)",
                            "minimum": 1
                        },
                        "content_type": {
                            "type": "string",
                            "description": "Primary content category for optimal layout selection",
                            "enum": ["title", "image", "text", "quote", "comparison", "gallery", "statement", "transition"],
                            "examples": ["title: opening/section slides", "image: photo-focused slides", "text: bullet points/content", "quote: testimonials/citations", "comparison: side-by-side content", "gallery: multiple images", "statement: bold single message", "transition: section breaks"]
                        },
                        "content_description": {
                            "type": "string",
                            "description": "Detailed description of what will be on this slide - helps AI choose the perfect layout. Be specific about text amount, images, and visual elements.",
                            "examples": ["Company logo and presentation title", "3 bullet points about quarterly results", "Large product photo with brief description", "Customer testimonial quote", "Side-by-side comparison of old vs new features"]
                        },
                        "preferred_layout": {
                            "type": "string",
                            "description": "Specific Keynote layout name to use (optional). If not provided, AI will suggest the best layout based on content_type and content_description.",
                            "examples": ["Title", "Title & Bullets", "Title & Photo", "Quote", "Photo - 3 Up", "Statement"]
                        },
                        "force_create": {
                            "type": "boolean",
                            "description": "Override planning requirements and variety checks (not recommended - may result in poor layout variety)",
                            "default": False
                        }
                    },
                    "required": ["slide_number", "content_type", "content_description"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="check_presentation_progress",
                description="📊 PROGRESS ANALYZER: Review your presentation's layout variety and get smart recommendations for upcoming slides. This tool analyzes recent slide layouts to ensure professional variety and suggests optimal layouts for your next slides. Use every 3-5 slides to maintain visual diversity and engagement.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Name of the specific presentation document to analyze (optional - defaults to currently active presentation)"
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="get_layout_recommendations_for_position",
                description="💡 LAYOUT ADVISOR: Get contextual layout recommendations for a specific slide position. This tool analyzes your content description and slide position to suggest 2-3 optimal layouts with explanations. Perfect for when you're unsure which layout to choose or want to explore alternatives before creating a slide.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_position": {
                            "type": "integer",
                            "description": "The slide number/position in your presentation (1 = first slide, 2 = second slide, etc.)",
                            "minimum": 1
                        },
                        "content_description": {
                            "type": "string",
                            "description": "Detailed description of what content will be on this slide. Include text amount, images, visual elements, and purpose.",
                            "examples": ["Opening slide with company logo and presentation title", "3 bullet points explaining our new product features", "Large customer photo with testimonial quote", "Comparison table showing before/after metrics"]
                        }
                    },
                    "required": ["slide_position", "content_description"],
                    "additionalProperties": False
                }
            )
        ]
    
    async def start_presentation_planning(self, presentation_title: str, presentation_length: int, presentation_type: str = "business") -> List[TextContent]:
        """
        Initialize the guided presentation workflow with comprehensive planning.
        
        This method provides Claude Desktop with:
        - Complete layout analysis and options
        - Variety guidelines for the presentation length
        - Session tracking to ensure good design practices
        - Contextual recommendations based on presentation type
        """
        try:
            # Reset session state for new presentation
            self.session_state = {
                'has_seen_layouts': True,
                'has_planned_variety': True,
                'last_layout_check': time.time(),
                'slides_created_without_planning': 0,
                'presentation_name': presentation_title
            }
            
            # Provide general layout guidance without querying specific presentation
            # (since no presentation exists yet)
            layout_text = """📐 **Layout Strategy Overview**
Keynote offers various professional layouts designed for different content types:
• **Title layouts**: Perfect for section headers and opening slides
• **Content layouts**: Title & Bullets, Title & Photo for main content
• **Visual layouts**: Photo-focused layouts for impact moments  
• **Special layouts**: Quote, Statement, Blank for specific purposes

**Key principle**: Vary your layouts every 2-3 slides for visual interest."""
            
            # Get variety suggestions based on presentation type and length
            variety_guide_text = self._get_variety_suggestions(presentation_length, presentation_type)
            
            response_text = f"🎯 **Presentation Planning Started: '{presentation_title}'**\n\n"
            response_text += f"📏 **Length**: {presentation_length} slides | **Type**: {presentation_type}\n\n"
            
            response_text += "=" * 60 + "\n"
            response_text += layout_text + "\n\n"
            
            response_text += "=" * 60 + "\n"
            response_text += variety_guide_text + "\n\n"
            
            response_text += "=" * 60 + "\n"
            response_text += "🧘 **Presentation Zen Principles (by Garr Reynolds):**\n"
            response_text += "• **Restraint in preparation** - Plan thoroughly but execute simply\n"
            response_text += "• **Simplicity in design** - Focus on one idea per slide\n"
            response_text += "• **Naturalness in delivery** - Be authentic and conversational\n"
            response_text += "• **Kanso (Simplicity)** - Beauty through elimination and omission\n"
            response_text += "• **Shizen (Naturalness)** - Avoid over-refinement and elaborate designs\n\n"
            
            response_text += "=" * 60 + "\n"
            response_text += "🚀 **Next Steps (Zen Workflow):**\n"
            response_text += f"1. Use `suggest_story_structure` to plan your narrative arc\n"
            response_text += f"2. Use `create_guided_slide` for each of your {presentation_length} slides\n"
            response_text += "3. Specify slide_number, content_type, and content_description\n"
            response_text += "4. I'll suggest the best layout based on position and content\n"
            response_text += "5. Use `detect_text_overload` to check text simplicity\n"
            response_text += "6. Use `validate_zen_principles` for final zen compliance\n\n"
            
            response_text += "💡 **Zen Reminder**: What you leave out is as important as what you include!\n\n"
            
            # Check if we can access layouts (presentation exists)
            try:
                from .slide import SlideTools
                slide_tools = SlideTools()
                layouts_result = await slide_tools.get_available_layouts()
                if layouts_result and "📐 Available layouts:" in layouts_result[0].text:
                    response_text += "✅ **Presentation Ready**: You can now use `create_guided_slide` to start building.\n\n"
                    response_text += layouts_result[0].text
                else:
                    response_text += "⚠️ **Next Step**: Create your presentation with `create_presentation`, then use `create_guided_slide`."
            except:
                response_text += "⚠️ **Next Step**: Create your presentation with `create_presentation`, then use `create_guided_slide`."
            
            return [TextContent(
                type="text",
                text=response_text
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to start presentation planning: {str(e)}"
            )]
    
    def _get_variety_suggestions(self, presentation_length: int, presentation_type: str) -> str:
        """Generate variety suggestions based on presentation characteristics"""
        
        suggestions = f"🎨 **Layout Variety Guide for {presentation_type.title()} Presentation ({presentation_length} slides)**\n\n"
        
        if presentation_type == "business":
            suggestions += """**Recommended Flow:**
• Slide 1: Title layout (strong opening)
• Slides 2-3: Title & Bullets (key points)
• Slide 4: Title & Photo (visual break)
• Slides 5-6: Content layouts (details)
• Slide 7: Quote or Statement (impact moment)
• Final slides: Title & Photo or Statement (strong close)"""
        
        elif presentation_type == "educational":
            suggestions += """**Recommended Flow:**
• Slide 1: Title layout (course/topic intro)
• Slides 2-4: Title & Bullets (learning objectives)
• Slide 5: Photo layout (visual example)
• Slides 6-8: Mixed content layouts
• Slide 9: Quote layout (key concept)
• Final slides: Summary with Title & Bullets"""
        
        elif presentation_type == "creative":
            suggestions += """**Recommended Flow:**
• Slide 1: Photo or Statement (visual impact)
• Slides 2-3: Photo layouts (showcase work)
• Slide 4: Quote layout (inspiration)
• Slides 5-7: Mixed visual layouts
• Final slides: Statement or Blank (artistic close)"""
        
        else:  # technical
            suggestions += """**Recommended Flow:**
• Slide 1: Title layout (technical topic)
• Slides 2-4: Title & Bullets (specifications)
• Slide 5: Photo layout (diagrams/charts)
• Slides 6-8: Content layouts (detailed info)
• Final slides: Title & Bullets (conclusions)"""
        
        # Add length-specific advice
        if presentation_length <= 5:
            suggestions += "\n\n**Short Presentation Tip**: Use 2-3 different layouts maximum"
        elif presentation_length <= 10:
            suggestions += "\n\n**Medium Presentation Tip**: Aim for 4-5 different layouts with good variety"
        else:
            suggestions += "\n\n**Long Presentation Tip**: Use 6+ layouts, change every 2-3 slides"
            
        return suggestions
    
    async def create_guided_slide(self, slide_number: int, content_type: str, content_description: str, preferred_layout: str = "", force_create: bool = False) -> List[TextContent]:
        """
        Create a slide with intelligent layout selection and guidance.
        
        This method:
        - Analyzes content type and description for optimal layout choice
        - Enforces planning workflow to ensure variety
        - Provides contextual layout recommendations
        - Tracks session state to prevent repetitive layouts
        - Integrates with smart layout tools for AI-powered suggestions
        """
        try:
            # Check if planning has been done
            if not self.session_state['has_seen_layouts'] and not force_create:
                return [TextContent(
                    type="text",
                    text="🚫 **Planning Required First!**\n\nPlease use `start_presentation_planning` before creating slides.\nThis ensures you see all layout options and variety guidelines.\n\nOr use `force_create: true` to override (not recommended)."
                )]
            
            # Check if too many slides created without recent planning check
            if self.session_state['slides_created_without_planning'] >= 3:
                return [TextContent(
                    type="text",
                    text="⚠️ **Variety Check Recommended!**\n\nYou've created 3 slides without checking variety.\nPlease use `check_presentation_progress` to ensure good layout diversity.\n\nOr use `force_create: true` to continue anyway."
                )]
            
            # Get layout suggestion if not provided
            if not preferred_layout:
                try:
                    from .smart_layout import SmartLayoutTools
                    smart_tools = SmartLayoutTools()
                    suggestion = await smart_tools.suggest_layout_for_content(content_type, content_description)
                    suggested_layout = suggestion[0].text.split(": ")[1] if ": " in suggestion[0].text else "Title & Bullets"
                except:
                    # Fallback logic if smart tools fail
                    if content_type == "title":
                        suggested_layout = "Title"
                    elif content_type == "image":
                        suggested_layout = "Title & Photo"
                    elif content_type == "quote":
                        suggested_layout = "Quote"
                    elif content_type == "gallery":
                        suggested_layout = "Photo - 3 Up"
                    else:
                        suggested_layout = "Title & Bullets"
            else:
                suggested_layout = preferred_layout
            
            # Create the slide using existing tools
            from .slide import SlideTools
            slide_tools = SlideTools()
            
            result = await slide_tools.add_slide(
                position=slide_number if slide_number > 0 else 0,
                layout=suggested_layout,
                content_type=content_type,
                content_description=content_description
            )
            
            # Update session state
            self.session_state['slides_created_without_planning'] += 1
            
            # Add guidance to the response with zen validation
            original_text = result[0].text
            guidance_text = f"\n\n💡 **Layout Choice**: {suggested_layout}\n"
            guidance_text += f"📍 **Position**: Slide {slide_number}\n"
            guidance_text += f"🎯 **Content**: {content_type} - {content_description}\n"
            
            # Zen validation for content description (simplicity check)
            word_count = len(content_description.split())
            if word_count > 20:
                guidance_text += f"\n🧘 **Zen Alert**: Content description muy extenso ({word_count} palabras)\n"
                guidance_text += f"💡 **Zen Tip**: Considera simplificar a ideas más concisas\n"
            elif word_count > 15:
                guidance_text += f"\n⚠️ **Zen Notice**: Content moderadamente extenso ({word_count} palabras)\n"
            else:
                guidance_text += f"\n✅ **Zen Compliant**: Content sigue principios de simplicidad\n"
            
            # Suggest checking variety periodically
            if self.session_state['slides_created_without_planning'] >= 2:
                guidance_text += f"\n🔄 **Tip**: Consider using `detect_text_overload` to check zen compliance"
            
            # Add zen reminders every few slides
            if slide_number % 3 == 0:
                guidance_text += f"\n🧘 **Zen Reminder**: Less is more powerful - embrace simplicity"
            
            enhanced_text = original_text + guidance_text
            
            return [TextContent(
                type="text",
                text=enhanced_text
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to create guided slide: {str(e)}"
            )]
    
    async def check_presentation_progress(self, doc_name: str = "") -> List[TextContent]:
        """Check presentation progress and layout variety"""
        try:
            # Reset the planning counter
            self.session_state['slides_created_without_planning'] = 0
            self.session_state['last_layout_check'] = time.time()
            
            from .layout_guidance import LayoutGuidanceTools
            layout_tools = LayoutGuidanceTools()
            
            recent_usage = await layout_tools.get_recent_layout_usage(last_n_slides=5, doc_name=doc_name)
            
            progress_text = "📊 **Presentation Progress Check**\n\n"
            progress_text += recent_usage[0].text + "\n\n"
            
            progress_text += "🎯 **Next Slide Recommendations:**\n"
            progress_text += "• If last slide was text-heavy, try a photo layout\n"
            progress_text += "• If you've used 2-3 content slides, add a visual break\n"
            progress_text += "• Consider section transitions every 4-5 slides\n"
            progress_text += "• Use statement/quote layouts for impact moments\n\n"
            
            progress_text += "✅ **You can now continue creating slides with `create_guided_slide`**"
            
            return [TextContent(
                type="text",
                text=progress_text
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to check progress: {str(e)}"
            )]
    
    async def get_layout_recommendations_for_position(self, slide_position: int, content_description: str) -> List[TextContent]:
        """Get specific recommendations for a slide position"""
        try:
            # Analyze content description to determine type
            content_type = "text"
            if any(word in content_description.lower() for word in ["image", "photo", "picture", "visual"]):
                content_type = "image"
            elif any(word in content_description.lower() for word in ["quote", "testimonial", "saying"]):
                content_type = "quote"
            elif any(word in content_description.lower() for word in ["title", "header", "section"]):
                content_type = "title"
            elif any(word in content_description.lower() for word in ["gallery", "multiple", "several"]):
                content_type = "gallery"
            
            from .smart_layout import SmartLayoutTools
            smart_tools = SmartLayoutTools()
            
            suggestion = await smart_tools.suggest_layout_for_content(content_type, content_description)
            
            recommendations_text = f"💡 **Layout Recommendations for Slide {slide_position}**\n\n"
            recommendations_text += f"📝 **Content**: {content_description}\n"
            recommendations_text += f"🔍 **Detected Type**: {content_type}\n\n"
            recommendations_text += suggestion[0].text + "\n\n"
            
            # Add context-specific advice
            if slide_position <= 2:
                recommendations_text += "🚀 **Opening Slide Tips**: Use strong, clear layouts like Title or Title & Photo"
            elif slide_position >= 8:
                recommendations_text += "🎯 **Closing Slide Tips**: Consider Statement, Quote, or impactful photo layouts"
            else:
                recommendations_text += "📊 **Content Slide Tips**: Vary between text and visual layouts for better flow"
            
            return [TextContent(
                type="text",
                text=recommendations_text
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to get recommendations: {str(e)}"
            )]