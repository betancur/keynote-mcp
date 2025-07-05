#!/usr/bin/env python3
"""
Simple test to verify the modular architecture files are in place.
"""

import os

def test_file_structure():
    """Test that all required files are in place."""
    print("🚀 Keynote-MCP Modular Architecture File Check\n")
    print("📂 Testing file structure...")
    
    base_dir = os.path.dirname(__file__)
    
    required_files = [
        "src/applescript/text_content.applescript",
        "src/applescript/media_content.applescript", 
        "src/applescript/shapes_tables.applescript",
        "src/applescript/formatting.applescript",
        "src/applescript/object_management.applescript",
        "src/tools/content.py",
        "src/utils/applescript_runner.py",
        "docs/MODULAR_ARCHITECTURE.md",
        "docs/THEME_AWARE_CONTENT.md",
        "docs/ROADMAP.md",
        "docs/README.md"
    ]
    
    missing_files = []
    present_files = []
    
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
            present_files.append(file_path)
        else:
            print(f"❌ {file_path} - NOT FOUND")
            missing_files.append(file_path)
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Present: {len(present_files)}")
    print(f"   ❌ Missing: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️  Missing files:")
        for file in missing_files:
            print(f"     - {file}")
        return False
    else:
        print(f"\n🎉 All {len(required_files)} required files are present!")
        return True

def check_applescript_content():
    """Check if AppleScript files contain expected functions."""
    print("\n🍎 Checking AppleScript content...")
    
    base_dir = os.path.dirname(__file__)
    
    applescript_checks = {
        "text_content.applescript": ["setSlideContent", "getSlideDefaultElements", "addTitle"],
        "media_content.applescript": ["addImageFromPath", "addImageFromUnsplash"],
        "shapes_tables.applescript": ["addShape", "addTable"],
        "formatting.applescript": ["setTextStyle", "setSlideBackground"],
        "object_management.applescript": ["deleteObject", "moveObject"]
    }
    
    for file_name, expected_functions in applescript_checks.items():
        file_path = os.path.join(base_dir, "src", "applescript", file_name)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                found_functions = []
                missing_functions = []
                
                for func in expected_functions:
                    if f"on {func}" in content:
                        found_functions.append(func)
                    else:
                        missing_functions.append(func)
                
                print(f"📄 {file_name}:")
                print(f"   ✅ Found: {len(found_functions)} functions")
                if missing_functions:
                    print(f"   ⚠️  Missing: {missing_functions}")
                
            except Exception as e:
                print(f"❌ Error reading {file_name}: {e}")
        else:
            print(f"❌ {file_name}: File not found")

def check_python_integration():
    """Check Python files for modular integration."""
    print("\n🐍 Checking Python integration...")
    
    base_dir = os.path.dirname(__file__)
    
    # Check content.py for script_files mapping
    content_py_path = os.path.join(base_dir, "src", "tools", "content.py")
    if os.path.exists(content_py_path):
        try:
            with open(content_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "script_files" in content:
                print("✅ content.py: script_files mapping found")
            else:
                print("⚠️  content.py: script_files mapping not found")
                
            if "set_slide_content" in content:
                print("✅ content.py: set_slide_content method found")
            else:
                print("⚠️  content.py: set_slide_content method not found")
                
        except Exception as e:
            print(f"❌ Error reading content.py: {e}")
    else:
        print("❌ content.py: File not found")
    
    # Check applescript_runner.py for run_function method
    runner_py_path = os.path.join(base_dir, "src", "utils", "applescript_runner.py")
    if os.path.exists(runner_py_path):
        try:
            with open(runner_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "run_function" in content and "def run_function" in content:
                print("✅ applescript_runner.py: run_function method found")
            else:
                print("⚠️  applescript_runner.py: run_function method not found")
                
        except Exception as e:
            print(f"❌ Error reading applescript_runner.py: {e}")
    else:
        print("❌ applescript_runner.py: File not found")

if __name__ == "__main__":
    print("="*60)
    success = test_file_structure()
    check_applescript_content() 
    check_python_integration()
    
    print("\n" + "="*60)
    if success:
        print("🎉 Modular architecture verification completed successfully!")
        print("📝 Note: Functional testing requires Keynote to be running.")
    else:
        print("⚠️  Some files are missing. Please check the output above.")
