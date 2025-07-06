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
                        "description": "文档名称（可选，默认为当前文档）"
                    },
                    "position": {
                        "type": "integer",
                        "description": "插入位置（可选，0表示在末尾添加）"
                    },
                    "layout": {
                        "type": "string",
                        "description": "布局类型（可选）"
                    }
                }
            }
        ),
        Tool(
            name="delete_slide",
            description="删除幻灯片",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "要删除的幻灯片编号"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="duplicate_slide",
            description="复制幻灯片",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "要复制的幻灯片编号"
                    },
                    "new_position": {
                        "type": "integer",
                        "description": "新位置（可选，0表示在末尾添加）"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="move_slide",
            description="移动幻灯片位置",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    },
                    "from_position": {
                        "type": "integer",
                        "description": "原位置"
                    },
                    "to_position": {
                        "type": "integer",
                        "description": "目标位置"
                    }
                },
                "required": ["from_position", "to_position"]
            }
        ),
        Tool(
            name="get_slide_count",
            description="获取幻灯片数量",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    }
                }
            }
        ),
        Tool(
            name="select_slide",
            description="选择指定幻灯片",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "幻灯片编号"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="set_slide_layout",
            description="设置幻灯片布局",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "幻灯片编号"
                    },
                    "layout": {
                        "type": "string",
                        "description": "布局类型"
                    }
                },
                "required": ["slide_number", "layout"]
            }
        ),
        Tool(
            name="get_slide_info",
            description="获取幻灯片信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    },
                    "slide_number": {
                        "type": "integer",
                        "description": "幻灯片编号"
                    }
                },
                "required": ["slide_number"]
            }
        ),
        Tool(
            name="get_available_layouts",
            description="获取可用布局列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（可选，默认为当前文档）"
                    }
                }
            }
        )
    ]
