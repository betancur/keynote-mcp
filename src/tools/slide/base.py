"""
Main SlideTools class that integrates all slide operations
"""

from typing import List
from mcp.types import Tool, TextContent
from ...utils import AppleScriptRunner

from .schemas import get_slide_tool_schemas
from .basic_operations import SlideBasicOperations
from .navigation_operations import SlideNavigationOperations
from .layout_operations import SlideLayoutOperations


class SlideTools:
    """Slide operation tools class - Modular version"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
        
        # Initialize operation modules
        self.basic_ops = SlideBasicOperations(self.runner)
        self.navigation_ops = SlideNavigationOperations(self.runner)
        self.layout_ops = SlideLayoutOperations(self.runner)
    
    def get_tools(self) -> List[Tool]:
        """Get all slide operation tools"""
        return get_slide_tool_schemas()
    
    # Basic operations
    async def add_slide(self, doc_name: str = "", position: int = 0, layout: str = "", clear_default_content: bool = True) -> List[TextContent]:
        """Add new slide"""
        return await self.basic_ops.add_slide(doc_name, position, layout, clear_default_content)
    
    async def delete_slide(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        """Delete slide"""
        return await self.basic_ops.delete_slide(slide_number, doc_name)
    
    async def duplicate_slide(self, slide_number: int, doc_name: str = "", new_position: int = 0) -> List[TextContent]:
        """Duplicate slide"""
        return await self.basic_ops.duplicate_slide(slide_number, doc_name, new_position)
    
    async def move_slide(self, from_position: int, to_position: int, doc_name: str = "") -> List[TextContent]:
        """Move slide position"""
        return await self.basic_ops.move_slide(from_position, to_position, doc_name)
    
    # Navigation operations
    async def get_slide_count(self, doc_name: str = "") -> List[TextContent]:
        """Get slide count"""
        return await self.navigation_ops.get_slide_count(doc_name)
    
    async def select_slide(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        """Select specified slide"""
        return await self.navigation_ops.select_slide(slide_number, doc_name)
    
    async def get_slide_info(self, slide_number: int, doc_name: str = "") -> List[TextContent]:
        """Get slide information"""
        return await self.navigation_ops.get_slide_info(slide_number, doc_name)
    
    # Layout operations
    async def set_slide_layout(self, slide_number: int, layout: str, doc_name: str = "") -> List[TextContent]:
        """Set slide layout"""
        return await self.layout_ops.set_slide_layout(slide_number, layout, doc_name)
    
    async def get_available_layouts(self, doc_name: str = "") -> List[TextContent]:
        """Get available layout list"""
        return await self.layout_ops.get_available_layouts(doc_name)
