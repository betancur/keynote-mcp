"""
Slide operation tools - Modular structure

This module provides slide operations organized into specialized submodules:
- basic_operations: CRUD operations (add, delete, duplicate, move)
- navigation_operations: Navigation and information retrieval
- layout_operations: Layout management
- schemas: Tool schema definitions
- base: Main SlideTools class that integrates all operations
"""

from .base import SlideTools

__all__ = ['SlideTools']
