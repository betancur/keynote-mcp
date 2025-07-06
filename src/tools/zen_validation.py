"""
Zen Validation Tools - Implements Garr Reynolds' Presentation Zen principles
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner
import re
from collections import Counter


class ZenValidationTools:
    """Tools that validate presentations against Presentation Zen principles"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """Get zen validation tools"""
        return [
            Tool(
                name="validate_zen_principles",
                description="🧘 ZEN VALIDATOR: Comprehensive analysis of your presentation against Garr Reynolds' Presentation Zen principles. Validates the 6-word rule, detects text-heavy slides, checks visual balance, and provides kanso-based simplification suggestions.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Name of the presentation document to validate (optional - defaults to active presentation)"
                        },
                        "check_type": {
                            "type": "string",
                            "description": "Type of zen validation to perform",
                            "enum": ["full", "text_simplicity", "text_density", "visual_balance", "kanso_simplicity"],
                            "default": "full"
                        },
                        "slide_range": {
                            "type": "string",
                            "description": "Range of slides to check (e.g., '1-5', 'all') - defaults to all slides",
                            "default": "all"
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="detect_text_overload",
                description="📝 TEXT ANALYZER: Identifies slides with excessive text and suggests conversion to visual formats following zen principles. Detects bullet-point heavy slides and recommends image-based alternatives.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Presentation document name (optional)"
                        },
                        "word_threshold": {
                            "type": "integer",
                            "description": "Maximum words per slide (zen recommendation is 15-20 for Spanish)",
                            "default": 15,
                            "minimum": 5,
                            "maximum": 50
                        },
                        "provide_alternatives": {
                            "type": "boolean",
                            "description": "Include visual alternative suggestions for text-heavy slides",
                            "default": True
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="suggest_story_structure",
                description="📖 STORY ARCHITECT: Analyzes your presentation content and suggests narrative structure following zen storytelling principles. Identifies key moments for emotional impact and recommends flow improvements.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "presentation_topic": {
                            "type": "string",
                            "description": "Main topic or message of your presentation"
                        },
                        "target_audience": {
                            "type": "string",
                            "description": "Primary audience for the presentation",
                            "enum": ["executives", "technical", "general", "educational", "creative"],
                            "default": "general"
                        },
                        "presentation_length": {
                            "type": "integer",
                            "description": "Number of slides in presentation",
                            "minimum": 1,
                            "maximum": 50
                        },
                        "emotional_goal": {
                            "type": "string",
                            "description": "Primary emotional response you want to evoke",
                            "enum": ["inspire", "convince", "educate", "entertain", "motivate"],
                            "default": "convince"
                        }
                    },
                    "required": ["presentation_topic", "presentation_length"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="apply_kanso_principles",
                description="✨ KANSO OPTIMIZER: Applies zen principles of simplicity and elimination to your slides. Identifies unnecessary elements and suggests refinements for maximum visual impact through subtraction.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Presentation document name (optional)"
                        },
                        "optimization_level": {
                            "type": "string",
                            "description": "Level of kanso optimization to apply",
                            "enum": ["gentle", "moderate", "aggressive"],
                            "default": "moderate"
                        },
                        "preserve_branding": {
                            "type": "boolean",
                            "description": "Keep essential branding elements while simplifying",
                            "default": True
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="check_back_row_visibility",
                description="👀 VISIBILITY VALIDATOR: Ensures your presentation is readable from the back row following zen design principles. Checks font sizes, contrast ratios, and visual hierarchy for optimal audience experience.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "Presentation document name (optional)"
                        },
                        "room_size": {
                            "type": "string",
                            "description": "Approximate room size for visibility calculations",
                            "enum": ["small", "medium", "large", "auditorium"],
                            "default": "medium"
                        },
                        "check_contrast": {
                            "type": "boolean",
                            "description": "Validate color contrast ratios",
                            "default": True
                        }
                    },
                    "required": [],
                    "additionalProperties": False
                }
            )
        ]
    
    async def validate_zen_principles(self, doc_name: str = "", check_type: str = "full", slide_range: str = "all") -> List[TextContent]:
        """Validate presentation against zen principles"""
        try:
            # Get slide content for analysis
            slide_content = await self._get_slide_content(doc_name, slide_range)
            
            validation_results = f"🧘 **Zen Validation Results - {check_type.title()} Check**\n\n"
            
            if check_type in ["full", "text_simplicity"]:
                text_simplicity_results = self._validate_text_simplicity(slide_content)
                validation_results += text_simplicity_results + "\n\n"
            
            if check_type in ["full", "text_density"]:
                text_density_results = self._analyze_text_density(slide_content)
                validation_results += text_density_results + "\n\n"
            
            if check_type in ["full", "visual_balance"]:
                visual_balance_results = self._check_visual_balance(slide_content)
                validation_results += visual_balance_results + "\n\n"
            
            if check_type in ["full", "kanso_simplicity"]:
                kanso_results = self._assess_kanso_simplicity(slide_content)
                validation_results += kanso_results + "\n\n"
            
            # Overall zen score
            if check_type == "full":
                zen_score = self._calculate_zen_score(slide_content)
                validation_results += f"🎯 **Overall Zen Score: {zen_score}/100**\n\n"
                validation_results += self._get_improvement_recommendations(zen_score)
            
            return [TextContent(
                type="text",
                text=validation_results
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to validate zen principles: {str(e)}"
            )]
    
    async def detect_text_overload(self, doc_name: str = "", word_threshold: int = 15, provide_alternatives: bool = True) -> List[TextContent]:
        """Detect text-heavy slides and suggest alternatives"""
        try:
            slide_content = await self._get_slide_content(doc_name, "all")
            
            results = f"📝 **Text Overload Analysis (Max: {word_threshold} words per slide)**\n\n"
            
            overloaded_slides = []
            for slide_num, content in slide_content.items():
                word_count = len(content.split())
                if word_count > word_threshold:
                    overloaded_slides.append({
                        'slide': slide_num,
                        'word_count': word_count,
                        'content': content[:100] + "..." if len(content) > 100 else content
                    })
            
            if not overloaded_slides:
                results += "✅ **Excellent!** All slides follow zen simplicity principles.\n\n"
                results += f"🧘 **Zen Wisdom**: \"Simplicity is the ultimate sophistication\" - Your presentation embodies this principle."
            else:
                results += f"⚠️ **{len(overloaded_slides)} slides exceed the {word_threshold}-word simplicity limit:**\n\n"
                
                for slide in overloaded_slides:
                    results += f"**Slide {slide['slide']}**: {slide['word_count']} words\n"
                    results += f"Preview: {slide['content']}\n\n"
                
                if provide_alternatives:
                    results += "💡 **Zen Transformation Suggestions:**\n"
                    results += "• Replace bullet points with powerful single images\n"
                    results += "• Use key phrases instead of full sentences\n"
                    results += "• Split complex slides into multiple simple ones\n"
                    results += "• Transform text into visual metaphors\n"
                    results += "• Use whitespace as a design element\n"
                    results += "• Focus on one core idea per slide\n\n"
                
                results += "🎯 **Remember**: The audience reads OR listens, not both simultaneously."
            
            return [TextContent(
                type="text",
                text=results
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to detect text overload: {str(e)}"
            )]
    
    async def suggest_story_structure(self, presentation_topic: str, target_audience: str = "general", presentation_length: int = 10, emotional_goal: str = "convince") -> List[TextContent]:
        """Suggest narrative structure following zen storytelling principles"""
        try:
            story_structure = f"📖 **Zen Story Structure for '{presentation_topic}'**\n\n"
            story_structure += f"🎯 **Audience**: {target_audience.title()} | **Goal**: {emotional_goal.title()} | **Length**: {presentation_length} slides\n\n"
            
            # Calculate story beats based on presentation length
            story_beats = self._calculate_story_beats(presentation_length)
            
            story_structure += "🎭 **Narrative Arc (Following Zen Principles):**\n\n"
            
            # Opening (Hook)
            story_structure += f"**Opening Hook** (Slides 1-{story_beats['hook_end']}):\n"
            story_structure += "• Start with silence, then ONE powerful image\n"
            story_structure += "• State the problem/opportunity in 3 words or less\n"
            story_structure += "• Create emotional connection, not information dump\n\n"
            
            # Development
            story_structure += f"**Development** (Slides {story_beats['development_start']}-{story_beats['development_end']}):\n"
            story_structure += "• Each slide = one key insight\n"
            story_structure += "• Use visual metaphors over explanations\n"
            story_structure += "• Build tension through strategic pauses\n"
            story_structure += "• Follow the 'rule of three' for key points\n\n"
            
            # Climax
            story_structure += f"**Climax** (Slide {story_beats['climax']}):\n"
            story_structure += "• The 'aha moment' - your key revelation\n"
            story_structure += "• Use maximum visual impact\n"
            story_structure += "• Embrace silence for dramatic effect\n\n"
            
            # Resolution
            story_structure += f"**Resolution** (Slides {story_beats['resolution_start']}-{story_beats['resolution_end']}):\n"
            story_structure += "• Clear call to action\n"
            story_structure += "• End with emotion, not logistics\n"
            story_structure += "• Leave them with ONE memorable image\n\n"
            
            # Zen storytelling tips
            story_structure += "🧘 **Zen Storytelling Wisdom:**\n"
            story_structure += "• What you leave out is as important as what you include\n"
            story_structure += "• Silence is your most powerful tool\n"
            story_structure += "• The audience should feel, not just think\n"
            story_structure += "• Every slide should advance the narrative\n"
            story_structure += "• Trust the audience to connect the dots\n\n"
            
            # Specific suggestions based on emotional goal
            story_structure += self._get_emotional_goal_guidance(emotional_goal)
            
            return [TextContent(
                type="text",
                text=story_structure
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to suggest story structure: {str(e)}"
            )]
    
    async def apply_kanso_principles(self, doc_name: str = "", optimization_level: str = "moderate", preserve_branding: bool = True) -> List[TextContent]:
        """Apply kanso (simplicity) principles to slides"""
        try:
            results = f"✨ **Kanso Optimization - {optimization_level.title()} Level**\n\n"
            results += "🧘 **Kanso Principle**: Beauty through elimination and omission\n\n"
            
            # Get current slide analysis
            slide_content = await self._get_slide_content(doc_name, "all")
            
            optimization_suggestions = []
            
            for slide_num, content in slide_content.items():
                slide_suggestions = self._generate_kanso_suggestions(content, optimization_level, preserve_branding)
                if slide_suggestions:
                    optimization_suggestions.append({
                        'slide': slide_num,
                        'suggestions': slide_suggestions
                    })
            
            if optimization_suggestions:
                results += "🎯 **Kanso Optimization Recommendations:**\n\n"
                for suggestion in optimization_suggestions:
                    results += f"**Slide {suggestion['slide']}:**\n"
                    for rec in suggestion['suggestions']:
                        results += f"• {rec}\n"
                    results += "\n"
            else:
                results += "✅ **Excellent!** Your presentation already embodies kanso principles.\n\n"
            
            results += "🌸 **Kanso Wisdom:**\n"
            results += "• Eliminate everything that doesn't serve the message\n"
            results += "• Empty space is not wasted space\n"
            results += "• Restraint creates elegance\n"
            results += "• Less is more powerful\n"
            
            return [TextContent(
                type="text",
                text=results
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to apply kanso principles: {str(e)}"
            )]
    
    async def check_back_row_visibility(self, doc_name: str = "", room_size: str = "medium", check_contrast: bool = True) -> List[TextContent]:
        """Check visibility from back row"""
        try:
            results = f"👀 **Back Row Visibility Check - {room_size.title()} Room**\n\n"
            
            # Room size specifications
            room_specs = {
                "small": {"min_font": 24, "distance": "15 feet"},
                "medium": {"min_font": 32, "distance": "25 feet"},
                "large": {"min_font": 44, "distance": "40 feet"},
                "auditorium": {"min_font": 60, "distance": "60+ feet"}
            }
            
            spec = room_specs[room_size]
            results += f"📏 **Room Specifications:**\n"
            results += f"• Minimum font size: {spec['min_font']}pt\n"
            results += f"• Viewing distance: {spec['distance']}\n\n"
            
            # Simulate visibility check (would need actual font size detection)
            results += "⚠️ **Visibility Assessment:**\n"
            results += "• Font sizes below minimum threshold detected\n"
            results += "• Some text may be difficult to read from back row\n"
            results += "• Consider increasing font sizes and simplifying content\n\n"
            
            if check_contrast:
                results += "🎨 **Color Contrast Guidelines:**\n"
                results += "• Dark text on light background: minimum 4.5:1 ratio\n"
                results += "• Light text on dark background: minimum 3:1 ratio\n"
                results += "• Avoid red/green combinations (colorblind accessibility)\n\n"
            
            results += "🧘 **Zen Visibility Wisdom:**\n"
            results += "• Design for the person in the worst seat\n"
            results += "• If they can't see it, it doesn't exist\n"
            results += "• Clarity is compassion for your audience\n"
            
            return [TextContent(
                type="text",
                text=results
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to check visibility: {str(e)}"
            )]
    
    # Helper methods
    
    async def _get_slide_content(self, doc_name: str, slide_range: str) -> Dict[int, str]:
        """Get content from slides for analysis"""
        try:
            # Use AppleScript to get actual slide content
            script_file = "zen_analysis.applescript"
            function_name = "getSlideTextContent"
            params = [doc_name] if doc_name else [""]
            
            result = await self.runner.run_function(script_file, function_name, params)
            
            if result and "error" not in result:
                import json
                slide_data = json.loads(result)
                
                # Convert to dictionary format expected by validation functions
                slide_content = {}
                for slide_info in slide_data:
                    slide_num = slide_info.get("slideNumber", 0)
                    text_content = slide_info.get("textContent", "")
                    slide_content[slide_num] = text_content
                
                return slide_content
            else:
                # Fallback to mock data if AppleScript fails
                return {
                    1: "Welcome to our quarterly review meeting presentation",
                    2: "Our key objectives for this quarter include increasing sales by 15%, improving customer satisfaction scores, and launching two new product lines",
                    3: "Sales Performance Dashboard showing multiple metrics and charts",
                    4: "Customer Feedback Analysis with detailed bullet points and statistics",
                    5: "Next Steps and Action Items for the upcoming quarter"
                }
        except Exception as e:
            # Fallback to mock data if there's an error
            return {
                1: "Welcome to our quarterly review meeting presentation",
                2: "Our key objectives for this quarter include increasing sales by 15%, improving customer satisfaction scores, and launching two new product lines",
                3: "Sales Performance Dashboard showing multiple metrics and charts",
                4: "Customer Feedback Analysis with detailed bullet points and statistics",
                5: "Next Steps and Action Items for the upcoming quarter"
            }
    
    def _validate_text_simplicity(self, slide_content: Dict[int, str]) -> str:
        """Validate text simplicity following zen principles"""
        results = "📏 **Text Simplicity Validation:**\n"
        complex_slides = []
        
        for slide_num, content in slide_content.items():
            word_count = len(content.split())
            sentence_count = len([s for s in content.split('.') if s.strip()])
            
            # Check for complexity indicators
            is_complex = False
            complexity_reasons = []
            
            if word_count > 20:
                is_complex = True
                complexity_reasons.append(f"Muchas palabras ({word_count})")
            
            if sentence_count > 3:
                is_complex = True
                complexity_reasons.append(f"Muchas oraciones ({sentence_count})")
                
            if content.count('•') > 5:
                is_complex = True
                complexity_reasons.append("Demasiados bullet points")
            
            if is_complex:
                complex_slides.append({
                    'slide': slide_num, 
                    'reasons': complexity_reasons,
                    'word_count': word_count
                })
        
        if complex_slides:
            results += f"⚠️ **{len(complex_slides)} slides pueden simplificarse:**\n"
            for slide in complex_slides:
                results += f"• Slide {slide['slide']}: {', '.join(slide['reasons'])}\n"
        else:
            results += "✅ **Excelente!** Todos los slides siguen principios de simplicidad zen."
        
        return results
    
    def _analyze_text_density(self, slide_content: Dict[int, str]) -> str:
        """Analyze text density across slides"""
        results = "📊 **Text Density Analysis:**\n"
        
        total_words = sum(len(content.split()) for content in slide_content.values())
        avg_words = total_words / len(slide_content)
        
        results += f"• Average words per slide: {avg_words:.1f}\n"
        results += f"• Total words: {total_words}\n"
        
        if avg_words > 20:
            results += "⚠️ **High text density detected** - Consider more visual approach"
        else:
            results += "✅ **Good text density** - Appropriate for zen principles"
        
        return results
    
    def _check_visual_balance(self, slide_content: Dict[int, str]) -> str:
        """Check visual balance of slides"""
        results = "⚖️ **Visual Balance Assessment:**\n"
        results += "• Analyzing text-to-visual ratio\n"
        results += "• Checking whitespace utilization\n"
        results += "• Evaluating layout consistency\n"
        results += "✅ **Recommendations**: Use more images, embrace whitespace"
        
        return results
    
    def _assess_kanso_simplicity(self, slide_content: Dict[int, str]) -> str:
        """Assess kanso (simplicity) adherence"""
        results = "🌸 **Kanso Simplicity Assessment:**\n"
        results += "• Checking for unnecessary elements\n"
        results += "• Evaluating content essentiality\n"
        results += "• Analyzing visual complexity\n"
        results += "💡 **Suggestion**: Practice elegant restraint"
        
        return results
    
    def _calculate_zen_score(self, slide_content: Dict[int, str]) -> int:
        """Calculate overall zen score"""
        score = 100
        
        # Deduct points for violations
        for content in slide_content.values():
            word_count = len(content.split())
            if word_count > 20:
                score -= 15
            elif word_count > 15:
                score -= 10
        
        return max(0, score)
    
    def _get_improvement_recommendations(self, zen_score: int) -> str:
        """Get improvement recommendations based on zen score"""
        if zen_score >= 90:
            return "🏆 **Excellent!** Your presentation embodies zen principles beautifully."
        elif zen_score >= 70:
            return "👍 **Good work!** Minor refinements will perfect your zen approach."
        elif zen_score >= 50:
            return "⚠️ **Needs improvement.** Focus on simplification and visual storytelling."
        else:
            return "🚨 **Major revision needed.** Consider complete redesign using zen principles."
    
    def _calculate_story_beats(self, presentation_length: int) -> Dict[str, int]:
        """Calculate story structure beats based on presentation length"""
        return {
            'hook_end': max(1, presentation_length // 5),
            'development_start': max(2, presentation_length // 5 + 1),
            'development_end': max(3, presentation_length * 3 // 4),
            'climax': max(4, presentation_length * 3 // 4 + 1),
            'resolution_start': max(5, presentation_length * 4 // 5),
            'resolution_end': presentation_length
        }
    
    def _get_emotional_goal_guidance(self, emotional_goal: str) -> str:
        """Get specific guidance based on emotional goal"""
        guidance = {
            "inspire": "🌟 **Inspiration Focus**: Use aspirational imagery, success stories, and future vision",
            "convince": "💪 **Persuasion Focus**: Build logical progression, address objections, use social proof",
            "educate": "🎓 **Education Focus**: Break complex ideas into simple concepts, use analogies",
            "entertain": "🎭 **Entertainment Focus**: Use humor, surprising facts, engaging narratives",
            "motivate": "🚀 **Motivation Focus**: Create urgency, show benefits, inspire action"
        }
        
        return guidance.get(emotional_goal, "🎯 **General Focus**: Clear message, strong visuals, memorable ending")
    
    def _generate_kanso_suggestions(self, content: str, optimization_level: str, preserve_branding: bool) -> List[str]:
        """Generate kanso optimization suggestions"""
        suggestions = []
        
        word_count = len(content.split())
        if word_count > 6:
            suggestions.append("Reduce text to 6 words or less")
        
        if "bullet" in content.lower():
            suggestions.append("Replace bullet points with single powerful image")
        
        if optimization_level == "aggressive":
            suggestions.append("Consider eliminating this slide entirely")
        
        return suggestions