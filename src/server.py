#!/usr/bin/env python3
"""
Keynote-MCP Server
A Model Context Protocol server for AI assistants to control Keynote presentations through AppleScript automation.
"""

import asyncio
import json
import sys
from typing import Any, Sequence

from mcp.server import Server
from mcp.types import (
    CallToolRequest,
    ListToolsRequest,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from mcp.server.stdio import stdio_server

from .tools import PresentationTools, SlideTools, ContentTools, ExportTools, ZenValidationTools
from .tools.smart_layout import SmartLayoutTools
from .tools.layout_guidance import LayoutGuidanceTools
from .tools.guided_presentation import GuidedPresentationTools
from .utils import KeynoteError, AppleScriptError, FileOperationError, ParameterError


class KeynoteMCPServer:
    """Keynote MCP Server"""
    
    def __init__(self):
        self.server = Server("keynote-mcp")
        self.presentation_tools = PresentationTools()
        self.slide_tools = SlideTools()
        self.content_tools = ContentTools()
        self.export_tools = ExportTools()
        # Keep smart layout and guidance for internal use
        self.smart_layout_tools = SmartLayoutTools()
        self.layout_guidance_tools = LayoutGuidanceTools()
        # New guided workflow - this is what Claude Desktop will primarily use
        self.guided_presentation_tools = GuidedPresentationTools()
        # Zen validation tools for Presentation Zen principles
        self.zen_validation_tools = ZenValidationTools()
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register MCP handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """
            List all available tools with strategic ordering for Claude Desktop.
            
            Tools are ordered by priority to guide Claude Desktop's workflow:
            1. ZEN VALIDATION TOOLS (highest priority) - Presentation Zen principles
            2. GUIDED WORKFLOW TOOLS - Forces proper planning and layout guidance
            3. PRESENTATION MANAGEMENT - Core document operations  
            4. CONTENT & EXPORT TOOLS - Adding content and sharing
            5. ESSENTIAL SLIDE OPERATIONS - Limited to necessary functions only
            
            This ordering ensures Claude Desktop follows Presentation Zen methodology first,
            resulting in better presentation quality, layout variety, and zen principles.
            """
            tools = []
            # Priority 1: Zen validation tools (HIGHEST priority - Presentation Zen principles)
            # These tools ensure adherence to Garr Reynolds' Presentation Zen methodology
            tools.extend(self.zen_validation_tools.get_tools())
            
            # Priority 2: Essential workflow tools (Claude MUST use these second)
            # These tools enforce proper planning and provide layout guidance
            tools.extend(self.guided_presentation_tools.get_tools())
            
            # Priority 3: Presentation management
            # Basic document operations - create, open, save, themes
            tools.extend(self.presentation_tools.get_tools())
            
            # Priority 4: Content and export tools
            # Adding content and exporting final results
            tools.extend(self.content_tools.get_tools())
            tools.extend(self.export_tools.get_tools())
            
            # Priority 5: Advanced tools (kept for power users, but not prominently featured)
            # Note: Removed basic slide tools and smart layout tools to force guided workflow
            # Only include essential slide operations that don't bypass the guided workflow
            essential_slide_tools = [tool for tool in self.slide_tools.get_tools() 
                                   if tool.name in ["delete_slide", "duplicate_slide", "move_slide", 
                                                  "get_slide_count", "select_slide", "get_slide_info", 
                                                  "set_slide_layout", "get_available_layouts"]]
            tools.extend(essential_slide_tools)
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Call tool"""
            try:
                # Presentation management tools
                if name == "create_presentation":
                    return await self.presentation_tools.create_presentation(
                        title=arguments["title"],
                        theme=arguments.get("theme", ""),
                        template=arguments.get("template", "")
                    )
                elif name == "open_presentation":
                    return await self.presentation_tools.open_presentation(
                        file_path=arguments["file_path"]
                    )
                elif name == "save_presentation":
                    return await self.presentation_tools.save_presentation(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "close_presentation":
                    return await self.presentation_tools.close_presentation(
                        doc_name=arguments.get("doc_name", ""),
                        should_save=arguments.get("should_save", True)
                    )
                elif name == "list_presentations":
                    return await self.presentation_tools.list_presentations()
                elif name == "set_presentation_theme":
                    return await self.presentation_tools.set_presentation_theme(
                        theme_name=arguments["theme_name"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_presentation_info":
                    return await self.presentation_tools.get_presentation_info(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_available_themes":
                    return await self.presentation_tools.get_available_themes()
                elif name == "get_presentation_resolution":
                    return await self.presentation_tools.get_presentation_resolution(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_slide_size":
                    return await self.presentation_tools.get_slide_size(
                        doc_name=arguments.get("doc_name", "")
                    )
                
                # Zen validation tools (HIGHEST PRIORITY - Presentation Zen principles)
                elif name == "validate_zen_principles":
                    return await self.zen_validation_tools.validate_zen_principles(
                        doc_name=arguments.get("doc_name", ""),
                        check_type=arguments.get("check_type", "full"),
                        slide_range=arguments.get("slide_range", "all")
                    )
                elif name == "detect_text_overload":
                    return await self.zen_validation_tools.detect_text_overload(
                        doc_name=arguments.get("doc_name", ""),
                        word_threshold=arguments.get("word_threshold", 15),
                        provide_alternatives=arguments.get("provide_alternatives", True)
                    )
                elif name == "suggest_story_structure":
                    return await self.zen_validation_tools.suggest_story_structure(
                        presentation_topic=arguments["presentation_topic"],
                        target_audience=arguments.get("target_audience", "general"),
                        presentation_length=arguments["presentation_length"],
                        emotional_goal=arguments.get("emotional_goal", "convince")
                    )
                elif name == "apply_kanso_principles":
                    return await self.zen_validation_tools.apply_kanso_principles(
                        doc_name=arguments.get("doc_name", ""),
                        optimization_level=arguments.get("optimization_level", "moderate"),
                        preserve_branding=arguments.get("preserve_branding", True)
                    )
                elif name == "check_back_row_visibility":
                    return await self.zen_validation_tools.check_back_row_visibility(
                        doc_name=arguments.get("doc_name", ""),
                        room_size=arguments.get("room_size", "medium"),
                        check_contrast=arguments.get("check_contrast", True)
                    )
                
                # Guided presentation workflow tools (PRIORITY)
                elif name == "start_presentation_planning":
                    return await self.guided_presentation_tools.start_presentation_planning(
                        presentation_title=arguments["presentation_title"],
                        presentation_length=arguments["presentation_length"],
                        presentation_type=arguments.get("presentation_type", "business")
                    )
                elif name == "create_guided_slide":
                    return await self.guided_presentation_tools.create_guided_slide(
                        slide_number=arguments["slide_number"],
                        content_type=arguments["content_type"],
                        content_description=arguments["content_description"],
                        preferred_layout=arguments.get("preferred_layout", ""),
                        force_create=arguments.get("force_create", False)
                    )
                elif name == "check_presentation_progress":
                    return await self.guided_presentation_tools.check_presentation_progress(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_layout_recommendations_for_position":
                    return await self.guided_presentation_tools.get_layout_recommendations_for_position(
                        slide_position=arguments["slide_position"],
                        content_description=arguments["content_description"]
                    )
                
                # Legacy slide operation tools (kept for compatibility but discouraged)
                # elif name == "add_slide":  # REMOVED - forces use of guided workflow
                elif name == "delete_slide":
                    return await self.slide_tools.delete_slide(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "duplicate_slide":
                    return await self.slide_tools.duplicate_slide(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", ""),
                        new_position=arguments.get("new_position", 0)
                    )
                elif name == "move_slide":
                    return await self.slide_tools.move_slide(
                        from_position=arguments["from_position"],
                        to_position=arguments["to_position"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_slide_count":
                    return await self.slide_tools.get_slide_count(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "select_slide":
                    return await self.slide_tools.select_slide(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "set_slide_layout":
                    return await self.slide_tools.set_slide_layout(
                        slide_number=arguments["slide_number"],
                        layout=arguments["layout"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_slide_info":
                    return await self.slide_tools.get_slide_info(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_available_layouts":
                    return await self.slide_tools.get_available_layouts(
                        doc_name=arguments.get("doc_name", "")
                    )
                
                # Content management tools
                elif name == "add_text_box":
                    return await self.content_tools.add_text_box(
                        slide_number=arguments["slide_number"],
                        text=arguments["text"],
                        x=arguments.get("x"),
                        y=arguments.get("y")
                    )
                elif name == "add_image":
                    return await self.content_tools.add_image(
                        slide_number=arguments["slide_number"],
                        image_path=arguments["image_path"],
                        x=arguments.get("x"),
                        y=arguments.get("y")
                    )
                elif name == "set_slide_content":
                    return await self.content_tools.set_slide_content(
                        slide_number=arguments["slide_number"],
                        title=arguments.get("title"),
                        body=arguments.get("body")
                    )
                elif name == "get_slide_default_elements":
                    return await self.content_tools.get_slide_default_elements(
                        slide_number=arguments["slide_number"]
                    )
                
                # Export and screenshot tools
                elif name == "screenshot_slide":
                    return await self.export_tools.screenshot_slide(
                        slide_number=arguments["slide_number"],
                        output_path=arguments["output_path"],
                        format=arguments.get("format", "png")
                    )
                elif name == "export_pdf":
                    return await self.export_tools.export_pdf(
                        output_path=arguments["output_path"]
                    )
                elif name == "export_images":
                    return await self.export_tools.export_images(
                        output_dir=arguments["output_dir"],
                        format=arguments.get("format", "png")
                    )
                
                # Legacy tools (REMOVED to force guided workflow)
                # These tools are still available internally but not exposed to Claude Desktop
                # This forces the use of the guided presentation workflow
                
                # Note: Smart layout and guidance tools are now integrated into the guided workflow
                # If needed for debugging, they can be temporarily re-enabled
                
                else:
                    return [TextContent(
                        type="text",
                        text=f"❌ Unknown tool: {name}"
                    )]
                    
            except ParameterError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Parameter error: {str(e)}"
                )]
            except AppleScriptError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ AppleScript error: {str(e)}"
                )]
            except FileOperationError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ File operation error: {str(e)}"
                )]
            except KeynoteError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Keynote error: {str(e)}"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Unknown error: {str(e)}"
                )]
    
    async def run(self):
        """Start the server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main function"""
    server = KeynoteMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main()) 