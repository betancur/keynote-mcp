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

from .tools import PresentationTools, SlideTools, ContentTools, ExportTools
from .tools.smart_layout import SmartLayoutTools
from .utils import KeynoteError, AppleScriptError, FileOperationError, ParameterError


class KeynoteMCPServer:
    """Keynote MCP Server"""
    
    def __init__(self):
        self.server = Server("keynote-mcp")
        self.presentation_tools = PresentationTools()
        self.slide_tools = SlideTools()
        self.content_tools = ContentTools()
        self.export_tools = ExportTools()
        self.smart_layout_tools = SmartLayoutTools()
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register MCP handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools"""
            tools = []
            tools.extend(self.presentation_tools.get_tools())
            tools.extend(self.slide_tools.get_tools())
            tools.extend(self.content_tools.get_tools())
            tools.extend(self.export_tools.get_tools())
            tools.extend(self.smart_layout_tools.get_tools())
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
                
                # Slide operation tools
                elif name == "add_slide":
                    return await self.slide_tools.add_slide(
                        doc_name=arguments.get("doc_name", ""),
                        position=arguments.get("position", 0),
                        layout=arguments.get("layout", ""),
                        content_type=arguments.get("content_type", ""),
                        content_description=arguments.get("content_description", "")
                    )
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
                
                # Smart layout tools
                elif name == "get_available_master_slides":
                    return await self.smart_layout_tools.get_available_master_slides(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "suggest_layout_for_content":
                    return await self.smart_layout_tools.suggest_layout_for_content(
                        content_type=arguments["content_type"],
                        content_description=arguments.get("content_description", ""),
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "add_slide_with_smart_layout":
                    return await self.smart_layout_tools.add_slide_with_smart_layout(
                        content_type=arguments["content_type"],
                        content_description=arguments.get("content_description", ""),
                        position=arguments.get("position", 0),
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_layout_recommendations":
                    return await self.smart_layout_tools.get_layout_recommendations(
                        content_type=arguments["content_type"],
                        content_description=arguments.get("content_description", ""),
                        doc_name=arguments.get("doc_name", "")
                    )
                
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