"""
Tool definitions for slide operations
"""

from mcp.types import Tool

def get_slide_tool_schemas():
    """Get all slide operation tool schemas"""
    return [
        Tool(
            name="add_slide",
            description="Add new slide",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    },
                    "position": {
                        "type": "integer",
                        "description": "Insert position (optional, 0 means add at the end)"
                    },
                    "layout": {
                        "type": "string",
                        "description": "Layout type (optional)"
                    }
                }
            }
        ),
        Tool(
            name="delete_slide",
            description="Delete slide",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number to delete"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="duplicate_slide",
            description="Duplicate slide",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number to duplicate"
                    },
                    "new_position": {
                        "type": "integer",
                        "description": "New position (optional, 0 means add at the end)"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="move_slide",
            description="Move slide position",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    },
                    "from_position": {
                        "type": "integer",
                        "description": "Original position"
                    },
                    "to_position": {
                        "type": "integer",
                        "description": "Target position"
                    }
                },
                "required": ["from_position", "to_position"]
            }
        ),
        Tool(
            name="get_slide_count",
            description="Get slide count",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    }
                }
            }
        ),
        Tool(
            name="select_slide",
            description="Select specified slide",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="set_slide_layout",
            description="Set slide layout",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number"
                    },
                    "layout": {
                        "type": "string",
                        "description": "Layout type"
                    }
                },
                "required": ["slide_number", "layout"]
            }
        ),
        Tool(
            name="get_slide_info",
            description="Get slide information",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "Slide number"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="get_available_layouts",
            description="Get available layout list",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (optional, defaults to current document)"
                    }
                }
            }
        )
    ]
