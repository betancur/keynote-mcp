"""
Export and screenshot tools
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number, validate_file_path, ParameterError
import tempfile
import os
import shutil
from pathlib import Path


class ExportTools:
    """Export and screenshot tools class"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """Get all export and screenshot tools"""
        return [
            Tool(
                name="screenshot_slide",
                description="📸 SLIDE SCREENSHOT: Capture a high-quality image of a specific slide for sharing, embedding, or preview purposes. This tool exports individual slides as image files in PNG or JPG format, maintaining the original slide quality and aspect ratio.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "Target slide number to capture (1-based indexing)",
                            "minimum": 1
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Full file path where the screenshot will be saved (include filename and extension)",
                            "examples": ["/Users/username/Desktop/slide-1.png", "~/Documents/presentation-cover.jpg", "/tmp/slide-screenshot.png"]
                        },
                        "format": {
                            "type": "string",
                            "description": "Image format for the output file",
                            "enum": ["png", "jpg"],
                            "default": "png"
                        }
                    },
                    "required": ["slide_number", "output_path"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="export_pdf",
                description="📄 PDF EXPORTER: Export the entire presentation as a high-quality PDF document. Perfect for sharing presentations via email, printing, or creating handouts. The PDF preserves all formatting, fonts, and layout exactly as they appear in Keynote.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "output_path": {
                            "type": "string",
                            "description": "Full file path where the PDF will be saved (must include .pdf extension)",
                            "examples": ["/Users/username/Desktop/presentation.pdf", "~/Documents/Q4-Review.pdf", "/tmp/slides-export.pdf"]
                        }
                    },
                    "required": ["output_path"],
                    "additionalProperties": False
                }
            ),
            Tool(
                name="export_images",
                description="🖼️ BULK IMAGE EXPORT: Export all slides as a sequence of individual image files. Perfect for creating slide galleries, web content, or when you need each slide as a separate image file. Images are automatically named with slide numbers.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "output_dir": {
                            "type": "string",
                            "description": "Directory path where all slide images will be saved (directory will be created if it doesn't exist)",
                            "examples": ["/Users/username/Desktop/slides/", "~/Documents/presentation-images/", "/tmp/exported-slides/"]
                        },
                        "format": {
                            "type": "string",
                            "description": "Image format for all exported slide files",
                            "enum": ["png", "jpg"],
                            "default": "png"
                        }
                    },
                    "required": ["output_dir"],
                    "additionalProperties": False
                }
            )
        ]
    
    async def screenshot_slide(self, slide_number: int, output_path: str, format: str = "png") -> List[TextContent]:
        """Screenshot single slide"""
        try:
            validate_slide_number(slide_number)
            validate_file_path(output_path)
            
            # Set export format
            export_format = "JPEG" if format.lower() == "jpg" else "PNG"
            
            # Get directory and filename from output path
            output_dir = os.path.dirname(output_path)
            output_filename = os.path.basename(output_path)
            
            # Create temporary export folder
            temp_dir = tempfile.mkdtemp()
            
            try:
                script = f'''
                tell application "Keynote"
                    tell front document
                        export slide {slide_number} as {export_format} to POSIX file "{temp_dir}/"
                    end tell
                end tell
                '''
                
                result = self.runner.run_inline_script(script)
                
                # Ensure output directory exists
                os.makedirs(output_dir, exist_ok=True)
                
                # Find generated file and rename to target filename
                temp_files = os.listdir(temp_dir)
                if temp_files:
                    # Move first file to target location
                    src_file = os.path.join(temp_dir, temp_files[0])
                    shutil.move(src_file, output_path)
                    
                    # Clean up temporary folder
                    shutil.rmtree(temp_dir)
                    
                    return [TextContent(
                        type="text",
                        text=f"✅ Screenshot saved: {output_path}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="❌ No screenshot file generated"
                    )]
                    
            finally:
                # Clean up temporary folder
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Screenshot failed: {str(e)}"
            )]
    
    async def export_pdf(self, output_path: str) -> List[TextContent]:
        """Export presentation as PDF"""
        try:
            validate_file_path(output_path)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)
            
            script = f'''
            tell application "Keynote"
                tell front document
                    export to POSIX file "{output_path}" as PDF
                end tell
            end tell
            '''
            
            result = self.runner.run_inline_script(script)
            
            return [TextContent(
                type="text",
                text=f"✅ PDF exported: {output_path}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ PDF export failed: {str(e)}"
            )]
    
    async def export_images(self, output_dir: str, format: str = "png") -> List[TextContent]:
        """Export all slides as image sequence"""
        try:
            validate_file_path(output_dir)
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Set export format
            export_format = "JPEG" if format.lower() == "jpg" else "PNG"
            
            script = f'''
            tell application "Keynote"
                tell front document
                    export as {export_format} to POSIX file "{output_dir}/"
                end tell
            end tell
            '''
            
            result = self.runner.run_inline_script(script)
            
            return [TextContent(
                type="text",
                text=f"✅ Images exported to: {output_dir}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Image export failed: {str(e)}"
            )]
