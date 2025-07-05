# Keynote-MCP

A Model Context Protocol (MCP) server that enables AI assistants to control Keynote presentations through AppleScript automation.

> **🎉 This is an enhanced fork** featuring modular architecture, theme-aware content management, and comprehensive documentation improvements.

## Features
- **Presentation Management**: Create, open, save, close presentations  
- **Slide Operations**: Add, delete, duplicate, move slides
- **Theme-Aware Content**: Professional content placement using Keynote's design elements
- **Modular Architecture**: Maintainable codebase with specialized AppleScript modules
- **Export Functions**: Screenshots, PDF export

## Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/betancur/keynote-mcp.git
   cd keynote-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Grant macOS permissions**
   - System Preferences > Security & Privacy > Privacy
   - Add Terminal and Python to **Accessibility** permissions  
   - Add Python to **Automation** permissions for Keynote

4. **Configure Claude Desktop**
   Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "keynote": {
         "command": "python3",
         "args": ["/path/to/keynote-mcp/mcp_server.py"]
       }
     }
   }
   ```

5. **Test the server**
   ```bash
   python3 test_server.py
   ```

> **Note**: Make sure Keynote is installed and you have appropriate permissions for automation.

## Available Tools (26 total)

### Presentation Management
- `create_presentation` - Create new presentation
- `open_presentation` - Open existing presentation  
- `save_presentation` - Save presentation
- `close_presentation` - Close presentation

### Slide Operations
- `add_slide` - Add new slide
- `delete_slide` - Delete slide
- `duplicate_slide` - Copy slide
- `move_slide` - Reorder slides

### Content Management
- `add_text_box` - Add text to slide
- `add_image` - Add image to slide
- `set_slide_content` - 🆕 Set content using theme elements (recommended)
- `get_slide_default_elements` - 🆕 Check available theme elements

### Export & Capture
- `screenshot_slide` - Take slide screenshot
- `export_pdf` - Export as PDF

### Theme-Aware Features
Our latest update includes **theme-aware content management** that uses Keynote's built-in design elements for professional-looking presentations with consistent styling.

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](./docs/) directory:

- **[📖 Documentation Index](./docs/README.md)** - Complete documentation overview
- **[🏗️ Modular Architecture](./docs/MODULAR_ARCHITECTURE.md)** - AppleScript modular structure
- **[🎨 Theme-Aware Content](./docs/THEME_AWARE_CONTENT.md)** - Best practices for theme elements
- **[🗺️ Project Roadmap](./docs/ROADMAP.md)** - Future development plans and features

### Quick Links
- **Getting Started**: Follow the Quick Setup section above
- **For Developers**: [Modular Architecture](./docs/MODULAR_ARCHITECTURE.md)
- **Best Practices**: [Theme-Aware Content](./docs/THEME_AWARE_CONTENT.md)

## 💡 Usage Examples

### Theme-Aware Content (Recommended)
```python
# Create new presentation
result = await call_tool("create_presentation", {
    "name": "My Presentation"
})

# Add slide with theme-aware content
result = await call_tool("add_slide", {
    "title": "Welcome", 
    "layout": "Title & Content"
})

# Set content using theme elements (automatic positioning & styling)
result = await call_tool("set_slide_content", {
    "title": "Project Overview",
    "subtitle": "Q4 2024 Results", 
    "bullet_points": ["Revenue up 15%", "New markets entered", "Team expansion"]
})

# Check what theme elements are available
result = await call_tool("get_slide_default_elements", {"slide_number": 1})
```

### Manual Content Placement
```python
# Add text to specific position
result = await call_tool("add_text_box", {
    "text": "Custom positioned text",
    "x": 100,
    "y": 200
})

# Add image with precise placement
result = await call_tool("add_image", {
    "image_path": "/path/to/image.jpg",
    "x": 300,
    "y": 150
})
```

## 🚀 What's New in This Fork

This enhanced version includes significant improvements over the original:

### ✨ **Major Enhancements**
- **🏗️ Modular Architecture**: Split monolithic AppleScript into 5 specialized modules for better maintainability
- **🎨 Theme-Aware Content**: Smart content placement using Keynote's built-in design elements
- **📚 Comprehensive Documentation**: Complete guides in the `docs/` folder
- **🔧 Enhanced Integration**: Improved Python-AppleScript modular execution
- **🌍 Internationalization**: All Chinese comments translated to English

### 🎯 **Key Benefits**
- **Professional Results**: Theme-aware functions create presentations with consistent styling
- **Better Performance**: Modular loading only loads necessary AppleScript code
- **Easier Maintenance**: Specialized files for different functionality areas
- **Developer Friendly**: Complete documentation and architecture guides

> **Credits**: This fork is based on the original [keynote-mcp](https://github.com/easychen/keynote-mcp) by [@easychen](https://github.com/easychen). We've enhanced it with modern architecture and professional content management features.

## License
MIT License
