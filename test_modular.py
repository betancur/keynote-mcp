#!/usr/bin/env python3
"""
Test script for the modular Keynote-MCP architecture.
Tests the new theme-aware functions and modular AppleScript structure.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.applescript_runner import AppleScriptRunner
from src.tools.content import ContentTools

async def test_modular_architecture():
    """Test the modular AppleScript architecture."""
    print("🔧 Testing Modular Architecture...")
    
    # Initialize tools
    runner = AppleScriptRunner()
    content_tools = ContentTools()
    
    try:
        # Test 1: Check if modular files exist
        print("\n📁 Checking modular AppleScript files...")
        for script_name, file_path in content_tools.script_files.items():
            full_path = os.path.join(os.path.dirname(__file__), "src", "applescript", file_path)
            if os.path.exists(full_path):
                print(f"✅ {script_name}: {file_path}")
            else:
                print(f"❌ {script_name}: {file_path} - NOT FOUND")
        
        # Test 2: Test AppleScript runner with a simple function
        print("\n🍎 Testing AppleScript runner...")
        try:
            # Test running a function from slide_content_simple.applescript
            result = runner.run_function(
                "slide_content_simple.applescript", 
                "getSlideDefaultElements", 
                ["", 1]
            )
            print(f"✅ AppleScript function execution: SUCCESS")
            print(f"   Result type: {type(result)}")
        except Exception as e:
            print(f"❌ AppleScript function execution failed: {e}")
        
        # Test 3: Test theme-aware content tools
        print("\n🎨 Testing theme-aware content tools...")
        try:
            # This would require Keynote to be open, so we'll just check the method exists
            if hasattr(content_tools, 'set_slide_content'):
                print("✅ set_slide_content method exists")
            else:
                print("❌ set_slide_content method missing")
                
            if hasattr(content_tools, 'get_slide_default_elements'):
                print("✅ get_slide_default_elements method exists")
            else:
                print("❌ get_slide_default_elements method missing")
                
        except Exception as e:
            print(f"❌ Theme-aware tools test failed: {e}")
        
        print("\n🎉 Modular architecture test completed!")
        print("\n📝 Note: Full functionality testing requires Keynote to be open with a presentation.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that all required files are in place."""
    print("\n📂 Testing file structure...")
    
    required_files = [
        "src/applescript/text_content.applescript",
        "src/applescript/media_content.applescript", 
        "src/applescript/shapes_tables.applescript",
        "src/applescript/formatting.applescript",
        "src/applescript/object_management.applescript",
        "src/tools/content.py",
        "src/utils/applescript_runner.py",
        "docs/MODULAR_ARCHITECTURE.md",
        "docs/THEME_AWARE_CONTENT.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  {len(missing_files)} files are missing!")
        return False
    else:
        print(f"\n🎉 All {len(required_files)} required files are present!")
        return True

if __name__ == "__main__":
    print("🚀 Starting Keynote-MCP Modular Architecture Test\n")
    
    # Test file structure first
    structure_ok = test_file_structure()
    
    if structure_ok:
        # Run async tests
        try:
            asyncio.run(test_modular_architecture())
        except Exception as e:
            print(f"❌ Async test failed: {e}")
    else:
        print("❌ Skipping functional tests due to missing files.")
    
    print("\n" + "="*50)
    print("Test completed. Check output above for any issues.")
